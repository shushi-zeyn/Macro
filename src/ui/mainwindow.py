from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame, QStackedWidget, QTextEdit,
                               QListWidget, QFileDialog, QMessageBox, QComboBox, QSlider, QRadioButton, QGroupBox,
                               QCheckBox, QSpinBox)
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from datetime import datetime
from pathlib import Path
import json
from pynput import keyboard
from src.ui.styles import THEMES
from src.ui.languages import TRANSLATIONS
from src.core.engine import RecorderWorker, PlayerWorker

class KeySignal(QObject):
    pressed = Signal(str)

class InfoCard(QFrame):
    def __init__(self, title, value, icon=""):
        super().__init__()
        self.setProperty("class", "Card")
        self.setMinimumHeight(80)
        self.setMaximumHeight(100)
        l = QVBoxLayout(self)
        l.setContentsMargins(10, 10, 10, 10)
        l.setSpacing(5)
        
        self.title_lbl = QLabel(f"{icon} {title}")
        self.title_lbl.setProperty("class", "CardTitle")
        
        self.val = QLabel(value)
        self.val.setProperty("class", "CardValue")
        
        l.addWidget(self.title_lbl)
        l.addWidget(self.val)
        l.addStretch()

class Sidebar(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.setObjectName("Sidebar")
        self.parent = parent
        self.setMinimumWidth(180)
        self.setMaximumWidth(220)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(15, 20, 15, 15)
        l.setSpacing(8)
        
        self.logo = QLabel("SHUSHI HUB")
        self.logo.setObjectName("Logo")
        l.addWidget(self.logo)
        
        subtitle = QLabel("ULTIMATE")
        subtitle.setStyleSheet("color: #888; font-size: 10px;")
        l.addWidget(subtitle)
        l.addSpacing(15)
        
        self.btn1 = self.mk_btn("nav_dash", 0)
        self.btn2 = self.mk_btn("nav_macro", 1)
        self.btn3 = self.mk_btn("nav_config", 2)
        
        l.addStretch()
        
        self.status = QLabel("● STANDBY")
        self.status.setStyleSheet("color: #95a5a6; font-weight: bold; font-size: 11px;")
        l.addWidget(self.status)
        
        # Signature
        self.signature = QLabel("Made by Shushi")
        self.signature.setStyleSheet("color: #555; font-size: 10px; font-style: italic; margin-top: 5px;")
        self.signature.setAlignment(Qt.AlignCenter)
        l.addWidget(self.signature)

    def mk_btn(self, key, idx):
        b = QPushButton(key) # On stocke la clé de traduction temporairement
        b.setProperty("class", "NavBtn")
        b.setCheckable(True)
        b.setAutoExclusive(True)
        if idx == 0: b.setChecked(True)
        b.clicked.connect(lambda: self.parent.switch_page(idx))
        self.layout().addWidget(b)
        return b

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shushi Hub Ultimate")
        self.resize(900, 600)
        self.setMinimumSize(700, 500)
        
        self.macros_path = Path("macros")
        self.macros_path.mkdir(exist_ok=True)
        
        self.macro_data = []
        self.recording_mode = 'LITE'
        self.recorder = None
        self.player = None
        self.is_hidden = False
        self.current_lang = "EN" # Langue par défaut
        
        self.start_play_time = None
        self.target_duration = 0
        
        self.hk_play = 'f1'
        self.hk_rec = 'f2'
        self.hk_ghost = 'f3'
        
        self.key_bridge = KeySignal()
        self.key_bridge.pressed.connect(self.handle_hotkey)
        
        self.setup_ui()
        self.apply_theme("Dark Matte")
        self.retranslate_ui() # Appliquer les textes initiaux
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        self.start_global_listener()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
        
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages, 1)
        
        self.setup_dash()
        self.setup_macro_page()
        self.setup_config_page()

    def setup_dash(self):
        p = QWidget()
        l = QVBoxLayout(p)
        l.setContentsMargins(25, 25, 25, 25)
        l.setSpacing(15)
        
        header_layout = QHBoxLayout()
        self.greeting = QLabel()
        self.greeting.setObjectName("Greeting")
        header_layout.addWidget(self.greeting)
        header_layout.addStretch()
        
        self.lbl_duration = QLabel("00:00")
        self.lbl_duration.setStyleSheet("color: #bb86fc; font-weight: bold; font-size: 24px; font-family: monospace;")
        self.lbl_duration.setVisible(False)
        header_layout.addWidget(self.lbl_duration)
        l.addLayout(header_layout)
        
        h = QHBoxLayout()
        h.setSpacing(10)
        self.card_time = InfoCard("TIME", datetime.now().strftime("%H:%M:%S"), "🕒")
        self.card_evts = InfoCard("EVENTS", "0", "🎬")
        self.card_mode = InfoCard("MODE", "LITE", "⚙️")
        h.addWidget(self.card_time)
        h.addWidget(self.card_evts)
        h.addWidget(self.card_mode)
        l.addLayout(h)
        
        duration_frame = QFrame()
        duration_frame.setStyleSheet("background-color: rgba(255,255,255,0.05); border-radius: 8px;")
        d_layout = QHBoxLayout(duration_frame)
        d_layout.setContentsMargins(10, 5, 10, 5)
        
        self.lbl_mode_play = QLabel()
        self.lbl_mode_play.setStyleSheet("color: #ccc; font-weight: bold;")
        d_layout.addWidget(self.lbl_mode_play)
        
        self.chk_infinite = QCheckBox()
        self.chk_infinite.setStyleSheet("color: #fff;")
        self.chk_infinite.toggled.connect(self.toggle_duration_spin)
        d_layout.addWidget(self.chk_infinite)
        
        d_layout.addSpacing(20)
        
        self.lbl_spin = QLabel()
        self.lbl_spin.setStyleSheet("color: #ccc;")
        d_layout.addWidget(self.lbl_spin)
        
        self.spin_min = QSpinBox()
        self.spin_min.setRange(0, 999)
        self.spin_min.setSuffix(" min")
        self.spin_min.setStyleSheet("background-color: #333; color: white; padding: 5px;")
        d_layout.addWidget(self.spin_min)
        
        self.spin_sec = QSpinBox()
        self.spin_sec.setRange(0, 59)
        self.spin_sec.setSuffix(" s")
        self.spin_sec.setStyleSheet("background-color: #333; color: white; padding: 5px;")
        d_layout.addWidget(self.spin_sec)
        
        d_layout.addStretch()
        l.addWidget(duration_frame)
        
        self.hk_info = QLabel()
        self.hk_info.setStyleSheet("color: #888; font-size: 11px; padding: 5px;")
        l.addWidget(self.hk_info)
        
        h2 = QHBoxLayout()
        h2.setSpacing(10)
        self.btn_rec = QPushButton()
        self.btn_rec.setProperty("class", "ActionBtn")
        self.btn_rec.clicked.connect(self.toggle_rec)
        
        self.btn_play = QPushButton()
        self.btn_play.setProperty("class", "ActionBtn")
        self.btn_play.clicked.connect(self.toggle_play)
        
        h2.addWidget(self.btn_rec)
        h2.addWidget(self.btn_play)
        l.addLayout(h2)
        
        self.console_lbl = QLabel()
        self.console_lbl.setStyleSheet("font-weight: bold; font-size: 12px; margin-top: 5px;")
        l.addWidget(self.console_lbl)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(150)
        l.addWidget(self.console)
        
        self.pages.addWidget(p)

    def setup_macro_page(self):
        p = QWidget()
        l = QVBoxLayout(p)
        l.setContentsMargins(25, 25, 25, 25)
        l.setSpacing(15)
        
        self.title_macro = QLabel()
        self.title_macro.setStyleSheet("font-size: 22px; font-weight: bold; color: #bb86fc;")
        l.addWidget(self.title_macro)
        
        h = QHBoxLayout()
        h.setSpacing(10)
        self.btn_save = QPushButton()
        self.btn_save.setProperty("class", "ActionBtn")
        self.btn_save.clicked.connect(self.save_macro)
        self.btn_load = QPushButton()
        self.btn_load.setProperty("class", "ActionBtn")
        self.btn_load.clicked.connect(self.use_selected_macro)
        h.addWidget(self.btn_save)
        h.addWidget(self.btn_load)
        l.addLayout(h)
        
        self.list_label = QLabel()
        self.list_label.setStyleSheet("font-size: 12px; margin-top: 5px; color: #e0e0e0;")
        l.addWidget(self.list_label)
        
        self.list_w = QListWidget()
        self.list_w.itemDoubleClicked.connect(self.use_selected_macro)
        self.refresh_macro_list()
        l.addWidget(self.list_w)
        
        self.btn_refresh = QPushButton()
        self.btn_refresh.setProperty("class", "NavBtn")
        self.btn_refresh.clicked.connect(self.refresh_macro_list)
        l.addWidget(self.btn_refresh)
        
        self.pages.addWidget(p)

    def setup_config_page(self):
        p = QWidget()
        l = QVBoxLayout(p)
        l.setContentsMargins(25, 25, 25, 25)
        l.setSpacing(20)
        
        self.title_config = QLabel()
        self.title_config.setStyleSheet("font-size: 22px; font-weight: bold; color: #bb86fc;")
        l.addWidget(self.title_config)
        
        # Langue
        self.grp_lang = QGroupBox()
        lang_layout = QVBoxLayout(self.grp_lang)
        self.lbl_lang = QLabel()
        self.cb_lang = QComboBox()
        self.cb_lang.addItems(["English", "Français"])
        self.cb_lang.currentTextChanged.connect(self.change_language)
        lang_layout.addWidget(self.lbl_lang)
        lang_layout.addWidget(self.cb_lang)
        l.addWidget(self.grp_lang)
        
        # Thème
        self.grp_theme = QGroupBox()
        theme_layout = QVBoxLayout(self.grp_theme)
        self.lbl_theme = QLabel()
        self.cb_theme = QComboBox()
        self.cb_theme.addItems(THEMES.keys())
        self.cb_theme.currentTextChanged.connect(self.apply_theme)
        theme_layout.addWidget(self.lbl_theme)
        theme_layout.addWidget(self.cb_theme)
        l.addWidget(self.grp_theme)
        
        # Opacité
        self.grp_opacity = QGroupBox()
        opacity_layout = QVBoxLayout(self.grp_opacity)
        h_op = QHBoxLayout()
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(50, 100)
        self.slider_opacity.setValue(100)
        self.lbl_opacity_val = QLabel("100%")
        self.lbl_opacity_val.setFixedWidth(40)
        self.slider_opacity.valueChanged.connect(self.update_opacity)
        h_op.addWidget(self.slider_opacity)
        h_op.addWidget(self.lbl_opacity_val)
        opacity_layout.addLayout(h_op)
        l.addWidget(self.grp_opacity)
        
        # Mode
        self.grp_mode = QGroupBox()
        mode_layout = QVBoxLayout(self.grp_mode)
        self.rb_lite = QRadioButton()
        self.rb_lite.setChecked(True)
        self.rb_pro = QRadioButton()
        self.rb_lite.toggled.connect(lambda: self.set_recording_mode("LITE") if self.rb_lite.isChecked() else None)
        self.rb_pro.toggled.connect(lambda: self.set_recording_mode("PRO") if self.rb_pro.isChecked() else None)
        mode_layout.addWidget(self.rb_lite)
        mode_layout.addWidget(self.rb_pro)
        l.addWidget(self.grp_mode)
        
        # Hotkeys
        self.grp_hk = QGroupBox()
        hk_layout = QVBoxLayout(self.grp_hk)
        self.btn_hk_play = QPushButton(f"▶ Play: {self.hk_play.upper()}")
        self.btn_hk_rec = QPushButton(f"🔴 Rec: {self.hk_rec.upper()}")
        self.btn_hk_ghost = QPushButton(f"👻 Ghost: {self.hk_ghost.upper()}")
        hk_layout.addWidget(self.btn_hk_play)
        hk_layout.addWidget(self.btn_hk_rec)
        hk_layout.addWidget(self.btn_hk_ghost)
        l.addWidget(self.grp_hk)
        
        l.addStretch()
        self.pages.addWidget(p)

    # --- Internationalisation ---

    def change_language(self, lang_name):
        code = "FR" if lang_name == "Français" else "EN"
        if code != self.current_lang:
            self.current_lang = code
            self.retranslate_ui()
            self.console.append(self.tr("log_lang"))

    def tr(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

    def retranslate_ui(self):
        # Sidebar
        self.sidebar.btn1.setText(self.tr("nav_dash"))
        self.sidebar.btn2.setText(self.tr("nav_macro"))
        self.sidebar.btn3.setText(self.tr("nav_config"))
        self.sidebar.status.setText(self.tr("status_standby"))
        self.sidebar.signature.setText(self.tr("made_by"))
        
        # Dashboard
        self.update_greeting()
        self.card_time.title_lbl.setText(f"🕒 {self.tr('card_time')}")
        self.card_evts.title_lbl.setText(f"🎬 {self.tr('card_events')}")
        self.card_mode.title_lbl.setText(f"⚙️ {self.tr('card_mode')}")
        self.hk_info.setText(self.tr("hk_info"))
        self.btn_rec.setText(self.tr("btn_rec"))
        self.btn_play.setText(self.tr("btn_play"))
        self.console_lbl.setText(self.tr("logs_title"))
        self.lbl_mode_play.setText(self.tr("mode_play"))
        self.chk_infinite.setText(self.tr("infinite"))
        self.lbl_spin.setText(self.tr("duration"))
        
        # Macros
        self.title_macro.setText(self.tr("title_macro"))
        self.btn_save.setText(self.tr("btn_save"))
        self.btn_load.setText(self.tr("btn_load"))
        self.list_label.setText(self.tr("list_label"))
        self.btn_refresh.setText(self.tr("btn_refresh"))
        
        # Config
        self.title_config.setText(self.tr("title_config"))
        self.grp_lang.setTitle(self.tr("grp_lang"))
        self.lbl_lang.setText(self.tr("lbl_lang"))
        self.grp_theme.setTitle(self.tr("grp_theme"))
        self.lbl_theme.setText(self.tr("lbl_theme"))
        self.grp_opacity.setTitle(self.tr("grp_opacity"))
        self.grp_mode.setTitle(self.tr("grp_mode"))
        self.rb_lite.setText(self.tr("rb_lite"))
        self.rb_pro.setText(self.tr("rb_pro"))
        self.grp_hk.setTitle(self.tr("grp_hk"))

    # --- Logique ---

    def toggle_duration_spin(self):
        is_infinite = self.chk_infinite.isChecked()
        self.spin_min.setEnabled(not is_infinite)
        self.spin_sec.setEnabled(not is_infinite)
        self.lbl_spin.setStyleSheet("color: #555;" if is_infinite else "color: #ccc;")

    def toggle_rec(self):
        if self.player and self.player.isRunning():
            self.console.append(self.tr("err_conflict_rec"))
            return

        if self.recorder and self.recorder.isRunning():
            self.recorder.stop_recording()
        else:
            self.recorder = RecorderWorker(self.recording_mode)
            self.recorder.log_signal.connect(self.console.append)
            self.recorder.finished.connect(self.fin_rec)
            self.recorder.start()
            
            self.btn_rec.setText(self.tr("btn_stop_rec"))
            self.btn_rec.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
            self.sidebar.status.setText(self.tr("status_rec"))
            self.sidebar.status.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.btn_play.setEnabled(False)
            self.btn_play.setStyleSheet("background-color: #333; color: #555;")
            self.console.append(self.tr("msg_rec_start"))

    def fin_rec(self, events):
        self.macro_data = events
        self.card_evts.val.setText(str(len(events)))
        
        self.btn_rec.setText(self.tr("btn_rec"))
        self.btn_rec.setProperty("class", "ActionBtn")
        self.style().unpolish(self.btn_rec); self.style().polish(self.btn_rec)
        
        self.sidebar.status.setText(self.tr("status_standby"))
        self.sidebar.status.setStyleSheet("color: #95a5a6; font-weight: bold;")
        self.console.append(f"{self.tr('msg_rec_end')} {len(events)}")
        
        self.btn_play.setEnabled(True)
        self.btn_play.setProperty("class", "ActionBtn")
        self.style().unpolish(self.btn_play); self.style().polish(self.btn_play)

    def toggle_play(self):
        if self.recorder and self.recorder.isRunning():
            self.console.append(self.tr("err_conflict_play"))
            return

        if self.player and self.player.isRunning():
            self.player.stop_playback()
        else:
            if not self.macro_data:
                QMessageBox.information(self, "Info", self.tr("err_no_data"))
                return

            is_infinite = self.chk_infinite.isChecked()
            duration_min = self.spin_min.value()
            duration_sec = self.spin_sec.value()
            total_seconds = (duration_min * 60) + duration_sec
            
            self.player = PlayerWorker()
            self.player.log_signal.connect(self.console.append)
            self.player.status_signal.connect(self.update_status)
            self.player.finished.connect(self.fin_play)
            
            self.player.start_playback(self.macro_data, infinite=is_infinite, duration=total_seconds)
            
            self.btn_play.setText(self.tr("btn_stop_play"))
            self.btn_play.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
            self.btn_rec.setEnabled(False)
            self.btn_rec.setStyleSheet("background-color: #333; color: #555;")
            self.console.append(self.tr("msg_play_start"))
            
            self.start_play_time = datetime.now()
            self.target_duration = total_seconds
            self.lbl_duration.setVisible(True)
            if is_infinite:
                self.lbl_duration.setText("∞")
            else:
                self.lbl_duration.setText("00:00")

    def fin_play(self):
        self.btn_play.setText(self.tr("btn_play"))
        self.btn_play.setProperty("class", "ActionBtn")
        self.style().unpolish(self.btn_play); self.style().polish(self.btn_play)
        
        self.btn_rec.setEnabled(True)
        self.btn_rec.setProperty("class", "ActionBtn")
        self.style().unpolish(self.btn_rec); self.style().polish(self.btn_rec)
        
        self.lbl_duration.setVisible(False)
        self.start_play_time = None
        self.console.append(self.tr("msg_play_end"))

    def update_status(self, msg, color):
        # On ne traduit pas les messages techniques du worker pour l'instant, ou on pourrait
        self.sidebar.status.setText(f"● {msg}")
        self.sidebar.status.setStyleSheet(f"color: {color}; font-weight: bold;")

    def set_recording_mode(self, mode):
        self.recording_mode = mode
        self.card_mode.val.setText(mode)
        self.console.append(f"{self.tr('log_mode')} {mode}")

    def switch_page(self, idx):
        self.pages.setCurrentIndex(idx)
        if idx == 1:
            self.refresh_macro_list()

    def apply_theme(self, name):
        if name in THEMES:
            self.setStyleSheet(THEMES[name])
            self.console.append(f"{self.tr('log_theme')} {name}")

    def update_opacity(self, value):
        self.setWindowOpacity(value / 100.0)
        self.lbl_opacity_val.setText(f"{value}%")

    def get_greeting(self):
        h = datetime.now().hour
        if 5 <= h < 13: return self.tr("greeting_morning")
        elif 13 <= h < 18: return self.tr("greeting_afternoon")
        else: return self.tr("greeting_evening")

    def update_greeting(self):
        self.greeting.setText(self.get_greeting())

    def update_time(self):
        self.card_time.val.setText(datetime.now().strftime("%H:%M:%S"))
        if self.start_play_time and self.player and self.player.isRunning():
            elapsed = (datetime.now() - self.start_play_time).total_seconds()
            if self.chk_infinite.isChecked():
                m, s = divmod(int(elapsed), 60)
                self.lbl_duration.setText(f"∞ {m:02d}:{s:02d}")
            elif self.target_duration > 0:
                remaining = max(0, self.target_duration - elapsed)
                m, s = divmod(int(remaining), 60)
                self.lbl_duration.setText(f"⏳ {m:02d}:{s:02d}")
            else:
                self.lbl_duration.setText(self.tr("cycle"))

    def refresh_macro_list(self):
        self.list_w.clear()
        for f in self.macros_path.glob("*.json"):
            self.list_w.addItem(f.name)

    def save_macro(self):
        if not self.macro_data:
            QMessageBox.warning(self, "Info", self.tr("warn_empty"))
            return

        fname, _ = QFileDialog.getSaveFileName(
            self, self.tr("btn_save"), str(self.macros_path), "JSON (*.json)"
        )
        if fname:
            try:
                data = {"mode": self.recording_mode, "events": self.macro_data}
                with open(fname, 'w') as f:
                    json.dump(data, f, indent=4)
                self.console.append(f"{self.tr('log_saved')} {Path(fname).name}")
                self.refresh_macro_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"{self.tr('err_save')} {e}")

    def use_selected_macro(self):
        current_item = self.list_w.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Info", self.tr("warn_select"))
            return
        
        macro_name = current_item.text()
        file_path = self.macros_path / macro_name
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.macro_data = data
                else:
                    self.macro_data = data.get("events", [])
                    mode = data.get("mode", "LITE")
                    self.set_recording_mode(mode)
                    if mode == "PRO": self.rb_pro.setChecked(True)
                    else: self.rb_lite.setChecked(True)
            
            self.console.append(f"{self.tr('log_loaded')} {macro_name}")
            self.card_evts.val.setText(str(len(self.macro_data)))
            self.switch_page(0)
            self.sidebar.btn1.setChecked(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{self.tr('err_load')} {e}")
    
    def start_global_listener(self):
        self.listener = keyboard.Listener(on_press=self._on_global_press)
        self.listener.start()
        self.console.append(self.tr("log_init"))

    def _on_global_press(self, key):
        try:
            k = key.char if hasattr(key, 'char') else str(key).replace('Key.', '')
            k = k.lower()
            if k == self.hk_play: self.key_bridge.pressed.emit('play')
            elif k == self.hk_rec: self.key_bridge.pressed.emit('rec')
            elif k == self.hk_ghost: self.key_bridge.pressed.emit('ghost')
        except: pass

    def handle_hotkey(self, action):
        if action == 'play': self.toggle_play()
        elif action == 'rec': self.toggle_rec()
        elif action == 'ghost': self.toggle_ghost()

    def toggle_ghost(self):
        if self.is_hidden:
            self.showNormal()
            self.activateWindow()
            self.raise_()
            self.is_hidden = False
            self.console.append(self.tr("msg_ghost_off"))
        else:
            self.hide()
            self.is_hidden = True
            print(self.tr("msg_ghost_on"))

    def closeEvent(self, event):
        if hasattr(self, 'listener'):
            self.listener.stop()
        event.accept()
