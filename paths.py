# NE JAMAIS DEPLACER TOUJOUR A LA RACINE

import os

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