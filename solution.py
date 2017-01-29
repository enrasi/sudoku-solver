assignments = []

# Definition of the 9x9 grid
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.

    ###################################################33

    This method is enhanced to identify twins, triples and quads.

    """

    # we don't want to modify original values in the loops
    new_values = values.copy()

    # iterating evey possible set available
    for list in unitlist:
        # this variable keeps values with length 2
        list_of_2 = dict()
        for box in list:
            value = values[box]
            if len(value) > 1: # we are only interested in non single values

                # check if value is a twin, triple, quads etc...
                if value in list_of_2 and len(value) == list_of_2[value] + 1:
                    for new_box in list:
                        new_value = values[new_box]
                        if new_value != value and len(new_value) > 1:

                            # check whether number available in other locations in the set
                            for str in value:
                                if str in new_value:
                                    new_value = new_value.replace(str, '')
                                    new_values[new_box] = new_value
                else:
                    # This check is need for triples and above
                    if value in list_of_2:
                        list_of_2[value] = list_of_2[value] + 1
                    else:
                        list_of_2[value] = 1

    return new_values

def naked_pairs(values):
    pass

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

# assigning some variables which will be needed through-out the solution
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# calculating diagonal positions in the grid
diagonal = [[a + b for a, b in zip(rows, cols)], [a + b for a,b in zip(rows, reversed(cols))]]
# adding diagonal positions to unit list
unitlist = row_units + column_units + square_units + diagonal
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
        Eliminate single values presented in peers
        Args:
            values(dict): The sudoku in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    """
        In the units sometimes there may be only one place for one digit.
        This identifies those locations and fill them
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            The dictionary representation of the added only choice in sudoku
    """
    new_values = values.copy()
    for set in unitlist:
        value_count = dict() # temporary holder for keeping digit counts in unit
        for box in set:
            box_val = values[box]
            for str in box_val: # storing digits in full string
                if str not in value_count:
                    value_count[str] = []
                value_count[str].append(box)
        for value in value_count:
            if len(value_count[value]) == 1: # only one occurrence of digit
                new_values[value_count[value][0]] = value

    return new_values

def hidden_twins(values):

    """
        Sometimes there can be hidden pairs in a unit.
        E.g. {2, 345, 456, 37, 67, 9, 1, 367, 8}

        we can rearrange this as
        {2, 45, 45, 37, 67, 9, 1, 367, 8}
        This function does exactly that.

        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            The dictionary representation of the eliminated hidden twins of the sudoku
    """

    new_values = values.copy()
    for list in unitlist:
        numbers = dict() # variable to keep digits and their locations
        for box in list:
            value = values[box]
            if len(value) > 1:
                for number in value:
                    if number in numbers:
                        numbers[number] += box
                    else:
                        numbers[number] = box

        # filter out only pairs
        twins = { x: numbers[x] for x in numbers if len(numbers[x]) == 4 }
        for key in twins:
            for key2 in twins:
                # two digits only shares same location
                if key != key2 and twins[key] == twins[key2]:
                    number_val = twins[key]
                    # remove all other variables from those two locations
                    first_box = number_val[0] + number_val[1]
                    second_box = number_val[2] + number_val[3]
                    new_values[first_box] = key + key2
                    new_values[second_box] = key + key2

    return new_values


def two_out_of_three(values):

    pass

def naked_chains(values):

    pass

def reduce_puzzle(values):
    """
        Iterate eliminatee(), naked_twins() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        # add naked_twins before only_choice as this remove more values from only_choice
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):

    """
        Using depth-first search and propagation, create a search tree and solve the sudoku.
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    sudoku = reduce_puzzle(values)
    if sudoku == False:
        return False
    min_len = 10
    min_box = ''
    for box in boxes:
        length = len(values[box])
        assign_value(values, box, values[box])
        if length > 1 and length < min_len:
            min_len = length
            min_box = box
    if (min_box == ''):
        return sudoku
    else:
        for letter in sudoku[min_box]:
            new_sudoku = values.copy()
            new_sudoku[min_box] = letter
            returned_val = search(new_sudoku)
            if returned_val:
                return returned_val
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    solved_grid = search(grid_values(grid))
    if solved_grid:
        return solved_grid
    else:
        return []


if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    sol = solve(diag_sudoku_grid)
    if sol:
        display(sol)
    else:
        print('Given Sudoku can not be solved!')

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
