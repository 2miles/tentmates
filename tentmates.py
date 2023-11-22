import csv
from itertools import permutations


def read_csv(csv_file):
    data = []
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


def build_preferences(preference_data, names):
    all_pairs = [[name1, name2] for name1, name2 in permutations(names, 2)]
    # Populate name pairs with data from prefs_data.
    # If no preference was given between two people then mark that as a 0
    for pref_row in preference_data:
        for pair_row in all_pairs:
            if pref_row[0] == pair_row[0] and pref_row[1] == pair_row[1]:
                pair_row.append(pref_row[2])
    for row in all_pairs:
        if len(row) < 3:
            row.append("0")
    return all_pairs


def build_tent_spots(tents_data):
    result = []
    for row in tents_data:
        for _ in range(int(row[1])):
            result.append(row[0])
    return result


def initial_assignment(names, tent_spots):
    result = []
    for i in range(len(names)):
        result.append([names[i], tent_spots[i]])
    return result


def split_on_tents(assignment):
    """
    Takes an assignment list: `[['alan', 'a'], ['bob', 'a'], ['carol', 'b'], ['dave', 'b']]`
    Returns list of names grouped by tents: `[['alan', 'bob'], ['carol', 'dave']]`
    """
    # Initialize a dictionary to store names for each letter
    letter_dict = {}
    # Organize names by letter in the dictionary
    for name, letter in assignment:
        if letter not in letter_dict:
            letter_dict[letter] = []
        letter_dict[letter].append(name)
    # Convert the dictionary values to a list of lists
    result_lists = list(letter_dict.values())
    return result_lists


def get_happiness(assignment, preferences):
    # split into seperate lists for each tent
    tent_groups = split_on_tents(assignment)


if __name__ == "__main__":
    preference_data = read_csv("tents-prefs.csv")
    tents_data = read_csv("tents-sizes.csv")
    tent_spots = build_tent_spots(tents_data)
    names = sorted(list(set(row[0] for row in preference_data)))
    preferences = build_preferences(preference_data, names)
    preferences_sorted = sorted(preferences, key=lambda x: int(x[2]), reverse=True)
    assignment = initial_assignment(names, tent_spots)
    tent_groups = split_on_tents(assignment)

    print(f"preference_data: {preference_data}")
    print()
    print(f"tents: {tents_data}")
    print()
    print(f"preferences: ")
    for element in preferences_sorted:
        print(element)
    print(f"tent_spots: {tent_spots}")
    print(f"initial_assignment: {assignment}")
    print(f"tent_groups: {tent_groups}")
