import csv
from itertools import permutations
import random


def read_csv(csv_file):
    """
    Read from CSV file into a data array \\
    Return the data array
    """
    data = []
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


# def build_preferences(preference_data, names):
#     """
#     Return a list of the preferences of every combination of pairs of people.
#     If no preference was given in the data file then assign it 0
#     """
#     all_pairs = [[name1, name2] for name1, name2 in permutations(names, 2)]
#     # Populate name pairs with data from prefs_data.
#     # If no preference was given between two people then mark that as a 0
#     for pref_row in preference_data:
#         for pair_row in all_pairs:
#             if pref_row[0] == pair_row[0] and pref_row[1] == pair_row[1]:
#                 pair_row.append(pref_row[2])
#     for row in all_pairs:
#         if len(row) < 3:
#             row.append("0")
#     return all_pairs


def build_tent_spots(tents_data):
    """
    Given the tents data, return a list of all the spots available as a list of tent names \\
    Return: `[a, a, b, b, c, c, c, d, d, d, d, e, e, e, e]`
    """
    result = []
    for row in tents_data:
        for _ in range(int(row[1])):
            result.append(row[0])
    return result


def assign(names, tent_spots):
    """
    Associate each person to a tent spot.
    """
    result = []
    for i in range(len(names)):
        result.append([names[i], tent_spots[i]])
    return result


def random_swap(tent_spots):
    # Randomly pick two distinct indices
    index1, index2 = random.sample(range(len(tent_spots)), 2)
    # Ensure the selected elements are different
    while tent_spots[index1] == tent_spots[index2]:
        index2 = random.randint(0, len(tent_spots) - 1)
    # Swap the elements at the selected indices
    tent_spots[index1], tent_spots[index2] = tent_spots[index2], tent_spots[index1]
    return tent_spots


def rand_assignment(names, tent_spots):
    return assign(names, random_swap(tent_spots))


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


def individual_value(person1, person2, preferences):
    """
    Calculate one persons happiness value for another person.
    """
    value = 0
    for row in preferences:
        if row[0] == person1 and row[1] == person2:
            value = row[2]
            return int(value)
    return 0


def tent_value(tent, preferences):
    """
    Calculate the happiness value for an individual tent, given the preference data
    """
    total = 0
    for i in range(len(tent)):
        for j in range(len(tent)):
            if j != i:
                total += individual_value(tent[i], tent[j], preferences)
    return total


def value(assignment, preferences):
    # split into seperate lists for each tent
    value = 0
    tent_groups = split_on_tents(assignment)
    for tent in tent_groups:
        value += tent_value(tent, preferences)
    return value


def are_arrays_same(array1, array2):
    """
    Return whether or not two arrays have the same elements.
    """
    # Convert each array to a set of tuples for comparison
    set1 = set(map(tuple, array1))
    set2 = set(map(tuple, array2))

    # Compare the sets
    return set1 == set2


if __name__ == "__main__":
    BEST_HAPPINESS = 140

    preference_data = read_csv("tents-prefs.csv")
    tents_data = read_csv("tents-sizes.csv")
    spots = build_tent_spots(tents_data)
    names = sorted(list(set(row[0] for row in preference_data)))
    happiness = 0
    assignment = []
    while happiness < BEST_HAPPINESS:
        assignment = rand_assignment(names, spots)
        happiness = value(assignment, preference_data)
    print(f"YAY you found happiness of at least {BEST_HAPPINESS}")
    print(assignment)
    print(happiness)
