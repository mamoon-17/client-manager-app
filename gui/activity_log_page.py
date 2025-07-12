import customtkinter as ctk
from customtkinter import CTkFont

class ActivityLogPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)
        self.__db = db
        self.controller = None

        self.configure(fg_color="#23262b")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="All Activity Logs",
            font=CTkFont(family="Raleway SemiBold", size=34),
            text_color="white"
        )
        self.title_label.grid(row=0, column=0, pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#2b2e33",
            corner_radius=10
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.refresh_logs()

    def refresh_logs(self):
        # Clear old widgets first
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Fetch updated activity logs
        activities = self.__db.get_queries().get_recent_activities(limit=100)

        if not activities:
            no_data = ctk.CTkLabel(self.scrollable_frame, text="No activity found.", text_color="white")
            no_data.pack(pady=10)
            return

        for activity_type, desc in activities:
            log = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"{activity_type}: {desc}",
                text_color="white",
                font=CTkFont(size=16),
                anchor="w",
                wraplength=800,
                justify="left"
            )
            log.pack(fill="x", padx=10, pady=5)

    def inject_controller(self, controller):
        self.controller = controller
