import customtkinter as ctk
from customtkinter import CTkFont
from tkinter import messagebox
from datetime import datetime, date

class InvoicesPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)

        # self.__db = db
        # self.__connection = None 
        # self.__root = root
        self.__main_frame = None
        self.__header_frame = None
        self.__client_frame = None
        self.__invoice_details_frame = None
        self.__payment_frame = None
        self.__buttons_frame = None

        self.__client_var = None
        self.__amount_var = None
        self.__due_date_var = None
        self.__invoice_date_var = None
        self.__description_var = None
        self.__bank_name_var = None
        self.__account_number_var = None
        self.__status_var = None
        self.__description_textbox = None

        self.__clients_data = []

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"

        self.__title_font = None
        self.__semi_bold_font = None
        self.__regular_font = None

        self.configure(fg_color=self.__FRAME_COLOR, corner_radius=0)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.initFonts()
        self.loadClients()
        self.initLayout()

    def initFonts(self):
        self.__title_font = CTkFont(family="Raleway SemiBold", size=28, weight="bold")
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=16)
        self.__regular_font = CTkFont(family="Raleway", size=14)

    def loadClients(self):
        self.__clients_data = [(1, "Zohaib - kms"), (2, "chishti - kys")]

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
        self.__header_frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        self.__header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.__header_frame.columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(self.__header_frame, text="Create New Invoice", font=self.__title_font, text_color="white")
        title_label.grid(row=0, column=0, pady=20)

    def initClientSection(self):
        self.__client_frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        self.__client_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.__client_frame.columnconfigure(1, weight=1)

        section_label = ctk.CTkLabel(self.__client_frame, text="Client Information", font=self.__semi_bold_font, text_color="white")
        section_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 10))

        client_label = ctk.CTkLabel(self.__client_frame, text="Select Client:", font=self.__regular_font, text_color="white")
        client_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)

        if self.__clients_data:
            client_values = [client[1] for client in self.__clients_data]
            self.__client_var = ctk.StringVar()
            client_dropdown = ctk.CTkComboBox(self.__client_frame, values=client_values, variable=self.__client_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, button_color=self.__temp_color, dropdown_fg_color=self.__FRAME_COLOR)
            client_dropdown.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=10)
        else:
            no_clients_label = ctk.CTkLabel(self.__client_frame, text="No clients found.", font=self.__regular_font, text_color="#ff6b6b")
            no_clients_label.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=10)

    def initInvoiceDetailsSection(self):
        self.__invoice_details_frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        self.__invoice_details_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.__invoice_details_frame.columnconfigure(1, weight=1)
        self.__invoice_details_frame.columnconfigure(3, weight=1)

        section_label = ctk.CTkLabel(self.__invoice_details_frame, text="Invoice Details", font=self.__semi_bold_font, text_color="white")
        section_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(20, 10))

        amount_label = ctk.CTkLabel(self.__invoice_details_frame, text="Amount:", font=self.__regular_font, text_color="white")
        amount_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)

        self.__amount_var = ctk.StringVar()
        amount_entry = ctk.CTkEntry(self.__invoice_details_frame, textvariable=self.__amount_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="0.00")
        amount_entry.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=10)

        invoice_date_label = ctk.CTkLabel(self.__invoice_details_frame, text="Invoice Date:", font=self.__regular_font, text_color="white")
        invoice_date_label.grid(row=1, column=2, sticky="w", padx=20, pady=10)

        self.__invoice_date_var = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        invoice_date_entry = ctk.CTkEntry(self.__invoice_details_frame, textvariable=self.__invoice_date_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="YYYY-MM-DD")
        invoice_date_entry.grid(row=1, column=3, sticky="ew", padx=(10, 20), pady=10)

        due_date_label = ctk.CTkLabel(self.__invoice_details_frame, text="Due Date:", font=self.__regular_font, text_color="white")
        due_date_label.grid(row=2, column=0, sticky="w", padx=20, pady=10)

        self.__due_date_var = ctk.StringVar()
        due_date_entry = ctk.CTkEntry(self.__invoice_details_frame, textvariable=self.__due_date_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="YYYY-MM-DD")
        due_date_entry.grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=10)

        status_label = ctk.CTkLabel(self.__invoice_details_frame, text="Status:", font=self.__regular_font, text_color="white")
        status_label.grid(row=2, column=2, sticky="w", padx=20, pady=10)

        self.__status_var = ctk.StringVar(value="UNPAID")
        status_dropdown = ctk.CTkComboBox(self.__invoice_details_frame, values=["PAID", "UNPAID"], variable=self.__status_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, button_color=self.__temp_color, dropdown_fg_color=self.__FRAME_COLOR)
        status_dropdown.grid(row=2, column=3, sticky="ew", padx=(10, 20), pady=10)

        description_label = ctk.CTkLabel(self.__invoice_details_frame, text="Description:", font=self.__regular_font, text_color="white")
        description_label.grid(row=3, column=0, sticky="nw", padx=20, pady=10)

        self.__description_textbox = ctk.CTkTextbox(self.__invoice_details_frame, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, height=80)
        self.__description_textbox.grid(row=3, column=1, columnspan=3, sticky="ew", padx=(10, 20), pady=10)

    def initPaymentSection(self):
        self.__payment_frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        self.__payment_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.__payment_frame.columnconfigure(1, weight=1)
        self.__payment_frame.columnconfigure(3, weight=1)

        section_label = ctk.CTkLabel(self.__payment_frame, text="Payment Information", font=self.__semi_bold_font, text_color="white")
        section_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(20, 10))

        bank_label = ctk.CTkLabel(self.__payment_frame, text="Bank Name:", font=self.__regular_font, text_color="white")
        bank_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)

        self.__bank_name_var = ctk.StringVar()
        bank_entry = ctk.CTkEntry(self.__payment_frame, textvariable=self.__bank_name_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="Enter bank name")
        bank_entry.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=10)

        account_label = ctk.CTkLabel(self.__payment_frame, text="Account Number:", font=self.__regular_font, text_color="white")
        account_label.grid(row=1, column=2, sticky="w", padx=20, pady=10)

        self.__account_number_var = ctk.StringVar()
        account_entry = ctk.CTkEntry(self.__payment_frame, textvariable=self.__account_number_var, font=self.__regular_font, fg_color=self.__FRAME_COLOR, border_color=self.__temp_color, placeholder_text="Enter account number")
        account_entry.grid(row=1, column=3, sticky="ew", padx=(10, 20), pady=(10, 20))

    def initButtonsSection(self):
        self.__buttons_frame = ctk.CTkFrame(self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15)
        self.__buttons_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        self.__buttons_frame.columnconfigure(0, weight=1)
        self.__buttons_frame.columnconfigure(1, weight=1)
        self.__buttons_frame.columnconfigure(2, weight=1)

        create_button = ctk.CTkButton(self.__buttons_frame, text="Create Invoice", font=self.__semi_bold_font, fg_color="#4a9eff", hover_color="#3d8bdb", corner_radius=10, height=45, command=self.createInvoice)
        create_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        clear_button = ctk.CTkButton(self.__buttons_frame, text="Clear Form", font=self.__semi_bold_font, fg_color=self.__temp_color, hover_color="#5a5d61", corner_radius=10, height=45, command=self.clearForm)
        clear_button.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        refresh_button = ctk.CTkButton(self.__buttons_frame, text="Refresh Clients", font=self.__semi_bold_font, fg_color="#28a745", hover_color="#218838", corner_radius=10, height=45, command=self.refreshClients)
        refresh_button.grid(row=0, column=2, padx=20, pady=20, sticky="ew")

    def createInvoice(self):
        print("[DEBUG] Create Invoice Clicked")
        messagebox.showinfo("Info", "Invoice creation simulated.")

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
        print("[DEBUG] Refresh Clients Clicked")
        messagebox.showinfo("Info", "Client list refresh simulated.")
