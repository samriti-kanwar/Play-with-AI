import tkinter as tk
from tkinter import ttk
import subprocess

def launch_hanoi():
    subprocess.Popen(["python", "tower_of_hanoi.py"])

def launch_puzzle():
    subprocess.Popen(["python", "puzzle_problem.py"])

def launch_maze():
    subprocess.Popen(["python", "maze_pathfinding.py"])

root = tk.Tk()
root.title("🧠 AI Puzzle Game Hub")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#2c3e50")    #dark blue-gray

#  Title
title = tk.Label(root, text="🧠 AI Puzzle Game Hub", font=("Helvetica", 24, "bold"),
                 bg="#2c3e50", fg="white")
title.pack(pady=30)

# Button
def create_button(text, command, bg, fg):
    return tk.Button(
        root,
        text=text,
        command=command,
        width=25,
        height=2,
        font=("Helvetica", 14),
        bg=bg,
        fg=fg,
        activebackground=fg,
        activeforeground=bg,
        relief="flat",
        cursor="hand2"
    )

# Buttons
btn_hanoi = create_button("🎯 Tower of Hanoi", launch_hanoi, "#1abc9c", "white")
btn_hanoi.pack(pady=10)

btn_puzzle = create_button("🧩 Puzzle Problem", launch_puzzle, "#3498db", "white")
btn_puzzle.pack(pady=10)

btn_maze = create_button("🗺️ Maze Pathfinding", launch_maze, "#e67e22", "white")
btn_maze.pack(pady=10)


footer = tk.Label(root, text="@ samriti kanwar Puzzle AI games", font=("Helvetica", 10),
                  bg="#2c3e50", fg="#bdc3c7")
footer.pack(side="bottom", pady=10)

# Run app
root.mainloop()
