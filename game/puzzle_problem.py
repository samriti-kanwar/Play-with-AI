import pygame
import tkinter as tk
from tkinter import messagebox
import random
import heapq
import time
import copy
import threading



# Initialize Pygame
pygame.init()

# Set up sound effects
MOVE_SOUND = pygame.mixer.Sound("move.wav")
SHUFFLE_SOUND = pygame.mixer.Sound("shuffle.wav")
HINT_SOUND = pygame.mixer.Sound("hint.wav")
WIN_SOUND = pygame.mixer.Sound("win.wav")

class PuzzleSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 AI Puzzle Solver (8/15 Puzzle)")
        self.size = 3  # default 3x3
        self.goal_state = []
        self.board = []
        self.tiles = []
        self.moves = 0
        self.start_time = None
        self.timer_running = False

    
        self.create_ui()
        self.set_goal_state()
        self.reset_board()

    def create_ui(self):
        self.board_frame = tk.Frame(self.root, bg="#111", padx=10, pady=10)
        self.board_frame.pack()

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        tk.Button(self.control_frame, text="🔀 Shuffle", font=("Arial", 14), command=self.shuffle_board).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="🤖 Solve with AI", font=("Arial", 14), command=lambda: threading.Thread(target=self.solve_with_ai).start()).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="💡 Hint", font=("Arial", 14), command=self.show_hint).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="🔁 Reset", font=("Arial", 14), command=self.reset_board).pack(side=tk.LEFT, padx=5)

        self.size_var = tk.IntVar(value=3)
        tk.Radiobutton(self.root, text="3x3 (8-puzzle)", variable=self.size_var, value=3, command=self.change_size).pack()
        tk.Radiobutton(self.root, text="4x4 (15-puzzle)", variable=self.size_var, value=4, command=self.change_size).pack()

        self.info_label = tk.Label(self.root, text="Moves: 0 | Time: 00:00", font=("Arial", 12))
        self.info_label.pack(pady=5)

    def change_size(self):
        self.size = self.size_var.get()
        self.set_goal_state()
        self.reset_board()

    def set_goal_state(self):
        n = self.size * self.size
        self.goal_state = [[(i * self.size + j + 1) % n for j in range(self.size)] for i in range(self.size)]

    def reset_board(self):
        self.moves = 0
        self.timer_running = False
        self.board = copy.deepcopy(self.goal_state)
        self.draw_board()
        self.update_info()

    def shuffle_board(self):
        flat = list(range(self.size * self.size))
        random.shuffle(flat)
        while not self.is_solvable(flat):
            random.shuffle(flat)
        self.board = [flat[i*self.size:(i+1)*self.size] for i in range(self.size)]
        self.moves = 0
        self.start_time = time.time()
        self.timer_running = True
        self.draw_board()
        self.update_info()
        self.update_timer()
        self.play_sound(SHUFFLE_SOUND)

    def draw_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.tiles = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                tile = tk.Button(self.board_frame, font=("Helvetica", 20), width=4, height=2,
                                 command=lambda i=i, j=j: self.move_tile(i, j), bg="#333", fg="white")
                tile.grid(row=i, column=j, padx=3, pady=3)
                row.append(tile)
            self.tiles.append(row)
        self.update_ui()

    def update_ui(self):
        for i in range(self.size):
            for j in range(self.size):
                num = self.board[i][j]
                btn = self.tiles[i][j]
                btn["text"] = "" if num == 0 else str(num)
                btn["bg"] = "#111" if num == 0 else "#1976D2"

    def move_tile(self, i, j):
        if self.board[i][j] == 0:
            return
        x, y = self.find_blank()
        if abs(x - i) + abs(y - j) == 1:
            self.board[x][y], self.board[i][j] = self.board[i][j], self.board[x][y]
            self.moves += 1
            self.update_ui()
            self.update_info()
            self.play_sound(MOVE_SOUND)
            if self.board == self.goal_state:
                self.timer_running = False
                self.play_sound(WIN_SOUND)
                messagebox.showinfo("🎉 Congrats!", f"You solved it in {self.moves} moves!")

    def find_blank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j

    def is_solvable(self, flat):
        inv = 0
        for i in range(len(flat)):
            for j in range(i+1, len(flat)):
                if flat[i] and flat[j] and flat[i] > flat[j]:
                    inv += 1
        if self.size % 2 == 1:
            return inv % 2 == 0
        else:
            row = flat.index(0) // self.size
            return (inv + row) % 2 == 1

    def update_info(self):
        mins, secs = self.get_time()
        self.info_label.config(text=f"Moves: {self.moves} | Time: {mins:02}:{secs:02}")

    def update_timer(self):
        if self.timer_running:
            self.update_info()
            self.root.after(1000, self.update_timer)

    def get_time(self):
        if not self.start_time:
            return 0, 0
        elapsed = int(time.time() - self.start_time)
        return elapsed // 60, elapsed % 60

    def solve_with_ai(self):
        path = self.a_star(self.board)
        if not path:
            messagebox.showinfo("No Solution", "This puzzle has no solution.")
            return
        for state in path[1:]:
            self.board = state
            self.moves += 1
            self.update_ui()
            self.update_info()
            time.sleep(0.3)
        self.timer_running = False
        self.play_sound(WIN_SOUND)
        messagebox.showinfo("🧠 Solved by AI", f"AI solved in {len(path)-1} moves!")

    def show_hint(self):
        path = self.a_star(self.board)
        if path and len(path) > 1:
            self.board = path[1]
            self.moves += 1
            self.update_ui()
            self.update_info()
            self.play_sound(HINT_SOUND)
        else:
            messagebox.showinfo("Hint", "No moves left or already solved.")

    def a_star(self, start):
        def h(state):
            return sum(
                abs((val - 1) // self.size - i) + abs((val - 1) % self.size - j)
                for i in range(self.size) for j in range(self.size)
                if (val := state[i][j]) != 0
            )

        visited = set()
        heap = [(h(start), 0, start, [])]
        while heap:
            est, cost, state, path = heapq.heappop(heap)
            state_t = tuple(tuple(row) for row in state)
            if state == self.goal_state:
                return path + [state]
            if state_t in visited:
                continue
            visited.add(state_t)
            for next_state in self.get_neighbors(state):
                heapq.heappush(heap, (
                    cost + 1 + h(next_state),
                    cost + 1,
                    next_state,
                    path + [state]
                ))
        return None

    def get_neighbors(self, state):
        neighbors = []
        x, y = next((i, j) for i in range(self.size) for j in range(self.size) if state[i][j] == 0)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(new_state)
        return neighbors

    def play_sound(self, sound):
        sound.play()

    def draw_background(self, surface):
        surface.blit(self.bg_image, (0, 0))

    def mainloop(self):
        surface = pygame.display.set_mode((600, 600))
        clock = pygame.time.Clock()

        while True:
            surface.fill((0, 0, 0))  # Clear screen
            self.draw_background(surface)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()
            clock.tick(60)

# 🚀 Launch
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleSolverApp(root)
    root.mainloop()
