import csv


def read_csv(file):
    data = []
    with open(file, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


if __name__ == "__main__":
    prefs = read_csv("tents-prefs.csv")
    tents = read_csv("tents-sizes.csv")

    print(f"prefs: {prefs}")
    print()
    print(f"tents: {tents}")
