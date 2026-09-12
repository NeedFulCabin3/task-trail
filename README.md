# Task Trail

> Command-line task persistence engine built around zero-dependency state files and argparse execution loops.

## Overview / Value Proposition

Switching contexts to record micro-tasks breaks development focus. Many task management utilities demand backend databases, network connectivity, or heavy runtime setups. `task-trail` addresses this operational friction by exposing a fast, local command-line interface that serializes task states directly into standard JSON storage located in the user's home path (`~/.todo_tasks.json`).

## Under the Hood / How It Works

`task-trail` uses standard input evaluation pipelines to manage task states:
```text
[CLI Entry Point] ──> [argparse Subparsers] ──> [JSON File I/O] ──> [User Home Path Storage]
│
[State Mutation]
(Filter, Update, Mass Clear)
```

1. **Command Routing**: `argparse` subparsers inspect command arguments (`add`, `list`, `update`, `delete`) and route control to distinct function handlers via standard callbacks (`func` defaults).
2. **Persistence State Machine**: State reads and writes flow through `load_tasks()` and `save_tasks()`. Reading handles parsing failures gracefully by falling back to empty states when corrupt data or missing files are encountered.
3. **Auto-Increment Strategy**: New task identifiers calculate max existing integer keys incremented by step 1, ensuring non-colliding numeric IDs across sessions.
4. **Mutually Exclusive Mutators**: State toggles (`--done` / `--undone`) use mutually exclusive groups to prevent conflicting boolean states during updates.

## Key Features

- **Isolated Subcommand Engine**: Distinct command parsers isolate positional and optional arguments per operation.
- **Selective Filtering**: Filter task lists by `pending`, `completed`, or `all` states without modifying target JSON payloads.
- **Batch Clearance**: Purge all completed entries in a single pass using the `--clear-done` execution flag.
- **Resilient File Access**: Input/output operations isolate `json.JSONDecodeError` and `OSError` boundaries to protect execution continuity.

## Tech Stack & Core Dependencies Breakdown

- **Python Target**: Python 3.10+
- **Standard Library Components**:
  - `argparse`: Handles terminal flag parsing, subcommand definitions, and help formatting.
  - `json`: Serializes internal dictionary lists to disk.
  - `pathlib.Path`: Offers cross-platform path resolution targeting user home directories[cite: 1].
  - `datetime`: Generates formatted timestamp strings (`YYYY-MM-DD HH:MM`) upon record creation[cite: 1].

## Environment & Web-Based Quick Start

### Launch in GitHub Codespaces

1. Click **Code** -> **Codespaces** -> **Create codespace on main**.
2. Once the web container boots, execute commands directly in the embedded terminal.

### Local Virtual Environment Setup

```bash
### Clone repository
git clone [https://github.com/your-username/task-trail.git](https://github.com/your-username/task-trail.git)
cd task-trail

### Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

### Run utility
python main.py --help
```

## Usage Example

# Add tasks with explicit priorities
python main.py add "Write technical documentation" -p high

# List only pending tasks
python main.py list -s pending

# Mark a task complete by ID
python main.py update 1 --done

# Purge completed tasks
python main.py delete --clear-done

## Repository Structure
```text
task-trail/
├── .github/
│   └── workflows/
│       └── ci.yml        # Automation pipelines for quality checks
├── .gitignore            # Rules for ignoring dynamic artifacts
├── LICENSE               # MIT License file
├── README.md             # Repository documentation
└── main.py               # Core CLI entry point and task management engine
```

## Roadmap

[] **Task Categories/Tags:** Extend JSON schemas to allow multi-tag metadata filtering.

[] **Structural Logging Output:** Add --json output flags across all commands for pipeline piping into tools like jq.

[] **Custom Storage File Configuration:** Allow overriding ~/.todo_tasks.json via an environment variable (TASK_TRAIL_PATH).

[] **Async I/O Processing:** Migrate storage routines to aiofiles if supporting concurrent CLI operations across multiple terminal multiplexer sessions.
