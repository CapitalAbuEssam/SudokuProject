import random

# grid: The Sudoku grid is a 9x9 2D list representing the puzzle.
# row, col: The coordinates of the cell where you want to place the number num.
# num: The number you want to check for validity in the specified cell.
def is_valid_move(grid, row, col, num):
    """ 
    Check if placing a number in the given cell is valid.
    It checks the row, column, and 3x3 subgrid for any duplicates.
    """
    # IT1: Check if the number is already in the same row or column
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    # IT2: Check if the number is already in the same 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True

""" 
Forward Checking steps:
1- Making a Hypothetical Move
2- Checking Immediate Consequences
3- Backtracking if Conflicts are Detected
"""
def forward_checking(grid, row, col, num):
    """ 
    Perform forward checking for a move. It temporarily places a number 
    in a cell and checks if this leads to any unsolvable condition in other cells.
    """
    grid[row][col] = num

    # Check all empty cells to see if they have at least one valid number left
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0 and not any(is_valid_move(grid, i, j, n) for n in range(1, 10)):
                grid[row][col] = 0  # Reset cell
                return False # No valid number left for any empty cell

    grid[row][col] = 0  # Reset cell
    return True # All empty cells still have at least one valid number left

def solve_sudoku(grid, use_forward_checking=True):
    """ 
    Solve the Sudoku puzzle using backtracking, optionally with forward checking.
    The function finds an empty cell and tries all numbers (1-9) in it.
    """
    # Find the next empty cell
    empty_cell = find_empty_location(grid)
    if not empty_cell:
        return True  # All cells are filled, puzzle solved

    row, col = empty_cell

    # Try all numbers for the current cell
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num) and (not use_forward_checking or forward_checking(grid, row, col, num)):
            grid[row][col] = num
            if solve_sudoku(grid, use_forward_checking):
                return True
            grid[row][col] = 0  # Reset cell if this path doesn't lead to a solution (BACKTRACKING)

    return False

def find_empty_location(grid):
    """ 
    Find the next empty cell (denoted by 0) in the grid. 
    Returns a tuple (row, col) if an empty cell is found, otherwise None.
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def print_grid(grid):
    """ Print the Sudoku grid with colors for better visualization. """
    color_map = {
        1: '\033[31m',  # Red
        2: '\033[32m',  # Green
        3: '\033[33m',  # Yellow
        4: '\033[34m',  # Blue
        5: '\033[35m',  # Magenta
        6: '\033[36m',  # Cyan
        7: '\033[91m',  # Light Red
        8: '\033[92m',  # Light Green
        9: '\033[93m',  # Light Yellow
        0: '\033[94m',  # Light Blue
    }
    for row in grid:
        colored_row = [
            color_map.get(num, '') + str(num) + '\033[0m' if num != 0 else '.'
            for num in row
        ]
        print(" ".join(colored_row))


def generate_sudoku():
    """ 
    Generate a random Sudoku grid with a minimal number of initial clues. 
    The function ensures that these clues don't violate Sudoku rules.
    """
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(17):  # 17 is the minimal number of clues for a valid Sudoku puzzle
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        # Ensure that the random number can be placed in the random cell
        while not is_valid_move(grid, row, col, num) or grid[row][col] != 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
        grid[row][col] = num
    return grid

# Main execution
# Generate a random initial Sudoku grid
initial_grid = generate_sudoku()
print("Initial Sudoku Grid:")
print_grid(initial_grid)

# Solve the puzzle with an option to enable or disable forward checking
if solve_sudoku(initial_grid, use_forward_checking=True):
    print("\nSudoku Puzzle Solved:")
    print_grid(initial_grid)
else:
    print("No solution exists")
