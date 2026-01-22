import tkinter as tk

from config import WINDOW_SIZE

def initiate_popup_panel():
    root = tk.Tk()
    root.title("Stream Panel")
    root.geometry(WINDOW_SIZE)
    root.resizable(True, True)

    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)