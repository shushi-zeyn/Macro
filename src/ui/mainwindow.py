from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame, QStackedWidget, QTextEdit,
                               QListWidget, QFileDialog, QMessageBox)
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
        self.setup_empty_page("Page Config (À venir)")

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
        
        # Boutons d'action
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
        
        # Liste des fichiers
        list_lbl = QLabel("📁 Macros disponibles (Double-clic pour charger):")
        list_lbl.setStyleSheet("font-size: 12px; margin-top: 5px; color: #e0e0e0;")
        l.addWidget(list_lbl)
        
        self.list_w = QListWidget()
        self.list_w.itemDoubleClicked.connect(self.use_selected_macro)
        self.refresh_macro_list() # On remplit la liste au démarrage
        l.addWidget(self.list_w)
        
        # Bouton Rafraîchir
        b_refresh = QPushButton("🔄 Rafraîchir la liste")
        b_refresh.setProperty("class", "NavBtn")
        b_refresh.clicked.connect(self.refresh_macro_list)
        l.addWidget(b_refresh)
        
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
        # Si on va sur la page Macros (index 1), on rafraîchit la liste
        if idx == 1:
            self.refresh_macro_list()

    def apply_theme(self, name):
        if name in THEMES:
            self.setStyleSheet(THEMES[name])

    def get_greeting(self):
        h = datetime.now().hour
        if 5 <= h < 13: return "☀️ Bonjour Shushi"
        elif 13 <= h < 18: return "🌤️ Bon après-midi"
        else: return "🌙 Bonsoir Shushi"

    def update_time(self):
        self.card_time.val.setText(datetime.now().strftime("%H:%M:%S"))

    # --- Logique Macros ---

    def refresh_macro_list(self):
        """Scanne le dossier macros/ et remplit la liste"""
        self.list_w.clear()
        # On cherche tous les fichiers .json
        for f in self.macros_path.glob("*.json"):
            self.list_w.addItem(f.name)

    def save_macro(self):
        """Ouvre une boîte de dialogue pour sauvegarder"""
        # Note: Pour l'instant on sauvegarde un fichier vide ou de test
        # car on n'a pas encore connecté le moteur d'enregistrement.
        fname, _ = QFileDialog.getSaveFileName(
            self, 
            "Sauvegarder la macro", 
            str(self.macros_path), 
            "JSON (*.json)"
        )
        
        if fname:
            try:
                # Simulation de données pour tester
                dummy_data = {"name": Path(fname).stem, "events": []}
                
                with open(fname, 'w') as f:
                    json.dump(dummy_data, f, indent=4)
                
                self.console.append(f"💾 Macro sauvegardée : {Path(fname).name}")
                self.refresh_macro_list()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde : {e}")

    def use_selected_macro(self):
        """Charge la macro sélectionnée dans la liste"""
        current_item = self.list_w.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner une macro dans la liste.")
            return
            
        macro_name = current_item.text()
        self.console.append(f"📂 Macro chargée : {macro_name}")
        # Ici on connectera plus tard le PlayerWorker pour jouer la macro
