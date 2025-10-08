# Simple To-Do List App

tasks = []

def show_menu():
    print("\n=== TO-DO LIST APP ===")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Mark Task as Done")
    print("5. Exit")

def view_tasks():
    if not tasks:
        print("No tasks yet!")
    else:
        for i, task in enumerate(tasks, start=1):
            status = "✅" if task["done"] else "❌"
            print(f"{i}. {task['title']} [{status}]")

def add_task():
    title = input("Enter task name: ")
    tasks.append({"title": title, "done": False})
    print(f"Task '{title}' added!")

def remove_task():
    view_tasks()
    try:
        task_num = int(input("Enter task number to remove: "))
        removed = tasks.pop(task_num - 1)
        print(f"Removed '{removed['title']}'")
    except (ValueError, IndexError):
        print("Invalid task number!")

def mark_done():
    view_tasks()
    try:
        task_num = int(input("Enter task number to mark done: "))
        tasks[task_num - 1]["done"] = True
        print(f"Marked '{tasks[task_num - 1]['title']}' as done!")
    except (ValueError, IndexError):
        print("Invalid task number!")

# Main loop
while True:
    show_menu()
    choice = input("Enter choice: ")

    if choice == '1':
        view_tasks()
    elif choice == '2':
        add_task()
    elif choice == '3':
        remove_task()
    elif choice == '4':
        mark_done()
    elif choice == '5':
        print("Goodbye 👋")
        break
    else:
        print("Invalid choice, try again.")
