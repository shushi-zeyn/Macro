from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame, QStackedWidget, QTextEdit)
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
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
        self.setup_empty_page("Page Macros (À venir)")
        self.setup_empty_page("Page Config (À venir)")

    def setup_dash(self):
        p = QWidget()
        l = QVBoxLayout(p)
        l.setContentsMargins(25, 25, 25, 25)
        l.setSpacing(15)
        
        # Message de bienvenue
        self.greeting = QLabel(self.get_greeting())
        self.greeting.setObjectName("Greeting")
        l.addWidget(self.greeting)
        
        # Cards
        h = QHBoxLayout()
        h.setSpacing(10)
        self.card_time = InfoCard("HEURE", datetime.now().strftime("%H:%M:%S"), "🕒")
        self.card_evts = InfoCard("EVENTS", "0", "🎬")
        self.card_mode = InfoCard("MODE", "LITE", "⚙️")
        h.addWidget(self.card_time)
        h.addWidget(self.card_evts)
        h.addWidget(self.card_mode)
        l.addLayout(h)
        
        # Infos hotkeys
        self.hk_info = QLabel("⌨️ F1: Play | F2: Rec | F3: Ghost")
        self.hk_info.setStyleSheet("color: #888; font-size: 11px; padding: 5px;")
        l.addWidget(self.hk_info)
        
        # Boutons
        h2 = QHBoxLayout()
        h2.setSpacing(10)
        self.btn_rec = QPushButton("🔴 REC (F2)")
        self.btn_rec.setProperty("class", "ActionBtn")
        
        self.btn_play = QPushButton("▶ PLAY (F1)")
        self.btn_play.setProperty("class", "ActionBtn")
        
        h2.addWidget(self.btn_rec)
        h2.addWidget(self.btn_play)
        l.addLayout(h2)
        
        # Console
        console_lbl = QLabel("📊 LOGS")
        console_lbl.setStyleSheet("font-weight: bold; font-size: 12px; margin-top: 5px;")
        l.addWidget(console_lbl)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(150)
        self.console.append("[System] Interface chargée.")
        l.addWidget(self.console)
        
        self.pages.addWidget(p)

    def setup_empty_page(self, title):
        p = QWidget()
        l = QVBoxLayout(p)
        lbl = QLabel(title)
        lbl.setAlignment(Qt.AlignCenter)
        l.addWidget(lbl)
        self.pages.addWidget(p)

    def switch_page(self, idx):
        self.pages.setCurrentIndex(idx)

    def apply_theme(self, name):
        if name in THEMES:
            self.setStyleSheet(THEMES[name])

    def get_greeting(self):
        h = datetime.now().hour
        
        if 5 <= h < 13:
            return "☀️ Bonjour Shushi"
        elif 13 <= h < 18:
            return "🌤️ Bon après-midi Shushi"
        else:
            # De 18h à 05h du matin
            return "🌙 Bonsoir Shushi"

    def update_time(self):
        self.card_time.val.setText(datetime.now().strftime("%H:%M:%S"))
