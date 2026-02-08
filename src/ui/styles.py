THEMES = {
    "Dark Matte": """
        QMainWindow { background-color: #121212; }
        QWidget { color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
        QFrame#Sidebar { background-color: #1e1e1e; border-right: 1px solid #2a2a2a; }
        QLabel#Logo { color: #bb86fc; font-size: 20px; font-weight: bold; }
        QLabel#Greeting { color: #ffffff; font-size: 36px; font-weight: bold; }
        QPushButton.NavBtn {
            background-color: transparent; border: none; text-align: left; 
            padding: 12px; font-size: 13px; color: #a0a0a0; border-radius: 8px;
        }
        QPushButton.NavBtn:hover { background-color: #2a2a2a; color: white; }
        QPushButton.NavBtn:checked { background-color: #2d2d2d; color: #bb86fc; font-weight: bold; }
        QFrame.Card { background-color: #1e1e1e; border-radius: 10px; border: 1px solid #2a2a2a; padding: 15px; }
        QLabel.CardValue { color: #bb86fc; font-size: 22px; font-weight: bold; }
        QLabel.CardTitle { color: #888; font-size: 11px; }
        QPushButton.ActionBtn {
            background-color: #bb86fc; color: #000; border-radius: 8px; font-weight: bold; padding: 10px;
            font-size: 13px;
        }
        QPushButton.ActionBtn:hover { background-color: #d0a0ff; }
        QTextEdit { background-color: #0a0a0a; border: 1px solid #2a2a2a; color: #03dac6; border-radius: 6px; 
                    padding: 8px; font-size: 12px; }
        QComboBox, QLineEdit { background-color: #2a2a2a; color: white; border: 1px solid #3a3a3a; 
                               padding: 6px; border-radius: 6px; font-size: 12px; }
        QListWidget { background-color: #1e1e1e; border: 1px solid #2a2a2a; color: white; border-radius: 6px; 
                     padding: 5px; font-size: 12px; }
        QRadioButton { color: #e0e0e0; font-size: 12px; }
        QLabel { color: #e0e0e0; font-size: 12px; }
    """
}
