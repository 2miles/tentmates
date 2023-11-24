import csv
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


def assign(names, spots):
    """
    Associate each person to a tent spot.
    """
    result = []
    for i in range(len(names)):
        result.append([names[i], spots[i]])
    return result


def swap_up(spots, preferences, old_value):
    """
    Go through all possible swaps until one with a higher happiness is found.
    If all swaps have been tried, return the original assignment
    """
    best_spots = spots.copy()
    for i in range(len(spots)):
        for j in range(i + 1, len(spots)):
            spots[i], spots[j] = spots[j], spots[i]  # swap
            new_value = value(assign(names, spots), preferences)
            if new_value > old_value:
                return assign(names, spots)  # Return if a better assignment is found
            else:
                spots[i], spots[j] = spots[j], spots[i]  # swap back
    return assign(names, best_spots)


def random_swap(spots):
    # Randomly pick two distinct indices
    index1, index2 = random.sample(range(len(spots)), 2)
    # Ensure the selected elements are different
    while spots[index1] == spots[index2]:
        index2 = random.randint(0, len(spots) - 1)
    # Swap the elements at the selected indices
    spots[index1], spots[index2] = spots[index2], spots[index1]
    return spots


def rand_assignment(names, spots):
    random_swap(spots)
    assignment = assign(names, spots)
    return assignment


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


def display(max_value, restarts, assignment):
    # Sort the array based on the letter on the right
    sorted_data = sorted(assignment, key=lambda x: x[1])
    print(f"\nRestarts: {restarts}\n")
    print(f"{max_value}")
    for name, letter in sorted_data:
        print(f"{name} : {letter}")
    print()


if __name__ == "__main__":
    GOAL_VALUE = 160
    HILL_HEIGHT = 2  # number of times to swap to a better position before taking the score and restarting

    preference_data = read_csv("tents-prefs.csv")
    tents_data = read_csv("tents-sizes.csv")
    spots = build_tent_spots(tents_data)
    names = sorted(list(set(row[0] for row in preference_data)))

    local_max_value = 0  # highest value found from the last local search
    restarts = 0  # number of times the local search is restarted

    while local_max_value < GOAL_VALUE:
        restarts += 1
        assignment = rand_assignment(names, spots)
        for _ in range(HILL_HEIGHT):
            assignment = swap_up(spots, preference_data, local_max_value)
        local_max_value = value(assignment, preference_data)

    display(local_max_value, restarts, assignment)
