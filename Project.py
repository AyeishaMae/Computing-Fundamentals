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
        
        tk.Button(root, text="Add Task", command=self.addTask).grid(row=4,column=0, padx=5)
        tk.Button(root, text="Edit Task", command=self.editTask).grid(row=4,column=1, padx=5)
        tk.Button(root, text="Delete Task", command=self.deleteTask).grid(row=4,column=2, padx=5)
        
        self.tree = ttk.Treeview(root, columns=("Name", "Description", "Priority", "Due Date"))
        self.tree.grid(row=5, column=0, columnspan=3)
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        def addTask(self):
            name = self.name_var.get()
            description = self.description_var.get()
            priority = self.priority_var.get()
            due_date = self.due_date_var.get()

            if not name or not description or not priority or not due_date:
                messagebox.showwarning("Input Error", "All fields are required.")
                return
            
            try:
                datetime.strptime(due_date, "%Y-%m-%d")  # Validate date format
            except ValueError:
                messagebox.showwarning("Input Error", "Due date must be in YYYY-MM-DD format.")
                return

            new_task = Task(name, description, priority, due_date)
            self.tasks.append(new_task)
            self.update_treeview()
            self.clear_fields()

        def editTask(self):
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Edit Error", "Please select a task to edit.")
                return

            index = self.tree.index(selected_item[0])
            self.tasks[index].name = self.name_var.get()
            self.tasks[index].description = self.description_var.get()
            self.tasks[index].priority = self.priority_var.get()
            self.tasks[index].due_date = self.due_date_var.get()
            self.update_treeview()
            self.clear_fields()

        def deleteTask(self):
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Delete Error", "Please select a task to delete.")
                return
            
            index = self.tree.index(selected_item[0])
            self.tasks.pop(index)
            self.update_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop() #Runs the actual UI