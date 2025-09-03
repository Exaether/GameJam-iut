#!/bin/bash

echo "Création de l'environnement virtuel..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Erreur lors de la création de l'environnement virtuel"
    exit 1
fi

echo "Environnement virtuel créé"

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Erreur lors de l'installation des dépendances"
    exit 1
fi

echo "Dépendances installées avec succès!"

echo "Pour lancer le jeu:"
echo "source ./venv/bin/activate"
echo "  python main.py"
echo "  deactivate (pour quitter)"