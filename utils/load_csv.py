def load_csv(path, callback):
    with open(path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            callback(parts)
