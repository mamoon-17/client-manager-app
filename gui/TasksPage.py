import customtkinter as ctk
from customtkinter import CTkFont
from tkinter import messagebox
from datetime import datetime, date


class TasksPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)
        self.__root = root
        self.__db = db
        self.__cursor = db.get_cursor()
        self.controller = None

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__FONT = CTkFont(family="Raleway", size=15)

        self.__tasks = []

        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color=self.__FRAME_COLOR)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.init_title()
        self.init_filters()
        self.init_task_list()
        self.refresh_tasks()

    def init_title(self):
        title_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        title_frame.grid(row=0, column=0, sticky="ew", padx=80, pady=(50, 10))
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=0)

        title = ctk.CTkLabel(title_frame, text="Task List", font=CTkFont(size=32, weight="bold"))
        title.grid(row=0, column=0, sticky="w")

        add_btn = ctk.CTkButton(title_frame, text="Add Task", command=self.open_add_task_dialog,
                                fg_color="#4a9eff", hover_color="#3d8bdb", font=self.__FONT)
        add_btn.grid(row=0, column=1, padx=(10, 0), sticky="e")

    def init_filters(self):
        filter_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=80, pady=(10, 5))
        filter_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.filter_priority = ctk.StringVar(value="All")
        self.filter_starred = ctk.BooleanVar(value=False)
        self.filter_completed = ctk.BooleanVar(value=False)

        ctk.CTkOptionMenu(filter_frame, variable=self.filter_priority, values=["All", "Low", "Medium", "High"],
                          command=lambda _: self.refresh_tasks(), fg_color=self.__WIDGET_COLOR).grid(row=0, column=0, padx=10)

        ctk.CTkCheckBox(filter_frame, text="Show Starred", variable=self.filter_starred,
                        command=self.refresh_tasks).grid(row=0, column=1)

        ctk.CTkCheckBox(filter_frame, text="Show Completed", variable=self.filter_completed,
                        command=self.refresh_tasks).grid(row=0, column=2)

    def init_task_list(self):
        self.tasks_container = ctk.CTkScrollableFrame(self, fg_color=self.__FRAME_COLOR)
        self.tasks_container.grid(row=2, column=0, sticky="nsew", padx=80, pady=10)
        self.tasks_container.columnconfigure(0, weight=1)

    def refresh_tasks(self):
        for widget in self.tasks_container.winfo_children():
            widget.destroy()

        query = "SELECT task_id, title, priority, deadline, is_starred, is_completed FROM tasks"
        filters = []
        params = []

        if self.filter_priority.get() != "All":
            filters.append("priority = %s")
            params.append(self.filter_priority.get())

        if self.filter_starred.get():
            filters.append("is_starred = 1")

        if self.filter_completed.get():
            filters.append("is_completed = 1")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY deadline ASC"

        try:
            self.__cursor.execute(query, tuple(params))
            self.__tasks = self.__cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch tasks: {str(e)}")
            self.__tasks = []

        for i, (task_id, title, priority, deadline, is_starred, is_completed) in enumerate(self.__tasks):
            frame = ctk.CTkFrame(self.tasks_container, fg_color=self.__WIDGET_COLOR, corner_radius=10)
            frame.grid(row=i, column=0, sticky="ew", padx=10, pady=8)

            status = "✅" if is_completed else "🔲"
            star = "⭐" if is_starred else "☆"
            label = ctk.CTkLabel(frame, text=f"{status} {title} | {priority} | Due: {deadline}", font=self.__FONT)
            label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

            star_btn = ctk.CTkButton(frame, text=star, width=40,
                                     command=lambda t_id=task_id, s=not is_starred: self.toggle_star(t_id, s))
            star_btn.grid(row=0, column=1, padx=5)

            complete_btn = ctk.CTkButton(frame, text="✓" if not is_completed else "Undo", width=60,
                                         command=lambda t_id=task_id, c=not is_completed: self.toggle_complete(t_id, c))
            complete_btn.grid(row=0, column=2, padx=5)

            delete_btn = ctk.CTkButton(frame, text="🗑", fg_color="red", width=40,
                                       command=lambda t_id=task_id: self.delete_task(t_id))
            delete_btn.grid(row=0, column=3, padx=5)

    def open_add_task_dialog(self):
        dialog = ctk.CTkInputDialog(title="Add Task", text="Enter Task Title:")
        title = dialog.get_input()
        if not title:
            return

        # Priority input (case-insensitive)
        priority_input = ctk.CTkInputDialog(title="Priority", text="Priority (Low/Medium/High):").get_input()
        if not priority_input:
            return
        priority = priority_input.capitalize()

        if priority not in ["Low", "Medium", "High"]:
            messagebox.showerror("Invalid", "Priority must be Low, Medium, or High.")
            return

        deadline = ctk.CTkInputDialog(title="Deadline", text="Deadline (YYYY-MM-DD):").get_input()
        if not self.validate_date(deadline):
            messagebox.showerror("Invalid", "Invalid or past deadline.")
            return

        try:
            self.__cursor.execute("INSERT INTO tasks (title, priority, deadline) VALUES (%s, %s, %s)",
                                  (title, priority, deadline))
            self.__db.commit()
            self.refresh_tasks()
        except Exception as e:
            print(f"[ERROR] Add task failed: {e}")
            messagebox.showerror("Error", "Failed to add task.")

    def delete_task(self, task_id):
        try:
            self.__cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
            self.__db.commit()
            self.refresh_tasks()
        except Exception as e:
            print(f"[ERROR] Delete task: {e}")

    def toggle_star(self, task_id, new_state):
        try:
            self.__cursor.execute("UPDATE tasks SET is_starred = %s WHERE task_id = %s", (new_state, task_id))
            self.__db.commit()
            self.refresh_tasks()
        except Exception as e:
            print(f"[ERROR] Star toggle: {e}")

    def toggle_complete(self, task_id, new_state):
        try:
            self.__cursor.execute("UPDATE tasks SET is_completed = %s WHERE task_id = %s", (new_state, task_id))
            self.__db.commit()
            self.refresh_tasks()
        except Exception as e:
            print(f"[ERROR] Complete toggle: {e}")

    def validate_date(self, date_str):
        try:
            due = datetime.strptime(date_str, "%Y-%m-%d").date()
            return due >= date.today()
        except ValueError:
            return False

    def inject_controller(self, controller):
        self.controller = controller
