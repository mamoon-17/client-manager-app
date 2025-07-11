import customtkinter as ctk
from customtkinter import CTkFont
from tkinter import messagebox
from datetime import date

class AddInvoicesPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)
        self.__db = db
        self.__cursor = self.__db.get_cursor()
        self.controller = None

        self.__main_frame = None
        self.__client_dropdown = None
        self.__client_var = None
        self.__amount_var = None
        self.__due_date_var = None
        self.__invoice_date_var = None
        self.__description_textbox = None
        self.__bank_name_var = None
        self.__account_number_var = None
        self.__status_var = None
        self.__clients_data = []

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"

        self.__title_font = CTkFont(family="Raleway SemiBold", size=28, weight="bold")
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=16)
        self.__regular_font = CTkFont(family="Raleway", size=14)

        self.configure(fg_color=self.__FRAME_COLOR, corner_radius=0)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.loadClients()
        self.initLayout()

    def loadClients(self):
        try:
            self.__cursor.execute("SELECT client_id, name, email FROM clients")
            self.__clients_data = self.__cursor.fetchall()
            print("[DEBUG] Clients fetched:", self.__clients_data)
        except Exception as e:
            print(f"[ERROR] Failed to load clients: {str(e)}")
            self.__clients_data = []

    def initLayout(self):
        self.__main_frame = ctk.CTkScrollableFrame(self, fg_color=self.__FRAME_COLOR, corner_radius=0)
        self.__main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.__main_frame.columnconfigure(0, weight=1)

        self.initHeader()
        self.initClientSection()
        self.initInvoiceDetailsSection()
        self.initPaymentSection()
        self.initButtonsSection()

    def initHeader(self):
        header = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.columnconfigure(0, weight=1)

        ctk.CTkLabel(header, text="Create New Invoice", font=self.__title_font, text_color="white").grid(row=0, column=0, pady=20)

    def initClientSection(self):
        frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Client Information", font=self.__semi_bold_font, text_color="white").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(frame, text="Select Client:", font=self.__regular_font, text_color="white").grid(row=1, column=0, sticky="w", padx=20, pady=10)

        self.__client_var = ctk.StringVar()
        if self.__clients_data:
            values = [f"{name} - {email}" for _, name, email in self.__clients_data]
            self.__client_dropdown = ctk.CTkComboBox(
                frame,
                values=values,
                variable=self.__client_var,
                font=self.__regular_font,
                fg_color=self.__FRAME_COLOR,
                border_color=self.__temp_color,
                button_color=self.__temp_color,
                dropdown_fg_color=self.__FRAME_COLOR
            )
            self.__client_dropdown.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=10)
        else:
            ctk.CTkLabel(frame, text="No clients found.", font=self.__regular_font, text_color="#ff6b6b").grid(row=1, column=1, sticky="w", padx=(10, 20), pady=10)

    def initInvoiceDetailsSection(self):
        frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        ctk.CTkLabel(frame, text="Invoice Details", font=self.__semi_bold_font, text_color="white").grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(20, 10))

        self.__amount_var = ctk.StringVar()
        ctk.CTkLabel(frame, text="Amount:", font=self.__regular_font, text_color="white").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        ctk.CTkEntry(frame, textvariable=self.__amount_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="0.00").grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=10)

        self.__invoice_date_var = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ctk.CTkLabel(frame, text="Invoice Date:", font=self.__regular_font, text_color="white").grid(row=1, column=2, sticky="w", padx=20, pady=10)
        ctk.CTkEntry(frame, textvariable=self.__invoice_date_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="YYYY-MM-DD").grid(row=1, column=3, sticky="ew", padx=(10, 20), pady=10)

        self.__due_date_var = ctk.StringVar()
        ctk.CTkLabel(frame, text="Due Date:", font=self.__regular_font, text_color="white").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        ctk.CTkEntry(frame, textvariable=self.__due_date_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="YYYY-MM-DD").grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=10)

        self.__status_var = ctk.StringVar(value="UNPAID")
        ctk.CTkLabel(frame, text="Status:", font=self.__regular_font, text_color="white").grid(row=2, column=2, sticky="w", padx=20, pady=10)
        ctk.CTkComboBox(frame, values=["PAID", "UNPAID"], variable=self.__status_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color).grid(row=2, column=3, sticky="ew", padx=(10, 20), pady=10)

        ctk.CTkLabel(frame, text="Description:", font=self.__regular_font, text_color="white").grid(row=3, column=0, sticky="nw", padx=20, pady=10)
        self.__description_textbox = ctk.CTkTextbox(frame, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, height=80)
        self.__description_textbox.grid(row=3, column=1, columnspan=3, sticky="ew", padx=(10, 20), pady=10)

    def initPaymentSection(self):
        frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        ctk.CTkLabel(frame, text="Payment Information", font=self.__semi_bold_font, text_color="white").grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(20, 10))

        self.__bank_name_var = ctk.StringVar()
        ctk.CTkLabel(frame, text="Bank Name:", font=self.__regular_font, text_color="white").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        ctk.CTkEntry(frame, textvariable=self.__bank_name_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="Enter bank name").grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=10)

        self.__account_number_var = ctk.StringVar()
        ctk.CTkLabel(frame, text="Account Number:", font=self.__regular_font, text_color="white").grid(row=1, column=2, sticky="w", padx=20, pady=10)
        ctk.CTkEntry(frame, textvariable=self.__account_number_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="Enter account number").grid(row=1, column=3, sticky="ew", padx=(10, 20), pady=10)

    def initButtonsSection(self):
        frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        frame.columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(frame, text="Create Invoice", font=self.__semi_bold_font, fg_color="#4a9eff", hover_color="#3d8bdb", command=self.createInvoice).grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(frame, text="Clear Form", font=self.__semi_bold_font, fg_color=self.__temp_color, command=self.clearForm).grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(frame, text="Refresh Clients", font=self.__semi_bold_font, fg_color="#28a745", command=self.refreshClients).grid(row=0, column=2, padx=20, pady=20, sticky="ew")

    def createInvoice(self):
        try:
            client_selection = self.__client_var.get()
            client_id = None

            for cid, name, email in self.__clients_data:
                if client_selection == f"{name} - {email}":
                    client_id = cid
                    break

            if not all([
                client_id,
                self.__amount_var.get().strip(),
                self.__invoice_date_var.get().strip(),
                self.__due_date_var.get().strip(),
                self.__status_var.get().strip()
            ]):
                messagebox.showwarning("Validation Error", "Please fill all required fields.")
                return

            query = """
                INSERT INTO invoices (client_id, amount, invoice_date, due_date, description, bank_name, account_number, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.__cursor.execute(query, (
                client_id,
                self.__amount_var.get().strip(),
                self.__invoice_date_var.get().strip(),
                self.__due_date_var.get().strip(),
                self.__description_textbox.get("1.0", "end").strip(),
                self.__bank_name_var.get().strip(),
                self.__account_number_var.get().strip(),
                self.__status_var.get().strip()
            ))
            self.__db.commit()

            # ✅ Activity Log
            self.__db._DB__queries.log_activity("Invoice Created", f"Invoice added for Client ID {client_id}")

            messagebox.showinfo("Success", "Invoice added successfully.")
            self.clearForm()
            self.controller.get_page("invoices").refresh_invoice_rows()
            self.controller.show_page("invoices")

        except Exception as e:
            self.__db.rollback()
            messagebox.showerror("Database Error", f"Error creating invoice: {str(e)}")

    def inject_controller(self, controller):
        self.controller = controller

    def clearForm(self):
        if self.__client_var:
            self.__client_var.set("")
        self.__amount_var.set("")
        self.__due_date_var.set("")
        self.__invoice_date_var.set(date.today().strftime("%Y-%m-%d"))
        self.__description_textbox.delete("1.0", "end")
        self.__bank_name_var.set("")
        self.__account_number_var.set("")
        self.__status_var.set("UNPAID")

    def refreshClients(self):
        self.loadClients()
        if self.__clients_data and self.__client_dropdown:
            updated_values = [f"{name} - {email}" for _, name, email in self.__clients_data]
            self.__client_dropdown.configure(values=updated_values)
        messagebox.showinfo("Refreshed", "Client list updated.")
