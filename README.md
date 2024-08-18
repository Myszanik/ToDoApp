# To-Do App

This repository contains a simple To-Do application built using Python's `tkinter` library and `tkcalendar` module. The app allows users to manage tasks, set priorities, and track task completion.

## Overview

The To-Do App features a graphical user interface where users can add, remove, update, and prioritize tasks. Tasks can be categorized into active, completed, and incomplete lists. The app also includes a calendar for selecting dates.

## Features

- **Task Management**:
  - Add, remove, update, and prioritize tasks.
  - Mark tasks as completed or incomplete.
  - Clear all tasks.

- **Task Prioritization**:
  - Set priority levels (1 to 5) with different colors.

- **Calendar**:
  - Integrated calendar for selecting dates.

## Requirements

- Python 3.x
- `tkinter` (usually comes pre-installed with Python)
- `tkcalendar` (install via `pip install tkcalendar`)

## How to Run

1. **Clone this Repository**:
   ```bash
   git clone https://github.com/yourusername/todo-app.git
1. **Navigate to the Project Directory**:
   ```bash
   cd todo-app
1. **Install Dependencies**:
   ```bash
   pip install tkcalendar
1. **Run the Application**:
   ```bash
   python todo_app.py

## Code Explanation

- **`ToDoApp` Class**: Contains the main logic for the To-Do app GUI.
  - **`__init__(self, master)`**: Initializes the GUI components including the entry field, task listboxes, buttons, and calendar.
  - **`update_task_display(self)`**: Updates the task listboxes to reflect the current state of tasks.
  - **`save_tasks(self)`**: Saves tasks to a JSON file.
  - **`load_tasks(self)`**: Loads tasks from a JSON file.
  - **`on_close(self)`**: Handles the application close event, saving tasks before exiting.
  - **`create_button(self, text, row, column, frame=None, text_color='black')`**: Creates a button with specified text and color, and places it in the specified frame.
  - **`button_click(self, text)`**: Handles button clicks for various actions such as adding, removing, and updating tasks.

## Usage

- **Add Task**: Enter a task description and click "Add" to add it to the active tasks list.
- **Remove Task**: Select a task from the active tasks list and click "Remove" to delete it.
- **Complete Task**: Select a task from the active tasks list and click "Complete" to move it to the completed tasks list.
- **Incomplete Task**: Select a task from the active tasks list and click "Incomplete" to move it to the incomplete tasks list.
- **Update Task**: Select a task from the active tasks list and click "Update" to edit it.
- **Move Up/Down**: Select a task and click "Up" or "Down" to move its position in the list.
- **Set Priority**: Click "Priority" to access the priority menu and set the priority level of a selected task.
- **Clear All**: Click "Clear All" to remove all tasks from all lists.

## Acknowledgements

- **`tkinter`**: For providing a simple and easy-to-use GUI framework for Python.
- **`tkcalendar`**: For offering a flexible and customizable calendar widget, enhancing the functionality of the To-Do app.
- **`json`**: For allowing easy and efficient storage and retrieval of task data in JSON format.

## Status

**Note:** This project is still in development. Features and functionality may be subject to change, and there may be some incomplete or experimental features. Contributions and feedback are welcome!


