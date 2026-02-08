import sys
from pathlib import Path

# Ajout du dossier racine du projet au path pour les imports
# On remonte de 2 niveaux : main.py -> src -> Macro (Racine)
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from src.ui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
