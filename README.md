# Shushi Hub Ultimate ⚡

**Shushi Hub Ultimate** est une application d'automatisation (Macro Recorder) moderne, rapide et élégante développée en Python avec **PySide6**.

Elle permet d'enregistrer vos actions (clics, clavier, mouvements) et de les rejouer à l'infini ou selon une durée précise.

## ✨ Fonctionnalités

### 🎮 Enregistrement & Lecture
- **Mode Lite** : Enregistre uniquement les clics et les touches (léger et rapide).
- **Mode Pro** : Enregistre tous les mouvements de souris avec une fluidité parfaite (optimisé avec `pynput`).
- **Lecture Intelligente** :
  - ⏳ **Minuteur** : Définissez une durée précise (minutes/secondes).
  - ∞ **Boucle Infinie** : Laissez tourner la macro sans fin.
  - 🛡️ **Sécurité** : Impossible de lancer deux actions contradictoires en même temps.

### 🎨 Interface Moderne
- **Thèmes** : 6 thèmes inclus (Dark Matte, Blue, Green, Red, Purple, Glassmorphism).
- **Mode Ghost** : Cachez l'interface complètement avec `F3`.
- **Transparence** : Réglez l'opacité de la fenêtre pour voir ce qui se passe derrière.
- **Logs en temps réel** : Suivez chaque action dans la console intégrée.

### ⌨️ Raccourcis Clavier
- **F1** : Play / Stop
- **F2** : Rec / Stop
- **F3** : Mode Ghost (Cacher/Montrer)

## 🚀 Installation

1. **Cloner le projet**
2. **Créer un environnement virtuel** (recommandé) :
   ```bash
   python -m venv venv
   # Activer : venv\Scripts\activate (Windows)
   ```
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Lancement

Exécutez simplement le fichier principal :
```bash
python src/main.py
```

## 📂 Structure du Projet
- `src/core/` : Moteur d'enregistrement et de lecture (Multithreading).
- `src/ui/` : Interface graphique (PySide6) et styles.
- `macros/` : Dossier où sont sauvegardés vos fichiers `.json`.

---
*Développé avec ❤️ par Shushi Zeyn.*
