def build_preferences(preference_data, names):
    """
    Return a list of the preferences of every combination of pairs of people.
    If no preference was given in the data file then assign it 0
    """
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


def rand_assign_until_happier(names, spots, preferences, old_value):
    """
    Do a random swap until the swap increased the value \\
    Then return that assignment
    """
    new_value = old_value
    count = 0
    og_assignment = assign(names, spots)
    while new_value <= old_value:
        count += 1
        if count >= 10000:
            return og_assignment
        assignment = rand_assignment(names, spots)
        new_value = value(assignment, preferences)
    return assignment


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


def are_arrays_same(array1, array2):
    """
    Return whether or not two arrays have the same elements.
    """
    # Convert each array to a set of tuples for comparison
    set1 = set(map(tuple, array1))
    set2 = set(map(tuple, array2))

    # Compare the sets
    return set1 == set2


def rand_hill_assignment(names, spots, preferences, happiness):
    count = 0
    ## swap one random person into a random tent
    random_swap(spots)
    assignment = assign(names, spots)

    while value(assignment, preferences) < happiness:
        count += 1
        if count == 100:
            return assignment
        random_swap(spots)
        assignment = assign(names, spots)
    return assignment
