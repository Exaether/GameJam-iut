import traceback
from core.game import Game

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Erreur lors du lancement du jeu: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 