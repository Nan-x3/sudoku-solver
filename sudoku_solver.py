import tkinter as tk
from tkinter import messagebox

def clear_grid():
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)

def validate_input():
    for i in range(9):
        for j in range(9):
            value = entries[i][j].get()
            if value and not value.isdigit():
                messagebox.showerror("Invalid Input", "Please enter only numbers between 1 and 9.")
                return False
            if value and (int(value) < 1 or int(value) > 9):
                messagebox.showerror("Invalid Input", "Numbers must be between 1 and 9.")
                return False
    return True

def is_valid_sudoku(grid):
    def is_valid_block(block):
        block = [num for num in block if num != '.' and num != '']
        return len(block) == len(set(block))

    # Check rows and columns
    for i in range(9):
        if not is_valid_block(grid[i]):
            return False
        if not is_valid_block([grid[j][i] for j in range(9)]):
            return False

    # Check 3x3 subgrids
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            block = [
                grid[r][c]
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
            ]
            if not is_valid_block(block):
                return False

    return True

def check_sudoku():
    if not validate_input():
        return
    grid = [[entries[i][j].get() if entries[i][j].get() else '.' for j in range(9)] for i in range(9)]
    
    # Check if the grid is fully filled
    if any('.' in row for row in grid):
        messagebox.showerror("Sudoku Check", "The grid is incomplete. Please fill all cells.")
        return
    
    if is_valid_sudoku(grid):
        messagebox.showinfo("Sudoku Check", "Congratulations! The Sudoku is correctly solved.")
    else:
        messagebox.showerror("Sudoku Check", "The Sudoku is not solved correctly.")

def print_grid():
    if not validate_input():
        return
    grid = [[entries[i][j].get() if entries[i][j].get() else '.' for j in range(9)] for i in range(9)]
    for row in grid:
        print(" ".join(row))

# Backtracking algorithm to solve the Sudoku
def solve_sudoku(grid):
    def is_valid(num, row, col):
        # Check row
        if num in grid[row]:
            return False
        # Check column
        for i in range(9):
            if grid[i][col] == num:
                return False
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if grid[i][j] == num:
                    return False
        return True

    def solve():
        for row in range(9):
            for col in range(9):
                if grid[row][col] == '.':
                    for num in '123456789':
                        if is_valid(num, row, col):
                            grid[row][col] = num
                            if solve():
                                return True
                            grid[row][col] = '.'  # backtrack
                    return False
        return True

    if solve():
        return grid
    else:
        return None

def solve_and_update():
    grid = [[entries[i][j].get() if entries[i][j].get() else '.' for j in range(9)] for i in range(9)]
    
    solved_grid = solve_sudoku(grid)
    
    if solved_grid:
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, solved_grid[i][j])
    else:
        messagebox.showerror("Sudoku Solver", "No solution exists for the Sudoku puzzle.")

# Initialize the main tkinter window
root = tk.Tk()
root.title("Sudoku Solver UI")

# Create a 9x9 grid of Entry widgets
entries = [[None for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        entry = tk.Entry(root, width=2, font=('Arial', 18), justify='center')
        entry.grid(row=i, column=j, padx=5, pady=5)
        entries[i][j] = entry

# Add buttons for clearing, printing, solving, and checking the grid
clear_button = tk.Button(root, text="Clear Grid", command=clear_grid, font=('Arial', 14))
clear_button.grid(row=9, column=0, columnspan=3, pady=10)

print_button = tk.Button(root, text="Print Grid", command=print_grid, font=('Arial', 14))
print_button.grid(row=9, column=3, columnspan=3, pady=10)

check_button = tk.Button(root, text="Check Sudoku", command=check_sudoku, font=('Arial', 14))
check_button.grid(row=9, column=6, columnspan=3, pady=10)

solve_button = tk.Button(root, text="Solve Sudoku", command=solve_and_update, font=('Arial', 14))
solve_button.grid(row=10, column=0, columnspan=9, pady=10)

# Start the main event loop
root.mainloop()
