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
        self.root.title("Task Manager") #Title of the window 
        self.root.geometry("700x600") #Creates size of the window 
        self.tasks = []

        # Task input fields
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        
        tk.Label(root, text="Task Name").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=1)
        
        tk.Label(root, text="Description").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.description_var, width=50).grid(row=1, column=1)
        
        tk.Label(root, text="Priority").grid(row=2, column=0)
        self.priority_combobox = ttk.Combobox(root, textvariable=self.priority_var, values=["Low", "Medium","High"])
        self.priority_combobox.grid(row=2, column=1)
        
        tk.Label(root, text="Due Date (YYYY-MM-DD)").grid(row=3, column=0)
        tk.Entry(root, textvariable=self.due_date_var).grid(row=3, column=1)
        
        tk.Button(root, text="Add Task", command=self.add_task).grid(row=4,column=0)
        tk.Button(root, text="Edit Task", command=self.edit_task).grid(row=4,column=1)
        tk.Button(root, text="Delete Task", command=self.delete_task).grid(row=4,column=2)
        
        self.tree = ttk.Treeview(root, columns=("Name", "Description", "Priority", "Due Date"))
        self.tree.grid(row=5, column=0, columnspan=3)
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        
        self.tree.bind("<Double-1>", self.on_item_double_click)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop() #Runs the actual UI