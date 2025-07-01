import customtkinter as ctk
from customtkinter import CTkFont
from datetime import datetime, date

class Clients(ctk.CTkFrame):

    def __init__(self, root, db):
        super().__init__(root)

        self.__db = db
        self.__root = root

        # Colors
        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"

        # Init layout
        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color=self.__FRAME_COLOR, corner_radius=0)

        self.rowconfigure(0, weight=0)  # Title
        self.rowconfigure(1, weight=0)  # Search/Sort
        self.rowconfigure(2, weight=1)  # Client rows
        self.rowconfigure(3, weight=0)  # Pagination
        self.columnconfigure(0, weight=1)

        self.initFonts()

        self.clients_title()
        self.search_and_sort_bar()
        self.client_rows()
        self.prev_next_buttons()

    def client_rows(self):
        self.clients_container = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        self.clients_container.grid(row=2, column=0, sticky="nsew", padx=60, pady=(10, 20))
        self.clients_container.columnconfigure(0, weight=1)

        current_page_clients = ["Ali Shan Ashiq", "Nice Afnan", "Muhammad Adnan", "Rohaib Saeed", "Lun Khanzada"]

        for i, client in enumerate(current_page_clients):
            client_frame = ctk.CTkFrame(self.clients_container, height=20, fg_color=self.__WIDGET_COLOR, corner_radius=10)
            client_frame.grid(row=i, column=0, sticky="ew", padx=20, pady=10)
            self.clients_container.rowconfigure(i, weight=0)

            name_label = ctk.CTkLabel(client_frame, text=client, font=ctk.CTkFont(size=16))
            name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            client_frame.bind("<Button-1>", lambda e, c=client: self.open_client_profile(c))

    def prev_next_buttons(self):
        pagination_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        pagination_frame.grid(row=3, column=0, sticky="ew", pady=(0, 30), padx=80)
        pagination_frame.columnconfigure((0, 1, 2, 3), weight=1)

        page_label = ctk.CTkLabel(pagination_frame, text="page 1/1")
        page_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="n")

        prev_btn = ctk.CTkButton(pagination_frame, text="Previous")
        prev_btn.grid(row=1, column=1, padx=(0, 5), pady=(0, 35), sticky="e")

        next_btn = ctk.CTkButton(pagination_frame, text="Next")
        next_btn.grid(row=1, column=2, padx=(5, 0), pady=(0, 35), sticky="w")

    def clients_title(self):
        title_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR)
        title_frame.grid(row=0, column=0, sticky="ew", padx=80, pady=(60, 10))
        title_frame.columnconfigure(0, weight=1)

        clients_label = ctk.CTkLabel(
            title_frame,
            text="Clients",
            font=self.__title_font,
            text_color="white"
        )
        clients_label.grid(row=0, column=0, sticky="w")

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

    def open_client_profile(self, client):
        print(f"Opening profile for: {client}")
