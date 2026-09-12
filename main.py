import argparse
import json
from datetime import datetime
from pathlib import Path

# File storage location
DATA_FILE = Path.home() / ".todo_tasks.json"


def load_tasks() -> list[dict]:
    """Load tasks from the JSON file."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Could not read task file standardly ({e}). Starting fresh.")
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Save tasks list to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except OSError as e:
        print(f"Error saving tasks to file: {e}")


def get_next_id(tasks: list[dict]) -> int:
    """Calculate the next integer ID for a task."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(args):
    tasks = load_tasks()
    task = {
        "id": get_next_id(tasks),
        "title": args.title,
        "completed": False,
        "priority": args.priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: '{task['title']}' [{task['priority'].upper()}]")


def list_tasks(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Add one with 'add <title>'.")
        return

    # Filter tasks based on flags
    if args.status == "pending":
        tasks = [t for t in tasks if not t["completed"]]
    elif args.status == "completed":
        tasks = [t for t in tasks if t["completed"]]

    if not tasks:
        print(f"No {args.status} tasks found.")
        return

    print("\n--- To-Do List ---")
    for t in tasks:
        status_symbol = "[✓]" if t["completed"] else "[ ]"
        print(
            f"{t['id']}. {status_symbol} {t['title']} "
            f"({t['priority'].upper()}) - Added: {t['created_at']}"
        )
    print()


def update_task(args):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == args.id), None)

    if not task:
        print(f"Error: Task #{args.id} not found.")
        return

    if args.done is not None:
        task["completed"] = args.done
    if args.title:
        task["title"] = args.title
    if args.priority:
        task["priority"] = args.priority

    save_tasks(tasks)
    print(f"Updated task #{task['id']}.")


def delete_task(args):
    tasks = load_tasks()
    original_count = len(tasks)

    if args.clear_done:
        tasks = [t for t in tasks if not t["completed"]]
        removed = original_count - len(tasks)
        print(f"Cleared {removed} completed task(s).")
    elif args.id is not None:
        tasks = [t for t in tasks if t["id"] != args.id]
        if len(tasks) == original_count:
            print(f"Error: Task #{args.id} not found.")
            return
        print(f"Deleted task #{args.id}.")
    else:
        print("Specify a task ID with --id or use --clear-done.")
        return

    save_tasks(tasks)


def main():
    parser = argparse.ArgumentParser(
        description="CLI To-Do List - Manage your daily tasks from the terminal."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task description")
    add_parser.add_argument(
        "-p",
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Priority level (default: medium)",
    )
    add_parser.set_defaults(func=add_task)

    # Command: list
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-s",
        "--status",
        choices=["all", "pending", "completed"],
        default="all",
        help="Filter by status (default: all)",
    )
    list_parser.set_defaults(func=list_tasks)

    # Command: update
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("-t", "--title", type=str, help="New title")
    update_parser.add_argument(
        "-p", "--priority", choices=["low", "medium", "high"], help="New priority"
    )
    
    # Toggle completed status flag
    status_group = update_parser.add_mutually_exclusive_group()
    status_group.add_argument(
        "--done", dest="done", action="store_true", help="Mark as completed"
    )
    status_group.add_argument(
        "--undone", dest="done", action="store_false", help="Mark as pending"
    )
    update_parser.set_defaults(done=None, func=update_task)

    # Command: delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("--id", type=int, help="ID of task to delete")
    delete_parser.add_argument(
        "--clear-done", action="store_true", help="Remove all completed tasks"
    )
    delete_parser.set_defaults(func=delete_task)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()