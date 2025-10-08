import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x500")
root.resizable(False, False)

tasks = []

# Functions
def add_task():
    task = entry_task.get()
    if task != "":
        listbox_tasks.insert(tk.END, f"❌ {task}")
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def delete_task():
    try:
        selected_task = listbox_tasks.curselection()[0]
        listbox_tasks.delete(selected_task)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete!")

def mark_done():
    try:
        selected_task = listbox_tasks.curselection()[0]
        task_text = listbox_tasks.get(selected_task)
        if task_text.startswith("✅"):
            messagebox.showinfo("Info", "Task already marked done!")
        else:
            listbox_tasks.delete(selected_task)
            listbox_tasks.insert(selected_task, task_text.replace("❌", "✅"))
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark done!")

# UI Layout
frame_tasks = tk.Frame(root)
frame_tasks.pack(pady=20)

listbox_tasks = tk.Listbox(
    frame_tasks,
    width=45,
    height=15,
    selectbackground="#a6a6a6",
    selectmode=tk.SINGLE
)
listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.BOTH)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

entry_task = tk.Entry(root, width=40, font=('Arial', 12))
entry_task.pack(pady=10)

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="Add Task", width=12, command=add_task)
btn_add.grid(row=0, column=0, padx=5)

btn_done = tk.Button(frame_buttons, text="Mark Done", width=12, command=mark_done)
btn_done.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(frame_buttons, text="Delete Task", width=12, command=delete_task)
btn_delete.grid(row=0, column=2, padx=5)

# Run the app
root.mainloop()
