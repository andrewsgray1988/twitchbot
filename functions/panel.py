import tkinter as tk
import threading

from config import WINDOW_SIZE
from functions.general import start_tasks

def start_panel(loop):
    def run():
        root = tk.Tk()
        root.title("Stream Panel")
        root.geometry(WINDOW_SIZE)
        root.resizable(True, True)

        container = tk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def start_tasks_button():
            loop.call_soon_threadsafe(start_tasks)

        tk.Button(container, text="Stream Started", command=start_tasks_button).pack()

        root.mainloop()

    threading.Thread(target=run, daemon=True).start()