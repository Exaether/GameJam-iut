from paths import get_data_path

def load_csv(filename, callback):
    with open(get_data_path(filename), "r") as file:
        for line in file:
            parts = line.strip().split(",")
            callback(parts)
