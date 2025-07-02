import customtkinter as ctk
from customtkinter import CTkFont
from datetime import datetime
import math

class InvoicesPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)
        self.__db = db
        self.__root = root
        self.__cursor = db.get_cursor()
        self.controller = None  # 🔧 fix for missing controller

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"

        self.__invoices_per_page = 5
        self.__current_page = 1
        self.__total_pages = 1
        self.__invoices = []

        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color=self.__FRAME_COLOR, corner_radius=0)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)

        self.initFonts()
        self.invoices_title()
        self.search_and_sort_bar()
        self.prev_next_buttons()      # Moved up
        self.invoice_rows()           # Moved down

    def initFonts(self):
        self.__title_font = CTkFont(family="Raleway SemiBold", size=34, weight="bold")
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=16)
        self.__regular_font = CTkFont(family="Raleway", size=14)

    def invoice_rows(self):
        self.invoices_container = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        self.invoices_container.grid(row=2, column=0, sticky="nsew", padx=60, pady=(10, 20))
        self.invoices_container.columnconfigure(0, weight=1)

        self.fetch_invoices()
        self.refresh_invoice_rows()

    def fetch_invoices(self):
        offset = (self.__current_page - 1) * self.__invoices_per_page

        try:
            self.__cursor.execute("SELECT COUNT(*) FROM invoices")
            total = self.__cursor.fetchone()[0]
            self.__total_pages = max(1, math.ceil(total / self.__invoices_per_page))

            self.__cursor.execute("""
                SELECT i.invoice_id, c.name AS client_name, i.amount, i.status, i.due_date
                FROM invoices i
                JOIN clients c ON i.client_id = c.client_id
                ORDER BY i.due_date DESC
                LIMIT %s OFFSET %s
            """, (self.__invoices_per_page, offset))

            self.__invoices = self.__cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch invoices: {str(e)}")
            self.__invoices = []

    def refresh_invoice_rows(self):
        for widget in self.invoices_container.winfo_children():
            widget.destroy()

        for i, (invoice_id, client, amount, status, due) in enumerate(self.__invoices):
            frame = ctk.CTkFrame(self.invoices_container, fg_color=self.__WIDGET_COLOR, corner_radius=10)
            frame.grid(row=i, column=0, sticky="ew", padx=20, pady=10)
            self.invoices_container.rowconfigure(i, weight=0)

            text = f"#{invoice_id} | {client} | Rs. {amount:.2f} | {status} | Due: {due}"
            label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=15))
            label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            frame.bind("<Button-1>", lambda e, inv_id=invoice_id: self.open_invoice_details(inv_id))

        self.page_label.configure(text=f"Page {self.__current_page} / {self.__total_pages}")

    def prev_next_buttons(self):
        pagination_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        pagination_frame.grid(row=3, column=0, sticky="ew", pady=(0, 30), padx=80)
        pagination_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.page_label = ctk.CTkLabel(pagination_frame, text="Page 1 / 1")
        self.page_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="n")

        self.prev_btn = ctk.CTkButton(pagination_frame, text="Previous", command=self.go_previous_page)
        self.prev_btn.grid(row=1, column=1, padx=(0, 5), pady=(0, 30), sticky="e")

        self.next_btn = ctk.CTkButton(pagination_frame, text="Next", command=self.go_next_page)
        self.next_btn.grid(row=1, column=2, padx=(5, 0), pady=(0, 30), sticky="w")

    def go_previous_page(self):
        if self.__current_page > 1:
            self.__current_page -= 1
            self.fetch_invoices()
            self.refresh_invoice_rows()

    def go_next_page(self):
        if self.__current_page < self.__total_pages:
            self.__current_page += 1
            self.fetch_invoices()
            self.refresh_invoice_rows()

    def invoices_title(self):
        title_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        title_frame.grid(row=0, column=0, sticky="ew", padx=80, pady=(60, 10))
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=0)

        invoices_label = ctk.CTkLabel(
            title_frame,
            text="Invoices",
            font=self.__title_font,
            text_color="white"
        )
        invoices_label.grid(row=0, column=0, sticky="w")

        add_invoice_btn = ctk.CTkButton(
            title_frame,
            text="Add Invoice",
            font=self.__semi_bold_font,
            fg_color="#4a9eff",
            hover_color="#3d8bdb",
            corner_radius=8,
            height=38,
            command=self.on_add_invoice_click
        )
        add_invoice_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

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
            placeholder_text="Search invoice by client name...",
            height=entry_height,
            font=entry_font
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)

        sort_var = ctk.StringVar(value="Sort by Date...")
        sort_menu = ctk.CTkOptionMenu(
            search_sort_frame,
            values=["Sort by Date...", "Newest", "Oldest", "Status: Paid", "Status: Unpaid"],
            variable=sort_var,
            fg_color=self.__WIDGET_COLOR,
            button_color=self.__WIDGET_COLOR,
            button_hover_color=self.__WIDGET_COLOR,
            height=entry_height,
            font=entry_font,
            dropdown_font=entry_font
        )
        sort_menu.grid(row=0, column=1, sticky="ew", pady=10)

    def open_invoice_details(self, invoice_id):
        print(f"Viewing invoice: #{invoice_id}")

    def inject_controller(self, controller):
        self.controller = controller

    def on_add_invoice_click(self):
        if self.controller:
            self.controller.show_page("add_invoice")
