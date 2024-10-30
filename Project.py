# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:43:47 2024

@author: ayeng
"""

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:46:55 2024

@author: ayeng
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:43:47 2024

@author: ayeng
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Represents an individual task
class Task:
    def __init__(self, name, description, priority, due_date, estimated_time, completed=False):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.estimated_time = estimated_time
        self.completed = completed

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("1200x1000")
        self.tasks = []

        # Create the Treeview
        self.tree = ttk.Treeview(root, columns=("Name", "Description", "Priority", "Due Date", "Estimated Time"))
        self.tree.heading("#0", text="")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Estimated Time", text="Estimated Time")
        self.tree.grid(row=6, column=0, columnspan=3, pady=(10, 5))

        # Button Frame for Add, Edit, Delete
        button_frame = tk.Frame(root)
        button_frame.grid(row=7, column=0, columnspan=3, pady=(20, 10))

        tk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=(10, 20))
        tk.Button(button_frame, text="Edit Task", command=self.edit_task).grid(row=0, column=1, padx=(20, 20))
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=(20, 10))

        # Sorting buttons on the right
        sort_frame = tk.Frame(root)
        sort_frame.grid(row=0, column=2, sticky="e", pady=(10, 5))

        tk.Button(sort_frame, text="Sort by Priority", command=self.sort_by_priority).grid(row=0, column=0, padx=5)
        tk.Button(sort_frame, text="Sort by Due Date", command=self.sort_by_due_date).grid(row=0, column=1, padx=5)

        # Task input fields
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.estimated_time_var = tk.StringVar()
        
        tk.Label(root, text="Task Name").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.name_var).grid(row=1, column=1)
        
        tk.Label(root, text="Description").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.description_var, width=50).grid(row=2, column=1)
        
        tk.Label(root, text="Priority").grid(row=3, column=0)
        self.priority_combobox = ttk.Combobox(root, textvariable=self.priority_var, values=["Low", "Medium", "High"])
        self.priority_combobox.grid(row=3, column=1)
        
        tk.Label(root, text="Due Date (YYYY-MM-DD)").grid(row=4, column=0)
        tk.Entry(root, textvariable=self.due_date_var).grid(row=4, column=1)
        
        tk.Label(root, text="Estimated Time (hours)").grid(row=5, column=0)
        tk.Entry(root, textvariable=self.estimated_time_var).grid(row=5, column=1)

        self.tree.bind("<Double-1>", self.on_item_double_click)

    def add_task(self):
        name = self.name_var.get()
        description = self.description_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()
        estimated_time = self.estimated_time_var.get()

        if not name or not description or not priority or not due_date or not estimated_time:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")  # Validate date format
        except ValueError:
            messagebox.showwarning("Input Error", "Due date must be in YYYY-MM-DD format.")
            return

        new_task = Task(name, description, priority, due_date, estimated_time)
        self.tasks.append(new_task)
        self.update_treeview()
        self.clear_fields()

    def edit_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Error", "Please select a task to edit.")
            return

        index = self.tree.index(selected_item[0])
        self.tasks[index].name = self.name_var.get()
        self.tasks[index].description = self.description_var.get()
        self.tasks[index].priority = self.priority_var.get()
        self.tasks[index].due_date = self.due_date_var.get()
        self.tasks[index].estimated_time = self.estimated_time_var.get()  # Update estimated time
        self.update_treeview()
        self.clear_fields()

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Error", "Please select a task to delete.")
            return
        
        index = self.tree.index(selected_item[0])
        self.tasks.pop(index)
        self.update_treeview()

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            self.tree.insert("", "end", values=(task.name, task.description, task.priority, task.due_date, task.estimated_time))

    def clear_fields(self):
        self.name_var.set("")
        self.description_var.set("")
        self.priority_var.set("")
        self.due_date_var.set("")
        self.estimated_time_var.set("")

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        index = self.tree.index(selected_item[0])
        task = self.tasks[index]
        self.name_var.set(task.name)
        self.description_var.set(task.description)
        self.priority_var.set(task.priority)
        self.due_date_var.set(task.due_date)
        self.estimated_time_var.set(task.estimated_time)

    def sort_by_priority(self):
        priority_order = {"Low": 0, "Medium": 1, "High": 2}
        self.tasks.sort(key=lambda task: priority_order[task.priority])
        self.update_treeview()

    def sort_by_due_date(self):
        self.tasks.sort(key=lambda task: datetime.strptime(task.due_date, "%Y-%m-%d"))
        self.update_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()  # Runs the actual UI
