import bisect

from paths import get_save_path
from utils import load_csv, insert_in_csv


class ScoreStorage:
    def __init__(self):
        self.scores = []
        self.load_scores()

    def load_scores(self):
        scores = []

        def build_item(parts):
            if len(parts) == 3:
                items = int(parts[0])
                hour, minute = map(int, parts[1:])
                scores.append({"items": items, "time": {"hour": hour, "minute": minute}})

        load_csv(get_save_path('scores.csv'), build_item)
        self.scores = scores

    def save_score(self, score):
        def minutes_score(heure, minute, ref_h=22, ref_m=0):
            """Transforme une heure + minute en score circulaire autour de ref_h:ref_m"""
            total = heure * 60 + minute
            ref_total = ref_h * 60 + ref_m
            return (total - ref_total) % (24 * 60)

        def sort_key(score: dict) -> tuple[int, int]:
            """Retourne la clé de tri pour un item"""
            return -score["items"], minutes_score(score["time"]["hour"], score["time"]["minute"])

        keys = [sort_key(score) for score in self.scores]
        pos = bisect.bisect_left(keys, sort_key(score))

        self.scores.insert(pos, score)

        values = score["items"],score["time"]["hour"],score["time"]["minute"]

        insert_in_csv(get_save_path('scores.csv'), values, pos)
