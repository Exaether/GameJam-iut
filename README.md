# Mon Jeu Pygame

Un jeu créer avec Pygame

## Installation

### Installation automatique (recommandée)
```bash
chmod +x install.sh
./install.sh
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

## Lancement du jeu

### Manuellement
```bash
source venv/bin/activate
python main.py
deactivate (pour quitter)
```

## Structure du projet

```
mon_jeu/
├── main.py              # Point d'entrée
├── core/
│   ├── game.py          # Classe Game principale
│   ├── input_handler.py # Gestion des entrées
│   └── settings.py      # Classe qui contient les constantes
├── entities/
│   ├── player.py        # Classe Player
│   ├── enemy.py         # Classe Enemy
│   └── __init__.py
├── assets/
│   ├── images/          # Sprites et images
│   ├── sounds/          # Effets sonores
└── README.md
```

## Fonctionnalités actuelles

- Menu principal avec boutons "Jouer" et "Quitter"
- Seul le bouton "Quitter" est fonctionnel pour le moment
- Architecture prête pour ajouter le gameplay

## Prochaines étapes

- Implémenter l'écran de jeu
- Ajouter le joueur et les ennemis
- Ajouter les collisions et le gameplay

## Contrôles

### Menu
- Clic souris sur les boutons

### Jeu (à venir)
- Flèches directionnelles ou ZQSD pour se déplacer
