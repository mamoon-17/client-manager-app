import customtkinter as ctk
from customtkinter import CTkFont
from datetime import datetime

class PaymentsPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)
        self.__db = db
        self.__root = root

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"

        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color=self.__FRAME_COLOR, corner_radius=0)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)

        self.initFonts()
        self.payments_title()
        self.search_and_filter_bar()
        self.init_mock_data()
        self.payment_rows()
        self.prev_next_buttons()

    def initFonts(self):
        self.__title_font = CTkFont(family="Raleway SemiBold", size=34, weight="bold")
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=16)
        self.__regular_font = CTkFont(family="Raleway", size=14)

    def payments_title(self):
        title_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        title_frame.grid(row=0, column=0, sticky="ew", padx=80, pady=(60, 10))
        title_frame.columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Payments",
            font=self.__title_font,
            text_color="white"
        )
        title_label.grid(row=0, column=0, sticky="w")

    def search_and_filter_bar(self):
        filter_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=80, pady=10)
        filter_frame.columnconfigure(0, weight=3)
        filter_frame.columnconfigure(1, weight=1)

        entry_font = ctk.CTkFont(size=16)
        entry_height = 44

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            fg_color=self.__WIDGET_COLOR,
            placeholder_text="Search payment by invoice ID...",
            height=entry_height,
            font=entry_font
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)

        self.filter_var = ctk.StringVar(value="All")
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "Paid", "Received", "Newest", "Oldest"],
            variable=self.filter_var,
            command=self.apply_filter,
            fg_color=self.__WIDGET_COLOR,
            button_color=self.__WIDGET_COLOR,
            button_hover_color=self.__WIDGET_COLOR,
            height=entry_height,
            font=entry_font,
            dropdown_font=entry_font
        )
        filter_menu.grid(row=0, column=1, sticky="ew", pady=10)

    def init_mock_data(self):
        self.mock_payments = [
            {"payment_id": 1, "invoice_id": 101, "amount_paid": 1500.00, "payment_date": "2025-07-01", "payment_type": "Received"},
            {"payment_id": 2, "invoice_id": 102, "amount_paid": 3200.50, "payment_date": "2025-06-09", "payment_type": "Paid"},
            {"payment_id": 3, "invoice_id": 103, "amount_paid": 875.75, "payment_date": "2025-07-02", "payment_type": "Received"},
        ]
        self.filtered_payments = self.mock_payments.copy()

    def payment_rows(self):
        if hasattr(self, 'payments_container'):
            self.payments_container.destroy()

        self.payments_container = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        self.payments_container.grid(row=2, column=0, sticky="nsew", padx=60, pady=(10, 20))
        self.payments_container.columnconfigure(0, weight=1)

        for i, payment in enumerate(self.filtered_payments):
            frame = ctk.CTkFrame(self.payments_container, fg_color=self.__WIDGET_COLOR, corner_radius=10)
            frame.grid(row=i, column=0, sticky="ew", padx=20, pady=10)
            self.payments_container.rowconfigure(i, weight=0)

            text = f"[{payment['payment_type']}] | Payment ID: {payment['payment_id']} | Invoice #{payment['invoice_id']} | Rs. {payment['amount_paid']} | Date: {payment['payment_date']}"
            label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=15))
            label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            frame.bind("<Button-1>", lambda e, payment=payment: self.view_payment_details(payment))

    def prev_next_buttons(self):
        pagination_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        pagination_frame.grid(row=3, column=0, sticky="ew", pady=(0, 30), padx=80)
        pagination_frame.columnconfigure((0, 1, 2, 3), weight=1)

        page_label = ctk.CTkLabel(pagination_frame, text="page 1/1")
        page_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="n")

        prev_btn = ctk.CTkButton(pagination_frame, text="Previous")
        prev_btn.grid(row=1, column=1, padx=(0, 5), pady=(0, 30), sticky="e")

        next_btn = ctk.CTkButton(pagination_frame, text="Next")
        next_btn.grid(row=1, column=2, padx=(5, 0), pady=(0, 30), sticky="w")

    def apply_filter(self, choice):
        if choice == "All":
            self.filtered_payments = self.mock_payments
        elif choice in ["Paid", "Received"]:
            self.filtered_payments = [p for p in self.mock_payments if p["payment_type"] == choice]
        elif choice == "Newest":
            self.filtered_payments = sorted(self.mock_payments, key=lambda x: x["payment_date"], reverse=True)
        elif choice == "Oldest":
            self.filtered_payments = sorted(self.mock_payments, key=lambda x: x["payment_date"])
        else:
            self.filtered_payments = self.mock_payments

        self.payment_rows()

    def view_payment_details(self, payment):
        print(f"Viewing payment: {payment}")

    def inject_controller(self, controller):
        self.controller = controller
