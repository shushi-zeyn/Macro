import time
from pynput import keyboard, mouse
import pyautogui
from PySide6.QtCore import QThread, Signal

# Optimisations globales
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

class RecorderWorker(QThread):
    finished = Signal(list)
    log_signal = Signal(str)
    
    def __init__(self, mode='lite', hotkeys_to_ignore=None):
        super().__init__()
        self.recording = False
        self.mode = mode
        self.events = []
        self.start_time = None
        self.hotkeys_to_ignore = hotkeys_to_ignore or []
        
    def run(self):
        self.recording = True
        self.events = []
        self.start_time = time.time()
        self.log_signal.emit(f"🔴 Enregistrement démarré (Mode: {self.mode})")
        
        on_move = self._on_move if self.mode == 'PRO' else None
        
        with mouse.Listener(on_click=self._on_click, on_move=on_move) as m_listener:
            with keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release) as k_listener:
                while self.recording:
                    time.sleep(0.05)
        
        self.finished.emit(self.events)

    def stop_recording(self):
        self.recording = False
    
    def _on_key_press(self, key):
        if not self.recording: return
        try:
            k = key.char if hasattr(key, 'char') else str(key).replace('Key.', '')
            if k.lower() in self.hotkeys_to_ignore: return
            self.events.append({'t': time.time()-self.start_time, 'type': 'key_press', 'key': k})
        except: pass

    def _on_key_release(self, key):
        if not self.recording: return
        try:
            k = key.char if hasattr(key, 'char') else str(key).replace('Key.', '')
            if k.lower() in self.hotkeys_to_ignore: return
            self.events.append({'t': time.time()-self.start_time, 'type': 'key_release', 'key': k})
        except: pass

    def _on_click(self, x, y, button, pressed):
        if not self.recording: return
        self.events.append({
            't': time.time()-self.start_time, 'type': 'click', 
            'x': x, 'y': y, 'button': str(button).replace('Button.', ''), 'pressed': pressed
        })

    def _on_move(self, x, y):
        if not self.recording: return
        self.events.append({'t': time.time()-self.start_time, 'type': 'move', 'x': x, 'y': y})


class PlayerWorker(QThread):
    log_signal = Signal(str)
    status_signal = Signal(str, str)
    finished = Signal()
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.events = []
        self.loop = False
        
    def run(self):
        self.kb = keyboard.Controller()
        self.mouse = mouse.Controller() # Contrôleur souris pynput (plus rapide)
        
        self.status_signal.emit("RUNNING", "#2ecc71")
        self.log_signal.emit("▶ Lecture de la macro...")
        
        self.running = True
        
        while self.running:
            start_t = time.time()
            for event in self.events:
                if not self.running: break
                
                target = start_t + event['t']
                
                while time.time() < target and self.running:
                    time.sleep(0.001)
                
                if not self.running: break
                self._execute(event)
            
            if not self.loop: break
            time.sleep(0.1)
            
        self.status_signal.emit("STANDBY", "#95a5a6")
        self.log_signal.emit("⏸ Macro terminée")
        self.finished.emit()

    def stop_playback(self):
        self.running = False

    def start_playback(self, events, loop=False):
        self.events = events
        self.loop = loop
        self.start()

    def _execute(self, e):
        try:
            if e['type'] == 'key_press':
                k = self._parse_key(e['key'])
                if k: self.kb.press(k)
            elif e['type'] == 'key_release':
                k = self._parse_key(e['key'])
                if k: self.kb.release(k)
            elif e['type'] == 'click':
                # Pour le clic, on déplace d'abord la souris (via pynput pour la vitesse)
                self.mouse.position = (e['x'], e['y'])
                
                # Puis on clique (via pyautogui pour la fiabilité du clic)
                btn = 'left' if e['button'] == 'left' else 'right'
                if e['pressed']: 
                    pyautogui.mouseDown(button=btn)
                else: 
                    pyautogui.mouseUp(button=btn)
            elif e['type'] == 'move':
                # Mouvement ultra-rapide via pynput
                self.mouse.position = (e['x'], e['y'])
        except: pass

    def _parse_key(self, k_str):
        if len(k_str) == 1: return k_str
        return getattr(keyboard.Key, k_str, None)
