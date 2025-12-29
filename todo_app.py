import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
import json


class ToDoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do App")
        master.configure(bg='light slate gray')

        # Initialize task dictionary
        self.tasks = {}

        # Initialize current selected date
        self.current_date = datetime.today().strftime('%d/%m/%Y')

        # Initialize priority colors
        self.priority_colors = {
            "Priority 1": '#ff4c4c',
            "Priority 2": '#ff9c00',
            "Priority 3": '#f0e000',
            "Priority 4": '#d4e157',
            "Priority 5": '#4caf50'
        }

        # Create the entry field
        self.description = tk.Label(master, text="Type your task below to add it to your Active Tasks", width=43, justify='center', font=('Trebuchet MS', 35), fg='dark blue', bg='#faebd7')
        self.description.grid(row=0, column=0, columnspan=8, padx=50, pady=10)
        self.entry = tk.Entry(master, width=35, justify='center', font=('Arial', 40), fg='black', bg='white', insertbackground='black')
        self.entry.grid(row=1, column=0, columnspan=8, padx=5, pady=5)
        self.entry.focus_set()  # Set focus to the entry widget

        # Bind Enter key to Add button click
        self.master.bind('<Return>', self.add_task_from_entry)

        self.main_menu_frame = tk.Frame(master)
        self.main_menu_frame.grid(row=3, column=1)
        self.priority_menu_frame = tk.Frame(master)
        self.priority_menu_frame.grid(row=3, column=1)
        self.priority_menu_frame.grid_forget()

        self.description_active = tk.Label(master, text="Active Tasks", width=20, justify='left', font=('Baskerville', 35), fg='#00008B', bg='light slate gray')
        self.description_active.grid(row=2, column=0, pady=(25, 0))
        self.description_completed = tk.Label(master, text="Completed Tasks", width=15, justify='center', font=('Baskerville', 35), fg='#006400', bg='light slate gray')
        self.description_completed.grid(row=2, column=4, pady=(25, 0))
        self.description_incomplete = tk.Label(master, text="Incomplete Tasks", width=15, justify='center', font=('Baskerville', 35), fg='maroon', bg='light slate gray')
        self.description_incomplete.grid(row=2, column=5, pady=(25, 0))

        self.task_listbox_active = tk.Listbox(master, width=15, justify='left', font=('Verdana', 40), fg='black', bg='beige')
        self.task_listbox_active.grid(row=3, column=0, sticky='nsew', rowspan=15, padx=15, pady=0)
        self.task_listbox_completed = tk.Listbox(master, width=15, justify='left', font=('Verdana', 40), fg='#006400', bg='beige')
        self.task_listbox_completed.grid(row=3, column=4, sticky='nsew', rowspan=15, padx=15, pady=0)
        self.task_listbox_incomplete = tk.Listbox(master, width=15, justify='left', font=('Verdana', 40), fg='maroon', bg='beige')
        self.task_listbox_incomplete.grid(row=3, column=5, sticky='nsew', rowspan=15, padx=(0, 15), pady=0)

        self.message = tk.Label(master, text="", width=15, justify='center', font=('Arial', 30), fg='orange', bg='light slate gray')
        self.message.place(x=1125, y=25)

        self.calendar = Calendar(master, font=("Arial", 15), showweeknumbers=False, showothermonthdays=False)
        self.calendar.place(x=0, y=0, width=245, height=160)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

        self.expanded_calendar = Calendar(master, font=("Arial", 40), showweeknumbers=False, showothermonthdays=False)
        self.expanded_calendar.place(x=380, y=150, width=900, height=500)
        self.expanded_calendar.place_forget()

        self.create_button("Add", 0, 0, frame=self.main_menu_frame)
        self.create_button("Remove", 1, 0, frame=self.main_menu_frame)
        self.create_button("Update", 2, 0, frame=self.main_menu_frame)
        self.create_button("Up", 3, 0, frame=self.main_menu_frame)
        self.create_button("Down", 4, 0, frame=self.main_menu_frame)
        self.create_button("Priority", 5, 0, frame=self.main_menu_frame)
        self.create_button("Complete", 6, 0, frame=self.main_menu_frame)
        self.create_button("Incomplete", 7, 0, frame=self.main_menu_frame)
        self.create_button("Clear All", 8, 0, frame=self.main_menu_frame)

        self.create_button("", 0, 0, frame=self.priority_menu_frame)
        for i in range(1, 6):
            self.create_button(f"Priority {i}", i, 0, frame=self.priority_menu_frame, text_color=self.priority_colors[f"Priority {i}"])
        self.create_button("Back", 6, 0, frame=self.priority_menu_frame)
        self.create_button("", 7, 0, frame=self.priority_menu_frame)
        self.create_button("", 8, 0, frame=self.priority_menu_frame)

        self.load_tasks()
        self.update_task_display()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_task_from_entry(self, event=None):
        # Call the button_click method for the "Add" button
        self.button_click("Add")

    def update_date_task_display(self):
        # Fetch tasks for the formatted current date
        tasks_for_date = self.tasks.get(self.current_date, {'active': [], 'completed': [], 'incomplete': []})

        # Clear current tasks from list boxes
        self.task_listbox_active.delete(0, tk.END)
        self.task_listbox_completed.delete(0, tk.END)
        self.task_listbox_incomplete.delete(0, tk.END)

        # Display tasks for the selected date
        for task in tasks_for_date['active']:
            self.task_listbox_active.insert(tk.END, task)
        for task in tasks_for_date['completed']:
            self.task_listbox_completed.insert(tk.END, task)
        for task in tasks_for_date['incomplete']:
            self.task_listbox_incomplete.insert(tk.END, task)

    def on_date_selected(self, event):
        # Retrieve and format the date from the calendar
        selected_date = self.calendar.get_date()
        self.current_date = datetime.strptime(selected_date, '%m/%d/%Y').strftime('%m/%d/%Y')
        print(f"Selected date: {self.current_date}")  # Debug statement
        self.update_date_task_display()

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = {}

        # Ensure that the display is updated for the current date
        self.update_date_task_display()

    def on_close(self):
        self.save_tasks()
        self.master.destroy()

    def clear_message(self):
        self.message.config(text="")

    def create_button(self, text, row, column, frame=None, text_color='black'):
        button_frame = frame if frame else self.master
        button = tk.Button(button_frame, text=text, fg=text_color, width=8, height=2, font=('Arial', 25), command=lambda: self.button_click(text))
        button.grid(row=row, column=column, padx=0, pady=6)

    def button_click(self, text):
        tasks_for_date = self.tasks.setdefault(self.current_date, {'active': [], 'completed': [], 'incomplete': []})

        if text == "Add":
            result = self.entry.get()
            if result != "":
                tasks_for_date['active'].append(result)
                self.task_listbox_active.insert('end', result)
                self.entry.delete(0, tk.END)
                self.message.config(text="New task added")
                self.message.after(1500, self.clear_message)
                self.save_tasks()

        elif text == "Remove":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                index = selected_index[0]
                task = tasks_for_date['active'].pop(index)
                self.task_listbox_active.delete(index)
                self.message.config(text="Task removed")
                self.message.after(1500, self.clear_message)
                self.save_tasks()

        elif text == "Complete":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                index = selected_index[0]
                task = tasks_for_date['active'].pop(index)
                self.task_listbox_active.delete(index)
                tasks_for_date['completed'].append(task)
                self.task_listbox_completed.insert('end', task)
                self.message.config(text="Task completed")
                self.message.after(1500, self.clear_message)
                self.save_tasks()

        elif text == "Incomplete":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                index = selected_index[0]
                task = tasks_for_date['active'].pop(index)
                self.task_listbox_active.delete(index)
                tasks_for_date['incomplete'].append(task)
                self.task_listbox_incomplete.insert('end', task)
                self.message.config(text="Task incomplete")
                self.message.after(1500, self.clear_message)
                self.save_tasks()

        elif text == "Clear All":
            tasks_for_date['active'].clear()
            tasks_for_date['completed'].clear()
            tasks_for_date['incomplete'].clear()
            self.task_listbox_active.delete(0, tk.END)
            self.task_listbox_completed.delete(0, tk.END)
            self.task_listbox_incomplete.delete(0, tk.END)
            self.message.config(text="All tasks cleared")
            self.message.after(1500, self.clear_message())
            self.save_tasks()

        elif text == "Update":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                selected_text = self.task_listbox_active.get(selected_index)
                self.task_listbox_active.delete(selected_index)
                self.entry.insert('end', selected_text)

        elif text == "Down":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                index = selected_index[0]
                if index < len(self.task_listbox_active.get(0, tk.END)) - 1:
                    task = tasks_for_date['active'].pop(index)
                    tasks_for_date['active'].insert(index + 1, task)
                    self.update_date_task_display()
                    self.message.config(text="Task moved down")
                    self.message.after(1500, self.clear_message)

        elif text == "Up":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                index = selected_index[0]
                if index > 0:
                    task = tasks_for_date['active'].pop(index)
                    tasks_for_date['active'].insert(index - 1, task)
                    self.update_date_task_display()
                    self.message.config(text="Task moved up")
                    self.message.after(1500, self.clear_message)

        elif text == "Priority":
            self.main_menu_frame.grid_forget()
            self.priority_menu_frame.grid(row=3, column=1)
            self.master.update_idletasks()

        elif text == "Back":
            self.priority_menu_frame.grid_forget()
            self.main_menu_frame.grid(row=3, column=1)
            self.master.update_idletasks()

        elif text.startswith("Priority"):
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                index = selected_index[0]
                task = self.task_listbox_active.get(index)
                color = self.priority_colors.get(text, 'black')
                self.task_listbox_active.delete(index)
                self.task_listbox_active.insert(index, task)
                self.task_listbox_active.itemconfig(index, {'fg': color})
                self.message.config(text="Priority updated")
                self.message.after(1500, self.clear_message)

    def update_task_display(self):
        # Refresh task list boxes based on the current date
        self.update_date_task_display()


root = tk.Tk()
app = ToDoApp(root)
root.mainloop()
