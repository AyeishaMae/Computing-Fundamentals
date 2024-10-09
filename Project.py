# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:22:56 2024

@author: ayeng
"""

import tkinter as tk 
from tkinter import messagebox, ttk
from datetime import datetime

# Represents an individual task 
class Task:
    def __init__(self, name, description, priority, due_date, completed=False):
        self.name = name
        self.description = description 
        self.priority = priority 
        self.due_date = due_date
        self.completed = completed 
        
class TaskManager:
    def __init__(self,root):
        self.root = root 
        self.root.title("Task Manager")
        self.root.geometry("700x600")
        self.tasks = []

        # Task input fields
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()