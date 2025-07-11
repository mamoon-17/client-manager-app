import customtkinter as ctk
from customtkinter import CTkFont
import math
import os
import smtplib
from tkinter import filedialog, simpledialog, messagebox
from email.message import EmailMessage
from utils.encryption import decrypt_note

class Clients(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)

        self.__db = db
        self.__root = root
        self.__cursor = db.get_cursor()
        self.controller = None

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"

        self.__clients_per_page = 5
        self.__current_page = 1
        self.__total_pages = 1
        self.__total_clients = 0

        self.__search_var = ctk.StringVar()
        self.__sort_var = ctk.StringVar(value="Sort by Date...")

        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color=self.__FRAME_COLOR, corner_radius=0)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)

        self.initFonts()
        self.clients_title()
        self.search_and_sort_bar()
        self.client_rows()
        self.prev_next_buttons()
        self.refresh_client_rows()

    def initFonts(self):
        self.__title_font = CTkFont(family="Raleway SemiBold", size=34, weight="bold")
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=16)
        self.__regular_font = CTkFont(family="Raleway", size=14)

    def clients_title(self):
        title_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        title_frame.grid(row=0, column=0, sticky="ew", padx=80, pady=(60, 10))
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=0)

        clients_label = ctk.CTkLabel(title_frame, text="Clients", font=self.__title_font, text_color="white")
        clients_label.grid(row=0, column=0, sticky="w")

        add_client_btn = ctk.CTkButton(
            title_frame,
            text="Add Client",
            font=self.__semi_bold_font,
            fg_color="#4a9eff",
            hover_color="#3d8bdb",
            corner_radius=8,
            height=38,
            command=self.on_Addclients_click
        )
        add_client_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

    def search_and_sort_bar(self):
        search_sort_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        search_sort_frame.grid(row=1, column=0, sticky="ew", padx=80, pady=10)
        search_sort_frame.columnconfigure(0, weight=3)
        search_sort_frame.columnconfigure(1, weight=1)

        entry_font = ctk.CTkFont(size=16)
        entry_height = 44

        search_entry = ctk.CTkEntry(
            search_sort_frame,
            fg_color=self.__WIDGET_COLOR,
            placeholder_text="Search...",
            height=entry_height,
            font=entry_font,
            textvariable=self.__search_var
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_client_rows())

        optionmenu = ctk.CTkOptionMenu(
            search_sort_frame,
            values=["Sort by Date...", "Oldest", "Newest"],
            variable=self.__sort_var,
            fg_color=self.__WIDGET_COLOR,
            button_color=self.__WIDGET_COLOR,
            button_hover_color=self.__WIDGET_COLOR,
            height=entry_height,
            font=entry_font,
            dropdown_font=entry_font,
            command=lambda _: self.refresh_client_rows()
        )
        optionmenu.grid(row=0, column=1, sticky="ew", pady=10)

    def client_rows(self):
        self.clients_container = ctk.CTkScrollableFrame(self, fg_color=self.__FRAME_COLOR)
        self.clients_container.grid(row=2, column=0, sticky="nsew", padx=60, pady=(10, 20))
        self.clients_container.columnconfigure(0, weight=1)

    def count_total_clients(self, search_term="%%"):
        try:
            self.__cursor.execute("""
                SELECT COUNT(*) FROM clients
                WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(company_name) LIKE LOWER(%s)
            """, (search_term, search_term))
            self.__total_clients = self.__cursor.fetchone()[0]
            self.__total_pages = max(1, math.ceil(self.__total_clients / self.__clients_per_page))
        except Exception as e:
            print(f"[ERROR] Failed to count clients: {str(e)}")
            self.__total_clients = 0
            self.__total_pages = 1

    def refresh_client_rows(self):
        search_text = self.__search_var.get().strip()
        search_term = f"%{search_text}%" if search_text else "%%"

        sort_value = self.__sort_var.get()
        order = "DESC" if sort_value == "Newest" else "ASC"

        self.count_total_clients(search_term)

        for widget in self.clients_container.winfo_children():
            widget.destroy()

        try:
            offset = (self.__current_page - 1) * self.__clients_per_page
            self.__cursor.execute(f"""
                SELECT client_id, name, email, company_name, notes
                FROM clients
                WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(company_name) LIKE LOWER(%s)
                ORDER BY client_id {order}
                LIMIT %s OFFSET %s
            """, (search_term, search_term, self.__clients_per_page, offset))
            clients = self.__cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Fetching clients: {e}")
            clients = []

        for i, (client_id, name, email, company, encrypted_note) in enumerate(clients):
            frame = ctk.CTkFrame(self.clients_container, fg_color=self.__WIDGET_COLOR, corner_radius=10)
            frame.grid(row=i, column=0, sticky="ew", padx=20, pady=10)
            frame.columnconfigure(0, weight=5)
            frame.columnconfigure(1, weight=0)
            frame.columnconfigure(2, weight=0)

            label = ctk.CTkLabel(frame, text=f"{name} ({company}) - {email}", font=ctk.CTkFont(size=15))
            label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            notes_label = ctk.CTkLabel(frame, text="🔒 Hidden", font=ctk.CTkFont(size=13), text_color="gray")
            notes_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=10)

            def create_reveal_button(parent, enc_note, lbl):
                btn = ctk.CTkButton(
                    parent,
                    text="Show Notes",
                    width=110,
                    height=30,
                    font=ctk.CTkFont(size=12),
                    fg_color="#6c757d",
                    hover_color="#5a6268"
                )
                def toggle():
                    if btn.cget("text") == "Show Notes":
                        try:
                            lbl.configure(text="📝 " + decrypt_note(enc_note) if enc_note else "No notes.")
                            btn.configure(text="Hide Notes")
                        except:
                            lbl.configure(text="[Decrypt Error]")
                    else:
                        lbl.configure(text="🔒 Hidden")
                        btn.configure(text="Show Notes")
                btn.configure(command=toggle)
                return btn

            create_reveal_button(frame, encrypted_note, notes_label).grid(row=0, column=1, padx=(10, 5), pady=10, sticky="e")

            ctk.CTkButton(
                frame,
                text="Send Email",
                fg_color="#28a745",
                hover_color="#218838",
                width=110,
                command=lambda email=email: self.send_email_to_client(email)
            ).grid(row=0, column=2, padx=10, pady=10, sticky="e")

            frame.bind("<Button-1>", lambda e, c_id=client_id: self.open_client_profile(c_id))

        if hasattr(self, "page_label"):
            self.page_label.configure(text=f"Page {self.__current_page} / {self.__total_pages}")

    def prev_next_buttons(self):
        frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        frame.grid(row=3, column=0, sticky="ew", pady=(0, 30), padx=80)
        frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.page_label = ctk.CTkLabel(frame, text="Page 1 / 1")
        self.page_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="n")

        ctk.CTkButton(frame, text="Previous", command=self.go_previous_page).grid(row=1, column=1, padx=(0, 5), pady=(0, 30), sticky="e")
        ctk.CTkButton(frame, text="Next", command=self.go_next_page).grid(row=1, column=2, padx=(5, 0), pady=(0, 30), sticky="w")

    def go_previous_page(self):
        if self.__current_page > 1:
            self.__current_page -= 1
            self.refresh_client_rows()

    def go_next_page(self):
        if self.__current_page < self.__total_pages:
            self.__current_page += 1
            self.refresh_client_rows()

    def open_client_profile(self, client_id):
        print(f"Opening profile for client ID: {client_id}")

    def inject_controller(self, controller):
        self.controller = controller

    def on_Addclients_click(self):
        if self.controller:
            self.controller.show_page("add_clients")

    def send_email_to_client(self, to_email):
        try:
            pdf_path = filedialog.askopenfilename(
                title="Select Invoice PDF",
                filetypes=[("PDF Files", "*.pdf")]
            )
            if not pdf_path:
                return
            subject = simpledialog.askstring("Subject", "Enter email subject:")
            if not subject:
                return
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = os.getenv("GMAIL_USER")
            msg['To'] = to_email
            msg.set_content("Please find attached your invoice.")
            with open(pdf_path, "rb") as f:
                file_data = f.read()
                msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
                smtp.send_message(msg)
            messagebox.showinfo("Success", f"Email sent to {to_email}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email:\n{str(e)}")
