from pygame.sprite import Group
from entities.enemyGroup import EnemyGroup
from entities.enemy import Enemy
from entities.item import Item
from paths import get_data_path
from utils.load_csv import load_csv


class LevelLoader:
    # Méthode interne pour construire un garde à partir d'une ligne du CSV
    @staticmethod
    def load_guards():
        guards_list = EnemyGroup()

        def build_guard(parts):
            # On ignore les lignes invalides
            if len(parts) >= 7:
                x, y, min_x, max_x, min_y, max_y = map(int, parts[:6])
                guard_type = parts[6]
                direction = parts[7] if len(parts) > 7 else None
                guard = Enemy(x, y, min_x, max_x, min_y, max_y, guard_type, direction)
                guards_list.add(guard)

        load_csv(get_data_path("guards.csv"), build_guard)
        return guards_list

    @staticmethod
    def load_items():
        items_list = Group()

        # Méthode interne pour construire un item à partir d'une ligne du CSV
        def build_item(parts):
            if len(parts) == 2:
                try:
                    x, y = map(int, parts)
                    item = Item(x, y)
                    items_list.add(item)
                except ValueError:
                    pass  # Ignore les valeurs non numériques

        load_csv(get_data_path("items.csv"), build_item)
        return items_list, len(items_list)
