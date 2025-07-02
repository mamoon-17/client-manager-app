import customtkinter as ctk
from customtkinter import CTkFont
from datetime import datetime, date
import math

class Clients(ctk.CTkFrame):

    def __init__(self, root, db):
        super().__init__(root)

        self.__db = db
        self.__root = root
        self.__cursor = db.get_cursor()

        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"

        self.__clients_per_page = 5
        self.__current_page = 1
        self.__total_pages = 1
        self.__total_clients = 0

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

        self.refresh_client_rows()  # ✅ FIXED: move to the end of __init__

    def client_rows(self):
        self.clients_container = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        self.clients_container.grid(row=2, column=0, sticky="nsew", padx=60, pady=(10, 20))
        self.clients_container.columnconfigure(0, weight=1)

    def count_total_clients(self):
        try:
            self.__cursor.execute("SELECT COUNT(*) FROM clients")
            self.__total_clients = self.__cursor.fetchone()[0]
            self.__total_pages = max(1, math.ceil(self.__total_clients / self.__clients_per_page))
        except Exception as e:
            print(f"[ERROR] Failed to count clients: {str(e)}")
            self.__total_clients = 0
            self.__total_pages = 1

    def fetch_clients_for_page(self):
        offset = (self.__current_page - 1) * self.__clients_per_page
        try:
            self.__cursor.execute("""
                SELECT client_id, name, email, company_name 
                FROM clients 
                ORDER BY name ASC 
                LIMIT %s OFFSET %s
            """, (self.__clients_per_page, offset))
            return self.__cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch clients: {str(e)}")
            return []

    def refresh_client_rows(self):
        self.count_total_clients()

        for widget in self.clients_container.winfo_children():
            widget.destroy()

        clients = self.fetch_clients_for_page()
        
        for i, (client_id, name, email, company) in enumerate(clients):
            client_frame = ctk.CTkFrame(self.clients_container, height=20, fg_color=self.__WIDGET_COLOR, corner_radius=10)
            client_frame.grid(row=i, column=0, sticky="ew", padx=20, pady=10)
            self.clients_container.rowconfigure(i, weight=0)

            display_text = f"{name} ({company}) - {email}"
            name_label = ctk.CTkLabel(client_frame, text=display_text, font=ctk.CTkFont(size=16))
            name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            client_frame.bind("<Button-1>", lambda e, c_id=client_id: self.open_client_profile(c_id))

        if hasattr(self, "page_label"):
            self.page_label.configure(text=f"Page {self.__current_page} / {self.__total_pages}")

    def prev_next_buttons(self):
        self.pagination_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        self.pagination_frame.grid(row=3, column=0, sticky="ew", pady=(0, 30), padx=80)
        self.pagination_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.page_label = ctk.CTkLabel(self.pagination_frame, text="Page 1 / 1")
        self.page_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="n")

        self.prev_btn = ctk.CTkButton(self.pagination_frame, text="Previous", command=self.go_previous_page)
        self.prev_btn.grid(row=1, column=1, padx=(0, 5), pady=(0, 30), sticky="e")

        self.next_btn = ctk.CTkButton(self.pagination_frame, text="Next", command=self.go_next_page)
        self.next_btn.grid(row=1, column=2, padx=(5, 0), pady=(0, 30), sticky="w")

    def go_previous_page(self):
        if self.__current_page > 1:
            self.__current_page -= 1
            self.refresh_client_rows()

    def go_next_page(self):
        if self.__current_page < self.__total_pages:
            self.__current_page += 1
            self.refresh_client_rows()

    def clients_title(self):
        title_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        title_frame.grid(row=0, column=0, sticky="ew", padx=80, pady=(60, 10))
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=0)

        clients_label = ctk.CTkLabel(
            title_frame,
            text="Clients",
            font=self.__title_font,
            text_color="white"
        )
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
            font=entry_font
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)

        optionmenu_var = ctk.StringVar(value="Sort by Date...")
        optionmenu = ctk.CTkOptionMenu(
            search_sort_frame,
            values=["Sort by Date...", "Oldest", "Newest"],
            variable=optionmenu_var,
            fg_color=self.__WIDGET_COLOR,
            button_color=self.__WIDGET_COLOR,
            button_hover_color=self.__WIDGET_COLOR,
            height=entry_height,
            font=entry_font,
            dropdown_font=entry_font
        )
        optionmenu.grid(row=0, column=1, sticky="ew", pady=10)

    def initFonts(self):
        self.__title_font = CTkFont(family="Raleway SemiBold", size=34, weight="bold")
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=16)
        self.__regular_font = CTkFont(family="Raleway", size=14)

    def open_client_profile(self, client_id):
        print(f"Opening profile for client ID: {client_id}")

    def inject_controller(self, controller):
        self.controller = controller

    def on_Addclients_click(self):
        if self.controller:
            self.controller.show_page("add_clients")
