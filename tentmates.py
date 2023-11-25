import csv
import random
import argparse
import time


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


def display(result, verbose):
    # Sort the array based on the letter on the right
    restarts = result[2]
    assignment = result[1]
    max_value = result[0]
    sorted_data = sorted(assignment, key=lambda x: x[1])
    if verbose:
        print(f"\nRestarts: {restarts}")
    print()
    print(f"{max_value}")
    for name, letter in sorted_data:
        print(f"{name} : {letter}")
    print()


def test_display(test_results, num_tests, goal_value, hill_height):
    total = 0
    for result in test_results:
        total += result
    average = total / num_tests
    print(f"Goal Value:  {goal_value}")
    print(f"Hill Height: {hill_height}")
    print(f"Average:     {average:0.4f}")


def search(GOAL_VALUE, HILL_HEIGHT, spots, names, pref_data):
    restarts = 0  # number of times the local search is restarted
    local_max_value = 0  # highest value found from the last local search

    while local_max_value < GOAL_VALUE:
        restarts += 1
        assignment = rand_assignment(names, spots)
        for _ in range(HILL_HEIGHT):
            assignment = swap_up(spots, pref_data, local_max_value)
        local_max_value = value(assignment, pref_data)
    return (local_max_value, assignment, restarts)


if __name__ == "__main__":
    # Process arguments.
    parser = argparse.ArgumentParser(description="VW Bug Puzzle.")
    parser.add_argument("--verbose", "-v", action="store_true", help="show solution")
    parser.add_argument("--test", "-a", action="store_true", help="show solution")
    parser.add_argument(
        "--goal",
        type=int,
        help="The the assignment value to search for. Between 0 and 175)",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="How many consecutive 'swaps to a better state' to do before restart",
    )

    args = parser.parse_args()
    VERBOSE = args.verbose
    TEST = args.test
    GOAL_VALUE = args.goal
    # number of times to swap to a better position before taking the score and restarting
    HILL_HEIGHT = args.height

    NUM_OF_TEST_RUNS = 10
    if GOAL_VALUE == None:
        GOAL_VALUE = 175
    if HILL_HEIGHT == None:
        HIll_HEIGHT = 2
    test_results = []

    preference_data = read_csv("tents-prefs.csv")
    tents_data = read_csv("tents-sizes.csv")
    spots = build_tent_spots(tents_data)
    names = sorted(list(set(row[0] for row in preference_data)))

    if TEST == False:
        result = search(GOAL_VALUE, HILL_HEIGHT, spots, names, preference_data)
        display(result, VERBOSE)
    else:
        for _ in range(NUM_OF_TEST_RUNS):
            start = time.perf_counter()
            result = search(GOAL_VALUE, HILL_HEIGHT, spots, names, preference_data)
            stop = time.perf_counter()
            test_results.append(stop - start)
            local_max_value = result[0]
            if VERBOSE:
                print(f"Time: {stop-start:0.2f},    Score: {local_max_value} ")
        test_display(test_results, NUM_OF_TEST_RUNS, GOAL_VALUE, HILL_HEIGHT)
