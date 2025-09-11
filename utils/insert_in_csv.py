import csv
import os


def insert_in_csv(path, values, pos):
    # Lire toutes les lignes
    with open(path, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))

    # Limiter pos à la taille du fichier
    if pos < 0:
        pos = 0
    elif pos > len(reader):
        pos = len(reader)

    # Insérer la nouvelle ligne
    reader.insert(pos, values)

    # Écrire dans un fichier temporaire
    temp_filename = path + ".tmp"
    with open(temp_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(reader)

    # Remplacer l'ancien fichier par le temporaire
    os.replace(temp_filename, path)
