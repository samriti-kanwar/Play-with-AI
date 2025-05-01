import tkinter as tk
from tkinter import messagebox
from collections import deque




# Directions for up, down, left, right movement
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class MazeSolver:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = None
        self.goal = None
        self.path = []  # Path will store the coordinates of the path from start to goal
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.queue = deque()  # BFS queue
        self.moves = 0  # Counter for the moves
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Label for instructions
        self.instruction_label = tk.Label(self.root, text="Left-click to set Start (Green), Right-click to set Goal (Red).")
        self.instruction_label.pack()

        # Label for move counter
        self.move_counter_label = tk.Label(self.root, text="Moves: 0")
        self.move_counter_label.pack()

        self.draw_maze()
        self.create_buttons()

    def draw_maze(self):
        self.canvas.delete("all")
        size = 400
        cell_size = size // self.rows
        
        # Draw the grid and the obstacles
        for r in range(self.rows):
            for c in range(self.cols):
                color = "white" if self.maze[r][c] == 0 else "black"
                self.canvas.create_rectangle(c * cell_size, r * cell_size,
                                             (c + 1) * cell_size, (r + 1) * cell_size,
                                             fill=color)

        # Mark the start and goal points if they exist
        if self.start:
            start_x, start_y = self.start
            self.canvas.create_oval(start_y * cell_size + cell_size // 4, start_x * cell_size + cell_size // 4,
                                    (start_y + 1) * cell_size - cell_size // 4, (start_x + 1) * cell_size - cell_size // 4,
                                    fill="green", outline="black")
        if self.goal:
            goal_x, goal_y = self.goal
            self.canvas.create_oval(goal_y * cell_size + cell_size // 4, goal_x * cell_size + cell_size // 4,
                                    (goal_y + 1) * cell_size - cell_size // 4, (goal_x + 1) * cell_size - cell_size // 4,
                                    fill="red", outline="black")

    def create_buttons(self):
        self.start_button = tk.Button(self.root, text="Start Pathfinding", command=self.start_bfs)
        self.start_button.pack()

    def is_valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and not self.visited[x][y] and self.maze[x][y] == 0

    def bfs(self):
        if not self.start or not self.goal:
            print("Start or Goal not set!")
            return

        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Reset visited
        self.queue.append((self.start[0], self.start[1], []))  # (x, y, path)

        while self.queue:
            x, y, path = self.queue.popleft()

            # Add current position to the path
            path.append((x, y))

            # If we reached the goal, return the path
            if (x, y) == self.goal:
                self.path = path
                return path

            # Explore the neighboring cells (up, down, left, right)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny):
                    self.visited[nx][ny] = True
                    self.queue.append((nx, ny, path))

        return None  # No path found

    def show_path(self):
        if self.path:
            size = 400
            cell_size = size // self.rows

            # Color the optimal path in blue
            for i, (x, y) in enumerate(self.path):
                self.canvas.create_rectangle(y * cell_size, x * cell_size,
                                             (y + 1) * cell_size, (x + 1) * cell_size,
                                             outline="white", fill="light blue", width=2)
                self.moves += 1  # Increment the move counter for each step
                self.move_counter_label.config(text=f"Moves: {self.moves}")  # Update move count
                self.root.update_idletasks()  # Update the GUI
                self.root.after(200)  # Delay for visualization

            # Show a message box after pathfinding is complete
            messagebox.showinfo("Path Found", f"Path found! Total moves: {self.moves}")

        else:
            print("No path found.")
            messagebox.showinfo("No Path", "No path found from start to goal.")

    def set_start(self, event):
        cell_size = 400 // self.rows
        x, y = event.y // cell_size, event.x // cell_size

        # Boundary check: Ensure the clicked position is within maze bounds
        if 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x][y] == 0:
            self.start = (x, y)
            self.draw_maze()
            self.instruction_label.config(text="Right-click to set Goal (Red).")  # Update instructions

    def set_goal(self, event):
        cell_size = 400 // self.rows
        x, y = event.y // cell_size, event.x // cell_size

        # Boundary check: Ensure the clicked position is within maze bounds
        if 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x][y] == 0:
            self.goal = (x, y)
            self.draw_maze()
            self.instruction_label.config(text="Click 'Start Pathfinding' to solve the maze.")  # Update instructions

    def start_bfs(self):
        if self.start and self.goal:
            self.moves = 0  # Reset the move counter when starting a new search
            self.bfs()
            self.show_path()
        else:
            print("Start or Goal not set!")
            self.start_button.config(state="disabled")  # Disable the button if start or goal is missing

def main():
    maze = [
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0]
    ]

    root = tk.Tk()
    root.title("Maze Solver - BFS")

    solver = MazeSolver(root, maze)

    
    solver.canvas.bind("<Button-1>", solver.set_start)  # Set start on left-click
    solver.canvas.bind("<Button-3>", solver.set_goal)   # Set goal on right-click

    root.mainloop()

if __name__ == "__main__":
    main()
