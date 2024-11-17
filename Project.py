# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 09:01:25 2024

@author: ayeng
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Represents an individual task
class Task:
    def __init__(self, name, description, priority, due_date, estimated_time, completed=False):
        # Initialize task with provided attributes
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.estimated_time = estimated_time
        self.completed = completed  # Default value for completion status is False

# Main task manager application class
class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")  # Set window title
        self.root.geometry("1200x1000")  # Set window size
        self.root.configure(bg="lightblue")  # Set background color
        self.tasks = []  # List to hold tasks
        self.task_counter = 0  # Initialize task counter
        
        # Define custom fonts for UI
        custom_font = ("Verdana", 13)
        custom_fontb = ("Verdana", 24)
        self.header_font = ("Verdana", 13)
        self.cell_font = ("Verdana", 9)

        # Configure Treeview style
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=self.header_font, foreground="navy")
        self.style.configure("Treeview", font=self.cell_font)

        # Create Treeview widget to display tasks
        self.tree = ttk.Treeview(root,selectmode="extended", columns=("Name", "Description", "Priority", "Due Date", "Estimated Time", "Completed"))
        self.tree.heading("#0", text="")  # First column is hidden
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide the extra column
        self.tree.heading("Name", text="Name")  # Define the column headings
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Estimated Time", text="Estimated Time")
        self.tree.heading("Completed", text="Completed")
        
        self.tree.grid(row=6, column=0, columnspan=3, pady=(10, 5))  # Place the Treeview in the grid

        # Scrollbar for Treeview
        self.tree_scroll = tk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)  # Link the scrollbar to the Treeview
        self.tree_scroll.grid(row=6, column=3, sticky="ns", pady=(10, 5))  # Place scrollbar on the right

        # Button Frame for Add, Edit, Delete
        button_frame = tk.Frame(root, bg="lightblue")
        button_frame.grid(row=7, column=0, columnspan=3, pady=(20, 10))

        # Buttons for adding, editing, deleting, and marking completion of tasks
        tk.Button(button_frame, text="Add Task", command=self.add_task, fg="navyblue", bg="lightblue", highlightbackground="lightblue", font=custom_font).grid(row=0, column=0, padx=(10, 20))
        tk.Button(button_frame, text="Edit Task", command=self.edit_task, fg="navyblue", bg="lightblue", highlightbackground="lightblue", font=custom_font).grid(row=0, column=1, padx=(20, 20))
        tk.Button(button_frame, text="Delete Task", command=self.delete_task, fg="navyblue", bg="lightblue", highlightbackground="lightblue", font=custom_font).grid(row=0, column=2, padx=(20, 10))

        # Label to display total task times
        self.selected_tasks_time_label = tk.Label(root, text="Total Estimated Time : 0 hours", fg="white", bg="lightblue", font=custom_font)
        self.selected_tasks_time_label.grid(row=8, column=0, columnspan=3, pady=(10, 5))

        # Sorting buttons on the right
        sort_frame = tk.Frame(root, bg="lightblue")
        sort_frame.grid(row=0, column=2, sticky="e", pady=(10, 5))

        # Buttons for sorting tasks by priority or due date
        tk.Button(sort_frame, text="Sort by Priority", command=self.sort_by_priority, fg="navyblue", bg="lightblue", highlightbackground="lightblue", font=custom_font).grid(row=0, column=0, padx=5)
        tk.Button(sort_frame, text="Sort by Due Date", command=self.sort_by_due_date, fg="navyblue", bg="lightblue", highlightbackground="lightblue", font=custom_font).grid(row=0, column=1, padx=5)

        # Task input fields
        self.name_var = tk.StringVar()  # Variable for Task Name
        self.description_var = tk.StringVar()  # Variable for Task Description
        self.priority_var = tk.StringVar()  # Variable for Task Priority
        self.due_date_var = tk.StringVar()  # Variable for Task Due Date
        self.estimated_time_var = tk.StringVar()  # Variable for Task Estimated Time

        # Labels and entry fields for task details
        tk.Label(root, text="Task Manager", fg="white", bg="lightblue", font=custom_fontb).grid(row=0, column=1, sticky="n", padx=10)
        tk.Label(root, text="Task Name", fg="white", bg="lightblue", font=custom_font).grid(row=1, column=0)
        tk.Entry(root, textvariable=self.name_var, highlightbackground="lightblue").grid(row=1, column=1)

        tk.Label(root, text="Description", fg="white", bg="lightblue", font=custom_font).grid(row=2, column=0)
        tk.Entry(root, textvariable=self.description_var, width=50, highlightbackground="lightblue").grid(row=2, column=1)

        tk.Label(root, text="Priority", fg="white", bg="lightblue", font=custom_font).grid(row=3, column=0)
        self.priority_combobox = ttk.Combobox(root, textvariable=self.priority_var, values=["Low", "Medium", "High"])  # Combobox for priority
        self.priority_combobox.grid(row=3, column=1)

        tk.Label(root, text="Due Date (YYYY-MM-DD)", fg="white", bg="lightblue", font=custom_font).grid(row=4, column=0)
        tk.Entry(root, textvariable=self.due_date_var, highlightbackground="lightblue").grid(row=4, column=1)

        tk.Label(root, text="Estimated Time (hours)", fg="white", bg="lightblue", font=custom_font).grid(row=5, column=0)
        tk.Entry(root, textvariable=self.estimated_time_var, highlightbackground="lightblue").grid(row=5, column=1)

        # Label to display task count
        self.task_count_label = tk.Label(root, text=f"Total Tasks: {self.task_counter}", fg="white", bg="lightblue", font=custom_font)
        self.task_count_label.grid(row=0, column=0, sticky="w", padx=(10, 5))

        # Button to mark tasks as completed
        tk.Button(button_frame, text="Mark as Completed", command=self.toggle_completed, fg="navyblue", bg="lightblue", highlightbackground="lightblue", font=custom_font).grid(row=0, column=3, padx=(20, 10))

        # Bind double-click for editing task
        self.tree.bind("<Double-1>", self.on_item_double_click)


    # Add a new task to the list
    def add_task(self):
        name = self.name_var.get()
        description = self.description_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()
        estimated_time = self.estimated_time_var.get()

        # Check if any field is empty
        if not name or not description or not priority or not due_date or not estimated_time:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        # Validate due date format (YYYY-MM-DD)
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Due date must be in YYYY-MM-DD format.")
            return

        # Validate estimated time (ensure it's a valid number)
        try:
            float(estimated_time)  # Check if it's a valid number
        except ValueError:
            messagebox.showwarning("Input Error", "Estimated time must be a valid number.")
            return

        # Create a new Task object and add it to the task list
        new_task = Task(name, description, priority, due_date, estimated_time)
        self.tasks.append(new_task)
        
        # Increment the task counter
        self.task_counter += 1
        
        # Update the task count label
        self.task_count_label.config(text=f"Total Tasks: {self.task_counter}")
        
        self.update_treeview()  # Update the Treeview display
        self.clear_fields()  # Clear the input fields for the next task
        self.update_total_time() # Update the total time
    # Edit an existing task
    def edit_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Error", "Please select a task to edit.")
            return

        # Get the selected task's index and update its attributes
        index = self.tree.index(selected_item[0])
        self.tasks[index].name = self.name_var.get()
        self.tasks[index].description = self.description_var.get()
        self.tasks[index].priority = self.priority_var.get()
        self.tasks[index].due_date = self.due_date_var.get()
        self.tasks[index].estimated_time = self.estimated_time_var.get()  # Update estimated time
        self.update_treeview()  # Update the Treeview
        self.clear_fields()  # Clear the input fields
        self.update_total_time() # Update the total time
    # Delete a selected task
    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Error", "Please select a task to delete.")
            return

        # Get the selected task's index and remove it from the list
        index = self.tree.index(selected_item[0])
        self.tasks.pop(index)
        
        # Decrement the task counter
        self.task_counter -= 1
        
        # Update the task count label
        self.task_count_label.config(text=f"Total Tasks: {self.task_counter}")
        
        self.update_treeview()  # Update the Treeview after deletion
        self.update_total_time() # Update the total time
    # Update the Treeview with the current task list
    def update_treeview(self):
        # Clear the Treeview and add all tasks back
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            completed_state = "Yes" if task.completed else "No"  # Display completion status
            self.tree.insert("", "end", values=(task.name, task.description, task.priority, task.due_date, task.estimated_time, completed_state))

    # Clear all input fields
    def clear_fields(self):
        self.name_var.set("")
        self.description_var.set("")
        self.priority_var.set("")
        self.due_date_var.set("")
        self.estimated_time_var.set("")

    # Toggle the completion status of a task
    def toggle_completed(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Toggle Error", "Please select a task to mark as completed.")
            return

        # Get the selected task's index and toggle its completion status
        index = self.tree.index(selected_item[0])
        task = self.tasks[index]
        task.completed = not task.completed  # Toggle the completion status
        self.update_treeview()  # Update the Treeview

    # Handle double-click to edit a task's details
    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        # Get the selected task's index and populate the input fields
        index = self.tree.index(selected_item[0])
        task = self.tasks[index]
        self.name_var.set(task.name)
        self.description_var.set(task.description)
        self.priority_var.set(task.priority)
        self.due_date_var.set(task.due_date)
        self.estimated_time_var.set(task.estimated_time)

    # Sort tasks by priority (Low, Medium, High)
    def sort_by_priority(self):
        priority_order = {"Low": 0, "Medium": 1, "High": 2}  # Priority order mapping
        self.tasks.sort(key=lambda task: priority_order[task.priority])  # Sort tasks by priority
        self.update_treeview()  # Update the Treeview after sorting

    # Sort tasks by due date
    def sort_by_due_date(self):
        self.tasks.sort(key=lambda task: datetime.strptime(task.due_date, "%Y-%m-%d"))  # Convert date string to datetime for sorting
        self.update_treeview()  # Update the Treeview after sorting
        
    # Sum up the total of the tasks as they're being added
    def update_total_time(self):
        total_time = sum(float(task.estimated_time) for task in self.tasks)  # Sum up the time
        self.selected_tasks_time_label.config(text=f"Total Estimated Time: {total_time} hours")
    

# Main code to run the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = TaskManager(root)  # Initialize the TaskManager application
    root.mainloop()  # Start the Tkinter event loop
