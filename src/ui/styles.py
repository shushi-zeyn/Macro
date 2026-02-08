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
        QGroupBox { border: 1px solid #2a2a2a; border-radius: 6px; margin-top: 10px; font-weight: bold; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
    """,
    
    "Blue Matte": """
        QMainWindow { background-color: #0d1b2a; }
        QWidget { color: #e0e1dd; font-family: 'Segoe UI', sans-serif; }
        QFrame#Sidebar { background-color: #1b263b; border-right: 1px solid #415a77; }
        QLabel#Logo { color: #5fa8d3; font-size: 20px; font-weight: bold; }
        QLabel#Greeting { color: #ffffff; font-size: 36px; font-weight: bold; }
        QPushButton.NavBtn {
            background-color: transparent; border: none; text-align: left; 
            padding: 12px; font-size: 13px; color: #778da9; border-radius: 8px;
        }
        QPushButton.NavBtn:hover { background-color: #415a77; color: white; }
        QPushButton.NavBtn:checked { background-color: #415a77; color: #5fa8d3; font-weight: bold; }
        QFrame.Card { background-color: #1b263b; border-radius: 10px; border: 1px solid #415a77; padding: 15px; }
        QLabel.CardValue { color: #5fa8d3; font-size: 22px; font-weight: bold; }
        QLabel.CardTitle { color: #778da9; font-size: 11px; }
        QPushButton.ActionBtn {
            background-color: #5fa8d3; color: #0d1b2a; border-radius: 8px; font-weight: bold; padding: 10px;
            font-size: 13px;
        }
        QPushButton.ActionBtn:hover { background-color: #7bb8e0; }
        QTextEdit { background-color: #0a0f1a; border: 1px solid #415a77; color: #5fa8d3; border-radius: 6px; 
                    padding: 8px; font-size: 12px; }
        QComboBox, QLineEdit { background-color: #415a77; color: white; border: 1px solid #5fa8d3; 
                               padding: 6px; border-radius: 6px; font-size: 12px; }
        QListWidget { background-color: #1b263b; border: 1px solid #415a77; color: white; border-radius: 6px; 
                     padding: 5px; font-size: 12px; }
        QRadioButton { color: #e0e1dd; font-size: 12px; }
        QLabel { color: #e0e1dd; font-size: 12px; }
        QGroupBox { border: 1px solid #415a77; border-radius: 6px; margin-top: 10px; font-weight: bold; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
    """,
    
    "Green Matte": """
        QMainWindow { background-color: #0f1a0f; }
        QWidget { color: #d8f3dc; font-family: 'Segoe UI', sans-serif; }
        QFrame#Sidebar { background-color: #1b4332; border-right: 1px solid #2d6a4f; }
        QLabel#Logo { color: #52b788; font-size: 20px; font-weight: bold; }
        QLabel#Greeting { color: #ffffff; font-size: 36px; font-weight: bold; }
        QPushButton.NavBtn {
            background-color: transparent; border: none; text-align: left; 
            padding: 12px; font-size: 13px; color: #74c69d; border-radius: 8px;
        }
        QPushButton.NavBtn:hover { background-color: #2d6a4f; color: white; }
        QPushButton.NavBtn:checked { background-color: #2d6a4f; color: #52b788; font-weight: bold; }
        QFrame.Card { background-color: #1b4332; border-radius: 10px; border: 1px solid #2d6a4f; padding: 15px; }
        QLabel.CardValue { color: #52b788; font-size: 22px; font-weight: bold; }
        QLabel.CardTitle { color: #74c69d; font-size: 11px; }
        QPushButton.ActionBtn {
            background-color: #52b788; color: #0f1a0f; border-radius: 8px; font-weight: bold; padding: 10px;
            font-size: 13px;
        }
        QPushButton.ActionBtn:hover { background-color: #74c69d; }
        QTextEdit { background-color: #081208; border: 1px solid #2d6a4f; color: #52b788; border-radius: 6px; 
                    padding: 8px; font-size: 12px; }
        QComboBox, QLineEdit { background-color: #2d6a4f; color: white; border: 1px solid #52b788; 
                               padding: 6px; border-radius: 6px; font-size: 12px; }
        QListWidget { background-color: #1b4332; border: 1px solid #2d6a4f; color: white; border-radius: 6px; 
                     padding: 5px; font-size: 12px; }
        QRadioButton { color: #d8f3dc; font-size: 12px; }
        QLabel { color: #d8f3dc; font-size: 12px; }
        QGroupBox { border: 1px solid #2d6a4f; border-radius: 6px; margin-top: 10px; font-weight: bold; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
    """,
    
    "Red Matte": """
        QMainWindow { background-color: #1a0f0f; }
        QWidget { color: #f3d8d8; font-family: 'Segoe UI', sans-serif; }
        QFrame#Sidebar { background-color: #3d1f1f; border-right: 1px solid #6a2d2d; }
        QLabel#Logo { color: #e76f51; font-size: 20px; font-weight: bold; }
        QLabel#Greeting { color: #ffffff; font-size: 36px; font-weight: bold; }
        QPushButton.NavBtn {
            background-color: transparent; border: none; text-align: left; 
            padding: 12px; font-size: 13px; color: #c9847a; border-radius: 8px;
        }
        QPushButton.NavBtn:hover { background-color: #6a2d2d; color: white; }
        QPushButton.NavBtn:checked { background-color: #6a2d2d; color: #e76f51; font-weight: bold; }
        QFrame.Card { background-color: #3d1f1f; border-radius: 10px; border: 1px solid #6a2d2d; padding: 15px; }
        QLabel.CardValue { color: #e76f51; font-size: 22px; font-weight: bold; }
        QLabel.CardTitle { color: #c9847a; font-size: 11px; }
        QPushButton.ActionBtn {
            background-color: #e76f51; color: #1a0f0f; border-radius: 8px; font-weight: bold; padding: 10px;
            font-size: 13px;
        }
        QPushButton.ActionBtn:hover { background-color: #f4a261; }
        QTextEdit { background-color: #120808; border: 1px solid #6a2d2d; color: #e76f51; border-radius: 6px; 
                    padding: 8px; font-size: 12px; }
        QComboBox, QLineEdit { background-color: #6a2d2d; color: white; border: 1px solid #e76f51; 
                               padding: 6px; border-radius: 6px; font-size: 12px; }
        QListWidget { background-color: #3d1f1f; border: 1px solid #6a2d2d; color: white; border-radius: 6px; 
                     padding: 5px; font-size: 12px; }
        QRadioButton { color: #f3d8d8; font-size: 12px; }
        QLabel { color: #f3d8d8; font-size: 12px; }
        QGroupBox { border: 1px solid #6a2d2d; border-radius: 6px; margin-top: 10px; font-weight: bold; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
    """,
    
    "Purple Matte": """
        QMainWindow { background-color: #1a0f1a; }
        QWidget { color: #f0e6f0; font-family: 'Segoe UI', sans-serif; }
        QFrame#Sidebar { background-color: #2d1b2d; border-right: 1px solid #5a2d5a; }
        QLabel#Logo { color: #c77dff; font-size: 20px; font-weight: bold; }
        QLabel#Greeting { color: #ffffff; font-size: 36px; font-weight: bold; }
        QPushButton.NavBtn {
            background-color: transparent; border: none; text-align: left; 
            padding: 12px; font-size: 13px; color: #b392b3; border-radius: 8px;
        }
        QPushButton.NavBtn:hover { background-color: #5a2d5a; color: white; }
        QPushButton.NavBtn:checked { background-color: #5a2d5a; color: #c77dff; font-weight: bold; }
        QFrame.Card { background-color: #2d1b2d; border-radius: 10px; border: 1px solid #5a2d5a; padding: 15px; }
        QLabel.CardValue { color: #c77dff; font-size: 22px; font-weight: bold; }
        QLabel.CardTitle { color: #b392b3; font-size: 11px; }
        QPushButton.ActionBtn {
            background-color: #c77dff; color: #1a0f1a; border-radius: 8px; font-weight: bold; padding: 10px;
            font-size: 13px;
        }
        QPushButton.ActionBtn:hover { background-color: #e0aaff; }
        QTextEdit { background-color: #120812; border: 1px solid #5a2d5a; color: #c77dff; border-radius: 6px; 
                    padding: 8px; font-size: 12px; }
        QComboBox, QLineEdit { background-color: #5a2d5a; color: white; border: 1px solid #c77dff; 
                               padding: 6px; border-radius: 6px; font-size: 12px; }
        QListWidget { background-color: #2d1b2d; border: 1px solid #5a2d5a; color: white; border-radius: 6px; 
                     padding: 5px; font-size: 12px; }
        QRadioButton { color: #f0e6f0; font-size: 12px; }
        QLabel { color: #f0e6f0; font-size: 12px; }
        QGroupBox { border: 1px solid #5a2d5a; border-radius: 6px; margin-top: 10px; font-weight: bold; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
    """,
    
    "Glassmorphism": """
        QMainWindow { background-color: rgba(30, 30, 30, 0.9); } 
        QWidget { color: #ffffff; font-family: 'Segoe UI', sans-serif; }
        QFrame#Sidebar { background-color: rgba(255, 255, 255, 0.08); border-right: 1px solid rgba(255,255,255,0.15); }
        QLabel#Logo { color: #ffffff; font-size: 20px; font-weight: bold; }
        QLabel#Greeting { color: #ffffff; font-size: 36px; font-weight: bold; }
        QPushButton.NavBtn { background-color: transparent; color: #ccc; border-radius: 8px; padding: 12px; text-align: left;
                            font-size: 13px; }
        QPushButton.NavBtn:hover { background-color: rgba(255, 255, 255, 0.12); }
        QPushButton.NavBtn:checked { background-color: rgba(255, 255, 255, 0.18); color: #fff; font-weight: bold; }
        QFrame.Card { background-color: rgba(255,255,255,0.08); border-radius: 12px; border: 1px solid rgba(255,255,255,0.12); 
                     padding: 15px; }
        QLabel.CardValue { color: #ffffff; font-size: 22px; font-weight: bold; }
        QLabel.CardTitle { color: rgba(255,255,255,0.7); font-size: 11px; }
        QPushButton.ActionBtn { background-color: rgba(255, 255, 255, 0.15); color: white; border-radius: 8px; 
                               padding: 10px; border: 1px solid rgba(255, 255, 255, 0.25); font-size: 13px; }
        QPushButton.ActionBtn:hover { background-color: rgba(255, 255, 255, 0.25); }
        QTextEdit { background-color: rgba(0,0,0,0.4); color: #00ffaa; border-radius: 6px; padding: 8px; 
                   border: 1px solid rgba(255,255,255,0.15); font-size: 12px; }
        QComboBox, QLineEdit { background-color: rgba(255, 255, 255, 0.1); color: white; 
                              border: 1px solid rgba(255, 255, 255, 0.2); padding: 6px; border-radius: 6px; 
                              font-size: 12px; }
        QListWidget { background-color: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); 
                     color: white; border-radius: 6px; padding: 5px; font-size: 12px; }
        QRadioButton { color: #ffffff; font-size: 12px; }
        QLabel { color: #ffffff; font-size: 12px; }
        QGroupBox { border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; margin-top: 10px; font-weight: bold; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
    """
}
