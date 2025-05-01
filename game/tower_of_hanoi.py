import tkinter as tk
from tkinter import messagebox
import pygame


class TowerOfHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.num_disks = 3
        self.rods = {'A': [], 'B': [], 'C': []}
        self.selected_rod = None
        self.moves = []
        self.move_count = 0

        pygame.mixer.init()
        self.sounds = {
            'move': pygame.mixer.Sound("move1.wav"),
            'invalid': pygame.mixer.Sound("invalid.wav"),
            'success': pygame.mixer.Sound("sucess.wav")
        }

        self.setup_gui()

    def setup_gui(self):
        self.root.title("Tower of Hanoi")

        # Top controls
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        self.disk_option = tk.StringVar(value="3")
        tk.Label(self.control_frame, text="Select disks:").pack(side="left", padx=5)
        tk.OptionMenu(self.control_frame, self.disk_option, "3", "5").pack(side="left")

        tk.Button(self.control_frame, text="Start", command=self.initialize_game, bg="orange").pack(side="left", padx=10)

        self.Human_button = tk.Button(self.control_frame, text="Human mode", command=self.start_Human_mode, bg="lightblue")
        self.Human_button.pack(side="left", padx=10)

        self.aI_button = tk.Button(self.control_frame, text="AI Mode", command=self.start_aI_mode, bg="lightgreen")
        self.aI_button.pack(side="left", padx=10)

        # Status Labels
        self.mode_label = tk.Label(self.root, text="Select number of disks and click Start", font=("Arial", 12))
        self.mode_label.pack(pady=5)

        self.move_label = tk.Label(self.root, text="Moves: 0", font=("Arial", 12))
        self.move_label.pack(pady=5)

        # Canvas for rods and disks
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="lightgray")
        self.canvas.pack()

        self.rod_positions = {'A': 100, 'B': 300, 'C': 500}
        self.rod_height = 250
        self.rod_width = 15

        for rod in self.rod_positions:
            self.create_rod(rod)

    def create_rod(self, rod):
        x = self.rod_positions[rod]
        self.canvas.create_line(x, 100, x, self.rod_height, width=self.rod_width, fill="black")
        self.canvas.tag_bind(
            self.canvas.create_rectangle(x-40, 100, x+40, self.rod_height, outline="", tags=rod),
            "<Button-1>", lambda e, r=rod: self.on_rod_click(r)
        )
        self.canvas.create_text(x, 90, text=rod, font=("Arial", 14, "bold"))

    def initialize_game(self):
        self.num_disks = int(self.disk_option.get())
        self.rods = {'A': list(range(self.num_disks, 0, -1)), 'B': [], 'C': []}
        self.selected_rod = None
        self.move_count = 0
        self.update_gui()
        self.update_move_label()
        self.mode_label.config(text="Human", bg="lightblue")

    def update_gui(self):
        self.canvas.delete("disk")
        disk_height = 20
        for rod, disks in self.rods.items():
            x = self.rod_positions[rod]
            for i, disk in enumerate(disks):
                width = disk * 30
                y = self.rod_height - (i + 1) * (disk_height + 5)
                self.canvas.create_rectangle(x - width//2, y, x + width//2, y + disk_height,
                                             fill=self.get_disk_color(disk), tags="disk")
                self.canvas.create_text(x, y + 10, text=str(disk), fill="white", tags="disk")

    def get_disk_color(self, disk):
        colors = ["red", "green", "blue", "purple", "orange", "yellow", "pink", "cyan"]
        return colors[(disk - 1) % len(colors)]

    def on_rod_click(self, rod):
        if self.selected_rod is None:
            if not self.rods[rod]:
                return
            self.selected_rod = rod
            self.mode_label.config(text=f"Selected source: {rod}")
        else:
            source = self.selected_rod
            destination = rod
            self.selected_rod = None
            if self.is_valid_move(source, destination):
                disk = self.rods[source].pop()
                self.rods[destination].append(disk)
                self.play_sound("move")
                self.move_count += 1
                self.update_move_label()
                self.update_gui()
                self.check_win()
            else:
                self.play_sound("invalid")
                messagebox.showwarning("Invalid Move", "You can't place a larger disk on a smaller one.")
            self.mode_label.config(text="Human")

    def is_valid_move(self, source, destination):
        if not self.rods[source]:
            return False
        if not self.rods[destination]:
            return True
        return self.rods[source][-1] < self.rods[destination][-1]

    def check_win(self):
        if self.rods['C'] == list(range(self.num_disks, 0, -1)):
            self.play_sound("success")
            messagebox.showinfo("Success", f"You solved the Tower of Hanoi in {self.move_count} moves!")

    def start_Human_mode(self):
        self.selected_rod = None
        self.mode_label.config(text="Human", bg="lightblue")

    def start_aI_mode(self):
        self.selected_rod = None
        self.moves = []
        self.generate_moves(self.num_disks, 'A', 'B', 'C')
        self.mode_label.config(text="AI Mode", bg="lightgreen")
        self.animate_moves()

    def generate_moves(self, n, source, aux, dest):
        if n == 1:
            self.moves.append((source, dest))
        else:
            self.generate_moves(n-1, source, dest, aux)
            self.moves.append((source, dest))
            self.generate_moves(n-1, aux, source, dest)

    def animate_moves(self):
        if not self.moves:
            self.check_win()
            return
        source, dest = self.moves.pop(0)
        if self.is_valid_move(source, dest):
            self.rods[dest].append(self.rods[source].pop())
            self.play_sound("move")
            self.move_count += 1
            self.update_move_label()
            self.update_gui()
        self.root.after(500, self.animate_moves)

    def play_sound(self, key):
        if key in self.sounds:
            self.sounds[key].play()

    def update_move_label(self):
        self.move_label.config(text=f"Moves: {self.move_count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoiGUI(root)
    root.mainloop()
