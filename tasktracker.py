import argparse
import json
import os
import sys
from datetime import datetime

FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return []

def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def cmd_add(args):
    # take disc
    description = args.add

    #load tasks
    tasks = load_tasks()

    #generate id
    if not tasks:
        new_id = 1
    else:
        new_id = max(task["id"] for task in tasks) + 1

    #create task
    now = datetime.now()
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now.strftime("%d.%m.%Y %H:%M:%S"),
        "updatedAt": now.strftime("%d.%m.%Y %H:%M:%S"),
    }

    #add and save
    tasks.append(new_task)
    save_tasks(tasks)

def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found")
        return

    if args.status:
        tasks = [t for t in tasks if t["status"] == args.status]

    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"{task['id']}. [{task['status']}] {task['description']}. Last time updated: {task['updatedAt']}")

def cmd_update(args):
    task_id = args.id
    new_description = args.description
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            save_tasks(tasks)
            print(f"Task with ID {task_id} updated")
            return
    print(f"Task with ID {task_id} not found")

def cmd_delete(args):
    task_id = int(args.delete)
    tasks = load_tasks()

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            save_tasks(tasks)
            print(f"Task {task_id} deleted")
            return

    print(f"Task with ID {task_id} not found")

def mark_status(task_id, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            save_tasks(tasks)
            print(f"Task with ID {task_id} updated")
            return
    print(f"Task with ID {task_id} not found")

def cmd_mark_in_progress(args):
    mark_status(args.id, "in-progress")

def cmd_mark_done(args):
    mark_status(args.id, "done")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    #command add
    p_add = subparsers.add_parser("add", help="add a new task")
    p_add.add_argument("add", type=str, help="name of the task")
    p_add.set_defaults(func=cmd_add)

    #command update
    p_update = subparsers.add_parser("update", help="update a task")
    p_update.add_argument("id", type=int, help="ID of the task")
    p_update.add_argument("description", type=str, help="description of the task")
    p_update.set_defaults(func=cmd_update)

    #command delete
    p_delete = subparsers.add_parser("delete", help="delete a task")
    p_delete.add_argument("delete", type=int, help="ID of the task to delete")
    p_delete.set_defaults(func=cmd_delete)

    #command list
    p_list = subparsers.add_parser("list", help="list all tasks")
    p_list.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"], help="filter by status")
    p_list.set_defaults(func=cmd_list)

    #status in-progress
    p_progress = subparsers.add_parser("mark-in-progress", help="mark task in progress")
    p_progress.add_argument("id", type=int)
    p_progress.set_defaults(func=cmd_mark_in_progress)

    #status done
    p_done = subparsers.add_parser("mark-done", help="mark task as done")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=cmd_mark_done)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    main()