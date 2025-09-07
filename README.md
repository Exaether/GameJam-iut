# Le Château sans Portes

Jeu créent avec pygame
Thème Médieval
Contrainte Apparition, Disparition

## Installation

### Installation automatique (recommandée)
```bash
chmod +x install.sh
chmod +x create_exe_file.sh
./install.sh
./create_exe_file.sh
```

### Installation manuelle
1. Assurez-vous d'avoir Python 3.7+ installé
2. Créez un environnement virtuel :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Avec pyinstaller créent un executable 

## Lancement du jeu

### Manuellement
```bash
source venv/bin/activate
python main.py
deactivate (pour quitter)
```

### Executable Installer
Après installation de l'éxécutable
```bash
./{path}/dist/main
```

## Structure du projet

```
mon_jeu/
├── main.py              # Point d'entrée
├── components/          # Text, boutton et affichage de tout les menus
├── core/                # Gestion, calcul, il est le moteur du jeu
├── data/                # list des garde ou items crée on ajoute dans les csv avec separateur ','
├── entities/            # Gestion des entité en jeu (carte, joueur, enemy)
├── assets/
│   ├── images/          # Sprites et images
│   ├── sounds/          # Effets sonores
├── services/            # Gestion de la vision et des fichier musique ou police 
└── README.md
```

## Contrôles

### Menu
- clic souris

### Jeu (à venir)
- Utilisation du clavier
   - Espace pour intérargir
   - ZQSD ou flêche pour les déplacement