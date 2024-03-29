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
    If no preference given in data then return 0.
    """
    value = 0
    for row in preferences:
        if row[0] == person1 and row[1] == person2:
            value = row[2]
            return int(value)
    return 0


def tent_value(tent, preferences):
    """
    Calculate the total happiness value for a group.
    """
    total = 0
    for i in range(len(tent)):
        for j in range(len(tent)):
            if j != i:
                total += individual_value(tent[i], tent[j], preferences)
    return total


def value(assignment, preferences):
    """
    Get the total value for an assignment.
    """
    value = 0
    tent_groups = split_on_tents(assignment)
    for tent in tent_groups:
        value += tent_value(tent, preferences)
    return value


def display(result, verbose):
    # Sort the array based on the letter on the right
    print()
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


def test_display(test_results, num_tests):
    total = 0
    print()
    for result in test_results:
        total += result
    average = total / num_tests
    print(f"Average time: {average:0.4f}\n")


def search(goal, swaps, spots, names, pref_data):
    """
    Run the local searches until an assignment with a value at least as high \
    as the goal is found. \\
    Returns tuple (local_max, assignment, num_restarts)
    """
    restarts = 0
    local_max = 0  # highest value found from the last local search

    while local_max < goal:
        restarts += 1
        ## After every restart randomize the assignment.
        assignment = rand_assignment(names, spots)
        for _ in range(swaps):
            assignment = swap_up(spots, pref_data, local_max)
        local_max = value(assignment, pref_data)
    return (local_max, assignment, restarts)


if __name__ == "__main__":
    # Process arguments.
    parser = argparse.ArgumentParser(description="Tentmates")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show the number of restarts that happened or, if in test mode, \
            show the timings of each test",
    )
    parser.add_argument(
        "--test",
        type=int,
        default=None,
        help="The number of timing test to run. Leave blank to not run in test mode.",
    )
    parser.add_argument(
        "--goal",
        type=int,
        default=175,
        help="The the goal minimum accepted assignment value to search for. \
        Between 0 and 175)",
    )
    parser.add_argument(
        "--swaps",
        type=int,
        default=2,
        help="Number of consecutive swaps to a better state allowed before restart",
    )

    args = parser.parse_args()
    VERBOSE = args.verbose
    TEST_RUNS = args.test
    GOAL = args.goal
    # number of times to swap to a better position before taking the score and restarting
    SWAPS = args.swaps
    test_results = []

    preference_data = read_csv("tents-prefs.csv")
    tents_data = read_csv("tents-sizes.csv")
    spots = build_tent_spots(tents_data)
    names = sorted(list(set(row[0] for row in preference_data)))

    if TEST_RUNS == None:
        result = search(GOAL, SWAPS, spots, names, preference_data)
        display(result, VERBOSE)
    else:
        print()
        print(f"goal value: {GOAL}")
        print()
        for _ in range(TEST_RUNS):
            start = time.perf_counter()
            result = search(GOAL, SWAPS, spots, names, preference_data)
            stop = time.perf_counter()
            test_results.append(stop - start)
            local_max_value = result[0]
            if VERBOSE:
                print(f"Time: {stop-start:0.2f},    Score: {local_max_value} ")
        test_display(test_results, TEST_RUNS)
