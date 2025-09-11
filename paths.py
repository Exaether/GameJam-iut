import os
import sys
from pathlib import Path

from core.settings import Settings

# Racine projet calculée une fois, là où ce fichier est placé (à la racine du projet)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_asset_path(*subpaths):
    """
    Construit le chemin absolu vers un fichier dans 'assets'.
    Exemple : get_asset_path('ui', 'panels', 'wood_panel_long.png')
    """
    return os.path.join(PROJECT_ROOT, 'assets', *subpaths)


def get_data_path(*subpaths):
    """
    Construit le chemin absolu vers un fichier dans 'assets'.
    Exemple : get_asset_path('ui', 'panels', 'wood_panel_long.png')
    """
    return os.path.join(PROJECT_ROOT, 'data', *subpaths)


def get_save_path(*subpaths):
    """Retourne un répertoire pour stocker les données persistantes."""
    if sys.platform == "win32":
        base = os.getenv("APPDATA")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:  # Linux / Unix
        base = os.path.expanduser("~/.local/share")

    *dirs, file_name = subpaths
    dir_path = Path(base) / Settings.GAME_FOLDER_NAME / Path(*dirs)

    dir_path.mkdir(parents=True, exist_ok=True)  # crée les dossiers non existants

    file_path = dir_path / file_name
    file_path.touch(exist_ok=True)  # crée le fichier s'il n'existe pas

    return str(file_path)
