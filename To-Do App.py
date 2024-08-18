import tkinter as tk
from tkcalendar import Calendar
import json
class ToDoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do App")
        master.configure(bg='light slate gray')

        # Initialize task lists
        self.tasks_active = []
        self.tasks_completed = []
        self.tasks_incomplete = []

        self.priority1 = '#ff4c4c'
        self.priority2 = '#ff9c00'
        self.priority3 = '#f0e000'
        self.priority4 = '#d4e157'
        self.priority5 = '#4caf50'

        # Create the entry field
        self.description = tk.Label(master, text="Type your task below to add it to your active tasks", width=42, justify='center', font=('Garamond', 55), fg='darkblue', bg='#faebd7')
        self.description.grid(row=0, column=0, columnspan=8, padx=50, pady=10)
        self.entry = tk.Entry(master, width=50, justify='center', font=('Arial', 40), fg='black', bg='white', insertbackground='black')
        self.entry.grid(row=1, column=0, columnspan=8, padx=5, pady=5)
        self.main_menu_frame = tk.Frame(master)
        self.main_menu_frame.grid(row=3, column=1)
        self.priority_menu_frame = tk.Frame(master)
        self.priority_menu_frame.grid(row=3, column=1)
        self.priority_menu_frame.grid_forget()
        self.description_active = tk.Label(master, text="Active Tasks", width=30, justify='left', font=('Baskerville', 40), fg='#00008B', bg='light slate gray')
        self.description_active.grid(row=2, column=0)
        self.description_completed = tk.Label(master, text="Completed Tasks", width=15, justify='center', font=('Baskerville', 40), fg='#006400', bg='light slate gray')
        self.description_completed.grid(row=2, column=4)
        self.description_incomplete = tk.Label(master, text="Incomplete Tasks", width=15, justify='center', font=('Baskerville', 40), fg='maroon', bg='light slate gray')
        self.description_incomplete.grid(row=2, column=5)
        self.task_listbox_active = tk.Listbox(master, width=25, justify='left', font=('Verdana', 40), fg='black', bg='beige')
        self.task_listbox_active.grid(row=3, column=0, sticky='nsew', rowspan=15, padx=15, pady=5)
        self.task_listbox_completed = tk.Listbox(master, width=15, justify='left', font=('Verdana', 40), fg='#006400', bg='beige')
        self.task_listbox_completed.grid(row=3, column=4, sticky='nsew', rowspan=15, padx=15, pady=5)
        self.task_listbox_incomplete = tk.Listbox(master, width=15, justify='left', font=('Verdana', 40), fg='maroon', bg='beige')
        self.task_listbox_incomplete.grid(row=3, column=5, sticky='nsew', rowspan=15, padx=(0, 15), pady=5)
        self.message = tk.Label(master, text="", width=15, justify='center', font=('Arial', 30), fg='orange', bg='light slate gray')
        self.message.place(x=1390, y=25)
        self.calendar = Calendar(master, font=("Arial", 15), showweeknumbers=False, showothermonthdays=False)
        self.calendar.place(x=0, y=0, width=245, height=160)
        self.expanded_calendar = Calendar(master, font=("Arial", 40), showweeknumbers=False, showothermonthdays=False)
        self.expanded_calendar.place(x=380, y=150, width=900, height=500)
        self.expanded_calendar.place_forget()
        # self.expand_button = tk.Button(master, width=10, text='Expand Calendar', command=self.expand_calendar)
        # self.expand_button.place(x=0, y=135)
        # self.collapse_button = tk.Button(master, width=10, text='Collapse Calendar', command=self.collapse_calendar)
        # self.collapse_button.place(x=0, y=160)

        # Create the buttons
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
        self.create_button("Priority 1", 1, 0, frame=self.priority_menu_frame, text_color='#ff4c4c')
        self.create_button("Priority 2", 2, 0, frame=self.priority_menu_frame, text_color='#ff9c00')
        self.create_button("Priority 3", 3, 0, frame=self.priority_menu_frame, text_color='#f0e000')
        self.create_button("Priority 4", 4, 0, frame=self.priority_menu_frame, text_color='#d4e157')
        self.create_button("Priority 5", 5, 0, frame=self.priority_menu_frame, text_color='#4caf50')
        self.create_button("Back", 6, 0, frame=self.priority_menu_frame)
        self.create_button("", 7, 0, frame=self.priority_menu_frame)
        self.create_button("", 8, 0, frame=self.priority_menu_frame)

        # Load tasks from file
        self.load_tasks()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_task_display(self):
        self.task_listbox_active.delete(0, tk.END)
        self.task_listbox_completed.delete(0, tk.END)
        self.task_listbox_incomplete.delete(0, tk.END)

        for task in self.tasks_active:
            self.task_listbox_active.insert(tk.END, task)

        for task in self.tasks_completed:
            self.task_listbox_completed.insert(tk.END, task)

        for task in self.tasks_incomplete:
            self.task_listbox_incomplete.insert(tk.END, task)

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump({
                'active': self.tasks_active,
                'completed': self.tasks_completed,
                'incomplete': self.tasks_incomplete
            }, file, indent=4)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                data = json.load(file)
                self.tasks_active = data.get('active', [])
                self.tasks_completed = data.get('completed', [])
                self.tasks_incomplete = data.get('incomplete', [])
                self.update_task_display()
        except (FileNotFoundError, json.JSONDecodeError):
            # If file is not found or can't be decoded, initialize empty lists
            self.tasks_active = []
            self.tasks_completed = []
            self.tasks_incomplete = []

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
        if text == "Add":
            result = self.entry.get()
            if result != "":
                self.tasks_active.append(result)
                self.task_listbox_active.insert('end', result)
                self.entry.delete(0, tk.END)
                self.message.config(text="New task added")
                self.message.after(1500, self.clear_message)
                self.save_tasks()
        if text == "Remove":
            selected_index = self.task_listbox_active.curselection()  # Get the selected index (tuple)
            if selected_index:  # Check if there's any selection
                index = selected_index[0]  # Extract the index
                del self.tasks_active[index]  # Remove the item from the tasks_active list
                self.task_listbox_active.delete(index)  # Extract and use the index
                self.message.config(text="Task removed")
                self.message.after(1500, self.clear_message)
                self.save_tasks()
        if text == "Complete":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                selected_index = selected_index[0]
                selected_text = self.task_listbox_active.get(selected_index)

                if selected_text:
                    # Remove from active list and listbox
                    del self.tasks_active[selected_index]
                    self.task_listbox_active.delete(selected_index)

                    # Add to completed list and listbox
                    self.tasks_completed.append(selected_text)
                    self.task_listbox_completed.insert('end', selected_text)

                    # Provide feedback and save
                    self.message.config(text="Task completed")
                    self.message.after(1500, self.clear_message)
                    self.save_tasks()
        if text == "Incomplete":
            selected_index = self.task_listbox_active.curselection()
            if selected_index:
                selected_index = selected_index[0]
                selected_text = self.task_listbox_active.get(selected_index)

                if selected_text:
                    # Remove from active list and listbox
                    del self.tasks_active[selected_index]
                    self.task_listbox_active.delete(selected_index)

                    # Add to incomplete list and listbox
                    self.tasks_incomplete.append(selected_text)
                    self.task_listbox_incomplete.insert('end', selected_text)

                    # Provide feedback and save
                    self.message.config(text="Task incomplete")
                    self.message.after(1500, self.clear_message)
                    self.save_tasks()
        if text == "Clear All":
            self.tasks_active = []
            self.tasks_completed = []
            self.tasks_incomplete = []
            self.task_listbox_active.delete(0, tk.END)
            self.task_listbox_completed.delete(0, tk.END)
            self.task_listbox_incomplete.delete(0, tk.END)
            self.message.config(text="All tasks cleared")
            self.message.after(1500, self.clear_message)
            self.save_tasks()
        if text == "Update":
            selected_index = self.task_listbox_active.curselection()
            selected_text = self.task_listbox_active.get(selected_index)
            if selected_text:
                self.task_listbox_active.delete(selected_index)
                self.entry.insert('end', selected_text)
        if text == "Down":
            selected_index = self.task_listbox_active.curselection()[0]
            selected_text = self.task_listbox_active.get(selected_index)
            total_items = self.task_listbox_active.size()
            if selected_index < total_items - 1:
                self.task_listbox_active.delete(selected_index)
                self.task_listbox_active.insert(selected_index + 1, selected_text)
                self.message.config(text="Task moved down")
                self.message.after(1500, self.clear_message)
        if text == "Up":
            selected_index = self.task_listbox_active.curselection()[0]
            selected_text = self.task_listbox_active.get(selected_index)
            if selected_index > 0:
                self.task_listbox_active.delete(selected_index)
                self.task_listbox_active.insert(selected_index - 1, selected_text)
                self.message.config(text="Task moved up")
                self.message.after(1500, self.clear_message)
        if text == "Priority":
            self.main_menu_frame.grid_forget()
            self.priority_menu_frame.grid(row=3, column=1)
            self.master.update_idletasks()
        if text == "Back":
            self.priority_menu_frame.grid_forget()
            self.main_menu_frame.grid(row=3, column=1)
            self.master.update_idletasks()
        if text == "Priority 1":
            selected_index = self.task_listbox_active.curselection()[0]
            selected_text = self.task_listbox_active.get(selected_index)
            if selected_text:
                self.task_listbox_active.delete(selected_index)
                self.task_listbox_active.insert(selected_index, selected_text)
                self.task_listbox_active.itemconfig(selected_index, {'fg':self.priority1})
                self.message.config(text="Priority updated")
                self.message.after(1500, self.clear_message)
        if text == "Priority 2":
            selected_index = self.task_listbox_active.curselection()[0]
            selected_text = self.task_listbox_active.get(selected_index)
            if selected_text:
                self.task_listbox_active.delete(selected_index)
                self.task_listbox_active.insert(selected_index, selected_text)
                self.task_listbox_active.itemconfig(selected_index, {'fg':self.priority2})
                self.message.config(text="Priority updated")
                self.message.after(1500, self.clear_message)
        if text == "Priority 3":
            selected_index = self.task_listbox_active.curselection()[0]
            selected_text = self.task_listbox_active.get(selected_index)
            if selected_text:
                self.task_listbox_active.delete(selected_index)
                self.task_listbox_active.insert(selected_index, selected_text)
                self.task_listbox_active.itemconfig(selected_index, {'fg':self.priority3})
                self.message.config(text="Priority updated")
                self.message.after(1500, self.clear_message)
        if text == "Priority 4":
            selected_index = self.task_listbox_active.curselection()[0]
            selected_text = self.task_listbox_active.get(selected_index)
            if selected_text:
                self.task_listbox_active.delete(selected_index)
                self.task_listbox_active.insert(selected_index, selected_text)
                self.task_listbox_active.itemconfig(selected_index, {'fg':self.priority4})
                self.message.config(text="Priority updated")
                self.message.after(1500, self.clear_message)
        if text == "Priority 5":
            selected_index = self.task_listbox_active.curselection()[0]
            selected_text = self.task_listbox_active.get(selected_index)
            if selected_text:
                self.task_listbox_active.delete(selected_index)
                self.task_listbox_active.insert(selected_index, selected_text)
                self.task_listbox_active.itemconfig(selected_index, {'fg':self.priority5})
                self.message.config(text="Priority updated")
                self.message.after(1500, self.clear_message)

root = tk.Tk()
ToDoApp = ToDoApp(root)
root.mainloop()