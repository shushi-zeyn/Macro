from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame, QStackedWidget, QTextEdit,
                               QListWidget, QFileDialog, QMessageBox, QComboBox, QSlider, QRadioButton, QGroupBox)
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
from pathlib import Path
import json
from src.ui.styles import THEMES

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
        
        self.btn1 = self.mk_btn("🏠 Dashboard", 0)
        self.btn2 = self.mk_btn("⚡ Macros", 1)
        self.btn3 = self.mk_btn("⚙️ Config", 2)
        
        l.addStretch()
        
        self.status = QLabel("● STANDBY")
        self.status.setStyleSheet("color: #95a5a6; font-weight: bold; font-size: 11px;")
        l.addWidget(self.status)

    def mk_btn(self, text, idx):
        b = QPushButton(text)
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
        
        # Gestion des dossiers
        self.macros_path = Path("macros")
        self.macros_path.mkdir(exist_ok=True)
        
        self.setup_ui()
        self.apply_theme("Dark Matte")
        
        # Timer Heure
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

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
        
        self.greeting = QLabel(self.get_greeting())
        self.greeting.setObjectName("Greeting")
        l.addWidget(self.greeting)
        
        h = QHBoxLayout()
        h.setSpacing(10)
        self.card_time = InfoCard("HEURE", datetime.now().strftime("%H:%M:%S"), "🕒")
        self.card_evts = InfoCard("EVENTS", "0", "🎬")
        self.card_mode = InfoCard("MODE", "LITE", "⚙️")
        h.addWidget(self.card_time)
        h.addWidget(self.card_evts)
        h.addWidget(self.card_mode)
        l.addLayout(h)
        
        self.hk_info = QLabel("⌨️ F1: Play | F2: Rec | F3: Ghost")
        self.hk_info.setStyleSheet("color: #888; font-size: 11px; padding: 5px;")
        l.addWidget(self.hk_info)
        
        h2 = QHBoxLayout()
        h2.setSpacing(10)
        self.btn_rec = QPushButton("🔴 REC (F2)")
        self.btn_rec.setProperty("class", "ActionBtn")
        
        self.btn_play = QPushButton("▶ PLAY (F1)")
        self.btn_play.setProperty("class", "ActionBtn")
        
        h2.addWidget(self.btn_rec)
        h2.addWidget(self.btn_play)
        l.addLayout(h2)
        
        console_lbl = QLabel("📊 LOGS")
        console_lbl.setStyleSheet("font-weight: bold; font-size: 12px; margin-top: 5px;")
        l.addWidget(console_lbl)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(150)
        self.console.append("[System] Interface chargée.")
        l.addWidget(self.console)
        
        self.pages.addWidget(p)

    def setup_macro_page(self):
        p = QWidget()
        l = QVBoxLayout(p)
        l.setContentsMargins(25, 25, 25, 25)
        l.setSpacing(15)
        
        title = QLabel("⚡ GESTION MACROS")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #bb86fc;")
        l.addWidget(title)
        
        h = QHBoxLayout()
        h.setSpacing(10)
        b_save = QPushButton("💾 Sauvegarder une macro")
        b_save.setProperty("class", "ActionBtn")
        b_save.clicked.connect(self.save_macro)
        b_use = QPushButton("▶ Utiliser la macro sélectionnée")
        b_use.setProperty("class", "ActionBtn")
        b_use.clicked.connect(self.use_selected_macro)
        h.addWidget(b_save)
        h.addWidget(b_use)
        l.addLayout(h)
        
        list_lbl = QLabel("📁 Macros disponibles (Double-clic pour charger):")
        list_lbl.setStyleSheet("font-size: 12px; margin-top: 5px; color: #e0e0e0;")
        l.addWidget(list_lbl)
        
        self.list_w = QListWidget()
        self.list_w.itemDoubleClicked.connect(self.use_selected_macro)
        self.refresh_macro_list()
        l.addWidget(self.list_w)
        
        b_refresh = QPushButton("🔄 Rafraîchir la liste")
        b_refresh.setProperty("class", "NavBtn")
        b_refresh.clicked.connect(self.refresh_macro_list)
        l.addWidget(b_refresh)
        
        self.pages.addWidget(p)

    def setup_config_page(self):
        p = QWidget()
        l = QVBoxLayout(p)
        l.setContentsMargins(25, 25, 25, 25)
        l.setSpacing(20)
        
        title = QLabel("⚙️ CONFIGURATION")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #bb86fc;")
        l.addWidget(title)
        
        # 1. Thèmes
        theme_group = QGroupBox("🎨 Apparence")
        theme_layout = QVBoxLayout(theme_group)
        
        lbl_theme = QLabel("Choisir un thème :")
        self.cb_theme = QComboBox()
        self.cb_theme.addItems(THEMES.keys())
        self.cb_theme.currentTextChanged.connect(self.apply_theme)
        
        theme_layout.addWidget(lbl_theme)
        theme_layout.addWidget(self.cb_theme)
        l.addWidget(theme_group)
        
        # 2. Opacité
        opacity_group = QGroupBox("👻 Transparence")
        opacity_layout = QVBoxLayout(opacity_group)
        
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
        l.addWidget(opacity_group)
        
        # 3. Mode Macro
        mode_group = QGroupBox("📹 Mode d'enregistrement")
        mode_layout = QVBoxLayout(mode_group)
        
        self.rb_lite = QRadioButton("Lite (Clics + Clavier uniquement)")
        self.rb_lite.setChecked(True)
        self.rb_pro = QRadioButton("Pro (Mouvements de souris complets)")
        
        # Connexion des signaux pour les logs
        self.rb_lite.toggled.connect(lambda: self.log_mode_change("LITE") if self.rb_lite.isChecked() else None)
        self.rb_pro.toggled.connect(lambda: self.log_mode_change("PRO") if self.rb_pro.isChecked() else None)
        
        mode_layout.addWidget(self.rb_lite)
        mode_layout.addWidget(self.rb_pro)
        l.addWidget(mode_group)
        
        # 4. Raccourcis
        hk_group = QGroupBox("⌨️ Raccourcis Clavier")
        hk_layout = QVBoxLayout(hk_group)
        
        self.btn_hk_play = QPushButton("▶ Play: F1")
        self.btn_hk_rec = QPushButton("🔴 Rec: F2")
        self.btn_hk_ghost = QPushButton("👻 Ghost: F3")
        
        hk_layout.addWidget(self.btn_hk_play)
        hk_layout.addWidget(self.btn_hk_rec)
        hk_layout.addWidget(self.btn_hk_ghost)
        l.addWidget(hk_group)
        
        l.addStretch()
        self.pages.addWidget(p)

    def switch_page(self, idx):
        self.pages.setCurrentIndex(idx)
        if idx == 1:
            self.refresh_macro_list()

    def apply_theme(self, name):
        if name in THEMES:
            self.setStyleSheet(THEMES[name])
            self.console.append(f"🎨 Thème appliqué : {name}")

    def update_opacity(self, value):
        self.setWindowOpacity(value / 100.0)
        self.lbl_opacity_val.setText(f"{value}%")

    def log_mode_change(self, mode):
        """Log le changement de mode et met à jour la carte"""
        self.console.append(f"⚙️ Mode changé : {mode}")
        self.card_mode.val.setText(mode)

    def get_greeting(self):
        h = datetime.now().hour
        if 5 <= h < 13: return "☀️ Bonjour Shushi"
        elif 13 <= h < 18: return "🌤️ Bon après-midi"
        else: return "🌙 Bonsoir Shushi"

    def update_time(self):
        self.card_time.val.setText(datetime.now().strftime("%H:%M:%S"))

    # --- Logique Macros ---

    def refresh_macro_list(self):
        self.list_w.clear()
        for f in self.macros_path.glob("*.json"):
            self.list_w.addItem(f.name)

    def save_macro(self):
        fname, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder la macro", str(self.macros_path), "JSON (*.json)"
        )
        if fname:
            try:
                dummy_data = {"name": Path(fname).stem, "events": []}
                with open(fname, 'w') as f:
                    json.dump(dummy_data, f, indent=4)
                self.console.append(f"💾 Macro sauvegardée : {Path(fname).name}")
                self.refresh_macro_list()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde : {e}")

    def use_selected_macro(self):
        current_item = self.list_w.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner une macro dans la liste.")
            return
        macro_name = current_item.text()
        self.console.append(f"📂 Macro chargée : {macro_name}")
