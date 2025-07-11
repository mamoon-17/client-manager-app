import customtkinter as ctk
from tkinter import messagebox
from utils.encryption import encrypt_note

class AddClientsPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)
        self.__db = db

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"
        self.__font = ctk.CTkFont(family="Raleway", size=14)
        self.__title_font = ctk.CTkFont(family="Raleway SemiBold", size=24, weight="bold")

        self.configure(fg_color=self.__FRAME_COLOR)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.__name_var = ctk.StringVar()
        self.__email_var = ctk.StringVar()
        self.__phone_var = ctk.StringVar()
        self.__company_var = ctk.StringVar()
        self.__notes_var = ctk.StringVar()

        self.initUI()

    def initUI(self):
        scrollable_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        form_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        form_frame.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(form_frame, text="Add New Client", font=self.__title_font, text_color="white")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        subtitle_label = ctk.CTkLabel(
            form_frame,
            text="Please fill out the client's information below.",
            font=ctk.CTkFont(family="Raleway", size=12),
            text_color=self.__temp_color
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 25))

        labels = ["Name", "Email", "Phone", "Company Name", "Notes"]
        vars = [self.__name_var, self.__email_var, self.__phone_var, self.__company_var, self.__notes_var]

        for i, (label_text, var) in enumerate(zip(labels, vars)):
            row = i + 2
            label = ctk.CTkLabel(form_frame, text=f"{label_text}:", font=self.__font, text_color="white")
            label.grid(row=row, column=0, sticky="w", padx=30, pady=(12, 6))

            entry = ctk.CTkEntry(
                form_frame,
                textvariable=var,
                font=self.__font,
                fg_color=self.__FRAME_COLOR,
                border_color=self.__temp_color,
                placeholder_text=f"Enter {label_text.lower()}",
                height=35,
                corner_radius=8,
                border_width=1
            )
            entry.grid(row=row, column=1, sticky="ew", padx=(15, 30), pady=(12, 6))

        separator_frame = ctk.CTkFrame(form_frame, fg_color=self.__temp_color, height=1)
        separator_frame.grid(row=len(labels) + 2, column=0, columnspan=2, sticky="ew", padx=30, pady=15)

        button_frame = ctk.CTkFrame(form_frame, fg_color=self.__WIDGET_COLOR)
        button_frame.grid(row=len(labels) + 3, column=0, columnspan=2, pady=(10, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        add_btn = ctk.CTkButton(
            button_frame,
            text="Add Client",
            font=self.__font,
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=10,
            height=40,
            command=self.addClient
        )
        add_btn.grid(row=0, column=0, padx=(30, 15), pady=15, sticky="ew")

        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear Form",
            font=self.__font,
            fg_color=self.__temp_color,
            hover_color="#5a5d61",
            corner_radius=10,
            height=40,
            command=self.clearForm
        )
        clear_btn.grid(row=0, column=1, padx=(15, 30), pady=15, sticky="ew")

    def addClient(self):
        name = self.__name_var.get().strip()
        email = self.__email_var.get().strip()
        phone = self.__phone_var.get().strip()
        company = self.__company_var.get().strip()
        notes = self.__notes_var.get().strip()

        if not all([name, email, phone]):
            messagebox.showwarning("Validation Error", "Please fill all required fields (Name, Email, Phone).")
            return

        try:
            encrypted_notes = encrypt_note(notes) if notes else None

            cursor = self.__db.get_cursor()
            query = """
                INSERT INTO clients (name, email, phone, company_name, notes)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, phone, company or None, encrypted_notes))
            self.__db.commit()

            # ✅ Log activity
            self.__db._DB__queries.log_activity(
                activity_type="Client Added",
                description=f"Added client '{name}'",
                client_id=cursor.lastrowid
            )

            messagebox.showinfo("Success", "Client added successfully.")
            self.clearForm()
            self.controller.get_page("clients").refresh_client_rows()

        except Exception as e:
            self.__db.rollback()
            messagebox.showerror("Database Error", f"Error adding client: {str(e)}")

    def inject_controller(self, controller):
        self.controller = controller

    def clearForm(self):
        for var in [self.__name_var, self.__email_var, self.__phone_var, self.__company_var, self.__notes_var]:
            var.set("")
