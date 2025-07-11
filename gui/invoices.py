import customtkinter as ctk
from customtkinter import CTkFont
from datetime import datetime
import math
from utils.pdf_generator import generate_invoice_pdf
from tkinter import filedialog


class InvoicesPage(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)
        self.__db = db
        self.__root = root
        self.__cursor = db.get_cursor()
        self.controller = None

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"

        self.__invoices_per_page = 5
        self.__current_page = 1
        self.__total_pages = 1
        self.__invoices = []

        self.__sort_var = ctk.StringVar(value="Sort by Date...")
        self.__search_var = ctk.StringVar()

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
        self.prev_next_buttons()
        self.invoice_rows()

    def initFonts(self):
        self.__title_font = CTkFont(family="Raleway SemiBold", size=34, weight="bold")
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=16)
        self.__regular_font = CTkFont(family="Raleway", size=14)

    def invoice_rows(self):
        self.invoices_container = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        self.invoices_container.grid(row=2, column=0, sticky="nsew", padx=60, pady=(10, 20))
        self.invoices_container.columnconfigure(0, weight=1)

        self.apply_filters()

    def apply_filters(self):
        offset = (self.__current_page - 1) * self.__invoices_per_page
        sort = self.__sort_var.get()
        search = self.__search_var.get().strip().lower()

        where = []
        if search:
            where.append(f"LOWER(c.name) LIKE '%{search}%'")

        if sort == "Status: Paid":
            where.append("i.status = 'PAID'")
        elif sort == "Status: Unpaid":
            where.append("i.status = 'UNPAID'")

        where_clause = "WHERE " + " AND ".join(where) if where else ""

        order_clause = "ORDER BY i.due_date DESC"
        if sort == "Newest":
            order_clause = "ORDER BY i.invoice_date DESC"
        elif sort == "Oldest":
            order_clause = "ORDER BY i.invoice_date ASC"

        count_query = f"""
            SELECT COUNT(*)
            FROM invoices i
            JOIN clients c ON i.client_id = c.client_id
            {where_clause}
        """

        data_query = f"""
            SELECT i.invoice_id, c.name, i.amount, i.status, i.due_date
            FROM invoices i
            JOIN clients c ON i.client_id = c.client_id
            {where_clause}
            {order_clause}
            LIMIT %s OFFSET %s
        """

        try:
            self.__cursor.execute(count_query)
            total = self.__cursor.fetchone()[0]
            self.__total_pages = max(1, math.ceil(total / self.__invoices_per_page))

            self.__cursor.execute(data_query, (self.__invoices_per_page, offset))
            self.__invoices = self.__cursor.fetchall()

        except Exception as e:
            print(f"[ERROR] apply_filters(): {e}")
            self.__invoices = []

        self.refresh_invoice_rows()

    def refresh_invoice_rows(self):
        for widget in self.invoices_container.winfo_children():
            widget.destroy()

        for i, (invoice_id, client, amount, status, due) in enumerate(self.__invoices):
            frame = ctk.CTkFrame(self.invoices_container, fg_color=self.__WIDGET_COLOR, corner_radius=10)
            frame.grid(row=i, column=0, sticky="ew", padx=20, pady=10)
            frame.columnconfigure(0, weight=0)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=0)

            label = ctk.CTkLabel(
                frame,
                text=f"#{invoice_id} | {client} | Rs. {amount:.2f} | {status} | Due: {due}",
                font=ctk.CTkFont(size=15)
            )
            label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            pdf_btn = ctk.CTkButton(
                frame,
                text="Generate PDF",
                width=120,
                height=28,
                font=ctk.CTkFont(size=13),
                fg_color="#4a9eff",
                hover_color="#3d8bdb",
                command=lambda inv_id=invoice_id: self.generate_invoice_pdf(inv_id)
            )
            pdf_btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")

            frame.bind("<Button-1>", lambda e, inv_id=invoice_id: self.open_invoice_details(inv_id))

        if hasattr(self, "page_label"):
            self.page_label.configure(text=f"Page {self.__current_page} / {self.__total_pages}")

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
            font=entry_font,
            textvariable=self.__search_var
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)
        search_entry.bind("<KeyRelease>", lambda e: self.on_search_or_sort())

        sort_menu = ctk.CTkOptionMenu(
            search_sort_frame,
            values=["Sort by Date...", "Newest", "Oldest", "Status: Paid", "Status: Unpaid"],
            variable=self.__sort_var,
            command=lambda _: self.on_search_or_sort(),
            fg_color=self.__WIDGET_COLOR,
            button_color=self.__WIDGET_COLOR,
            button_hover_color=self.__WIDGET_COLOR,
            height=entry_height,
            font=entry_font,
            dropdown_font=entry_font
        )
        sort_menu.grid(row=0, column=1, sticky="ew", pady=10)

    def on_search_or_sort(self):
        self.__current_page = 1
        self.apply_filters()

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
            self.apply_filters()

    def go_next_page(self):
        if self.__current_page < self.__total_pages:
            self.__current_page += 1
            self.apply_filters()

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

    def generate_invoice_pdf(self, invoice_id):
        try:
            self.__cursor.execute("""
                SELECT i.invoice_id, i.amount, i.invoice_date, i.due_date, i.description, i.status,
                       c.name, c.email, c.phone, c.company_name
                FROM invoices i
                JOIN clients c ON i.client_id = c.client_id
                WHERE i.invoice_id = %s
            """, (invoice_id,))
            row = self.__cursor.fetchone()

            if not row:
                print(f"[ERROR] Invoice #{invoice_id} not found.")
                return

            invoice = {
                "invoice_id": row[0],
                "amount": float(row[1]),
                "invoice_date": row[2].strftime("%Y-%m-%d"),
                "due_date": row[3].strftime("%Y-%m-%d"),
                "description": row[4],
                "status": row[5]
            }
            client = {
                "name": row[6],
                "email": row[7],
                "phone": row[8],
                "company_name": row[9]
            }

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"invoice_{invoice_id}.pdf"
            )

            if file_path:
                generate_invoice_pdf(invoice, client, file_path)
                print(f"[INFO] PDF saved at: {file_path}")

        except Exception as e:
            print(f"[ERROR] Failed to generate PDF: {str(e)}")

    def open_invoice_details(self, invoice_id):
        print(f"Viewing invoice: #{invoice_id}")

    def inject_controller(self, controller):
        self.controller = controller

    def on_add_invoice_click(self):
        if self.controller:
            self.controller.show_page("add_invoice")
