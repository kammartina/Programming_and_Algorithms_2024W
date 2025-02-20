#deque lets us add or remove items from both ends quickly, which is perfect for the breadth-first search (BFS) algorithm because we need to add paths at the end and take paths from the front.
from collections import deque
### FUNCTION that prints the labyrinth
def print_labyrinth(lab: list[str], path: list[tuple[int, int]] = None):
    # lab = a list of strings
    # path = An optional list of tuples where each tuple represents a coordinate (row, column) in the labyrinth.
    # None = man sieht‘s nicht während den Path gesucht wird, sondern nachdem path gefunden wurde, wird das ganze path angezeigt
    #   it‘s not the type hint here; it is a default value (if the value will not be passed, use this None value)

    # This helper function replaces a character in a string at a specified index. --> replacing spaces with X when finding a path
    # s = the original string
    # r = the replacement string
    # idx = The index at which to replace the character
    # len - works for replacements that is longer than 1
    def replace_at_index(s: str, r: str, idx: int) -> str:
        return s[:idx] + r + s[idx + len(r):]
        # returns: A new string with the character at idx replaced by r

    #MAIN LOGIC - Column numbers: Generates a string of column numbers for display
    # n_columns - Determines the number of columns in the labyrinth by checking the length of the first row
    # numbers - Creates a string of column numbers, where each number is the column iπndex modulo 10 (to keep it within a single digit).
    n_columns = len(lab[0])
    numbers = " " + "".join([str(i % 10) for i in range(n_columns)])
    # " " -> leeren Platz am anfang der Zeile mit den Nummern
    # "" -> damit zwischen den Zahlen kein Platz wird

    # prints the column numbers above the labyrinth
    print(numbers)

    # ROW PROCESSING: Iterates through each row of the labyrinth
    #iterate through each index of every row of the labyrinth; enumerate function iterates over lab (= list of coordinates, consisting of tuples) and
    # keeps track of both the index and the value of each item in this list
    # enumerate return us a tuple of indexes of the items and the value
    for i, row in enumerate(lab):
        # if a path is found / if the path is not None (= if the path variable contains any value or elements / whether this list is empty or not) than...
        if path:
            # iterate through every item (every tuple in the list of this path, = every coordinate, f.e. (3,3))
            for item in path:
                # checks if the current row of the path matches the current row being printed. If it does, it replaces the character at the specified
                #   column (item[1]) with "X" in the current row to mark that position as part of the path.(use the defined function replace_at_index in
                #   order to) mark it with 'X'
                #item[0] = This represents the row number of the current coordinate in the path. For example, if item is (1, 4), then item[0] is 1.
                #i = row number; This is the current row index of the labyrinth as you loop through it using enumerate.
                if item[0] == i: # literally checking "Is there a part of the path on this row?"
                    row = replace_at_index(row, "X", item[1])

        # Prints the row of the labyrinth with its index (= row numbers) on both sides
        # index = a number from 0 to 9
        print(f"{i %10}{row}{i % 10}")

    # prints the numbers below the laryrinth
    print(numbers)


### FUNCTION: Prompts the user to input an integer and validates the input.
# a function that takes in one parameter called "message" which is a type of str;
#  but it is expected that the function returns a value of type int
def prompt_integer(message: str) -> int:
    text = input(message)

    # .isdigit - checks if the input is a digit/an integer
    # infinite loop - checking until the unsers gives in an integer
    while not text.isdigit():
        print("Only integers accepted!")
        text = input(message)

    # The function then converts text from a string to an integer using int() and returns this integer as the result.
    return int(text)


### FUNCTION: Prompts the user to input a row and column for a location.
def prompt_user_for_location(name: str) -> tuple[int, int]:
    row = prompt_integer(f"Row of {name} location: ")
    column = prompt_integer(f"Column of {name} location: ")
    return row, column
    # returns tuple - with comma - pythonic way; hint in the first row is only hint


### BFS function to traverse a graph
def bfs(lab: list[str], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    # ... your implementation here...
    # Create a queue to hold all paths we considered up until now
    queue = deque ()
    # we enqueue start path (a queue with just the start location in it)
    queue.append([start])

    # Creating a set that holds all the locations that we have already visited
    visited_locations = set()

    # Continue the search while there are paths in the queue
    while queue:
        # dequeue the first path in the queue using pop (because index is known --> [0] --> first path in the queue)
        path = queue.popleft()
        # Get the last location in the current path
        last = path[-1]

        # Check if we've reached the end location
        # when the last location in our path equals the desired end location, we found a path
        if last == end:
            # Return the complete path to the end
            return path

        # if ‘last‘ is not in our set (= all visited locations), add it to the set
        if last not in visited_locations:
            visited_locations.add(last)

        # Define the possible moves (right, left, down, up)
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Explore each possible move (= calculate the next position)
        # This loop iterates over each of the moves above, applying them one by one to the current position.
        for move in moves:
            # Here, last represents the last position in the current path, and it’s a tuple (row, col).
            # By adding move[0] to last[0] (the row coordinate) and move[1] to last[1] (the column coordinate), we calculate the
            #   row and column of the next location
            next_row = last[0] + move[0]
            next_column = last[1] + move [1]
            # next_location is then formed as a tuple (next_row, next_col) to represent this new position.
            next_location = (next_row, next_column)
            # instead of the previous four rows: next_location = (last + move)

            if is_traversible(lab, next_location):
                next_path = path + [next_location]  # creating new possible path
                queue.append(next_path)  # adding to the queue

    # If there is no path found, return an empty list
    return []

def is_traversible(lab: list[str], location: tuple[int, int]) -> bool:
    # check if location is in labyrinth
    # check if character in location is " " and return True if yes
    row, column = location
    if 0 <= row < len(lab) and 0 <= column < len(lab[0]): # checks if location is not outside lab
        return lab[row][column] == " "
    else:
        return False



# HARD-CODED PATH
    #path = [(1, 4), (1, 5), (1, 6), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (5, 8), (5, 9), (5, 10)]
    #return path



# Labyrinth represented as a list of strings
labyrinth = [
    "█████████████",
    "█           █",
    "█ █████ █████",
    "█ █   █     █",
    "█ ███ █ █████",
    "█     █     █",
    "█████████████"
]

# prints the initial state of labyrinth
print_labyrinth(labyrinth)

# Prompts the user for start and end locations.
start_location = prompt_user_for_location("start")
end_location = prompt_user_for_location("end")

# Find path using breadth-first search between start and end locations
path = bfs(labyrinth, start_location, end_location)

# using the function print_labyrinth to print the labyrinth and the found path in it marked with 'X's
print_labyrinth(labyrinth, path)