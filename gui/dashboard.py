import customtkinter as ctk
from customtkinter import CTkFont
from PIL import Image
import os

class Dashboard(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)

        self.__db = db
        self.__root = root

        # Frame containers
        self.__top_frame = None
        self.__middle_frame = None
        self.__bottom_frame = None
        self.__totalClients_frame = None
        self.__totalInvoices_frame = None
        self.__paidInvoices_frame = None
        self.__recentActivity_frame = None

        # Colors
        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"

        # Layout
        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color=self.__FRAME_COLOR, corner_radius=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.initTopframe()
        self.initMiddleframe()
        self.initBottomframe()

    def inject_controller(self, controller):
        self.controller = controller

    def initTopframe(self):
        self.__top_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR, corner_radius=15)
        self.__top_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        self.__top_frame.grid_propagate(False)
        self.__top_frame.columnconfigure(0, weight=1)
        self.__top_frame.columnconfigure(1, weight=1)
        self.__top_frame.rowconfigure(0, weight=1)

        self.initTotalClientsFrame()
        self.initTotalInvoicesFrame()

    def initTotalClientsFrame(self):
        self.__totalClients_frame = ctk.CTkFrame(
            self.__top_frame,
            fg_color=self.__WIDGET_COLOR,
            width=300,
            height=220,
            corner_radius=15,
        )
        self.__totalClients_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.__totalClients_frame.grid_propagate(False)
        self.__totalClients_frame.columnconfigure(0, weight=1)
        self.__totalClients_frame.rowconfigure(0, weight=1)
        self.totalClientsLabel()

    def totalClientsLabel(self):
        self.__labelsemi_bold_font = CTkFont(family="Raleway SemiBold", size=32)
        label = ctk.CTkLabel(
            self.__totalClients_frame,
            text="Total Clients",
            font=self.__labelsemi_bold_font,
            text_color="white",
            height=150
        )
        label.grid(row=0, column=0, sticky="nw", padx=60, pady=(5, 0))

        value = ctk.CTkLabel(
            self.__totalClients_frame,
            text="146",
            font=ctk.CTkFont(size=45, weight="bold"),
            text_color="white"
        )
        value.grid(row=1, column=0, sticky="nw", padx=60, pady=(0, 50))

    def initTotalInvoicesFrame(self):
        self.__totalInvoices_frame = ctk.CTkFrame(
            self.__top_frame,
            fg_color=self.__WIDGET_COLOR,
            width=300,
            height=220,
            corner_radius=15,
        )
        self.__totalInvoices_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        self.__totalInvoices_frame.grid_propagate(False)
        self.__totalInvoices_frame.rowconfigure(0, weight=1)
        self.__totalInvoices_frame.columnconfigure(1, weight=1)
        self.totalInvoicesLabel()

    def totalInvoicesLabel(self):
        self.__labelsemi_bold_font = CTkFont(family="Raleway SemiBold", size=32)
        label = ctk.CTkLabel(
            self.__totalInvoices_frame,
            text="Total Invoices",
            font=self.__labelsemi_bold_font,
            text_color="white",
            height=150
        )
        label.grid(row=0, column=0, sticky="nw", padx=60, pady=(5, 0))

        value = ctk.CTkLabel(
            self.__totalInvoices_frame,
            text="1,247",
            font=ctk.CTkFont(size=45, weight="bold"),
            text_color="white"
        )
        value.grid(row=1, column=0, sticky="nw", padx=60, pady=(0, 50))

    def initMiddleframe(self):
        self.__middle_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR, corner_radius=15)
        self.__middle_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.__middle_frame.grid_propagate(False)
        self.__middle_frame.columnconfigure(0, weight=1)
        self.__middle_frame.columnconfigure(1, weight=1)
        self.__middle_frame.rowconfigure(0, weight=1)

        self.initPaidInvoicesFrame()
        self.initRecentActivityFrame()

    def initPaidInvoicesFrame(self):
        self.__paidInvoices_frame = ctk.CTkFrame(
            self.__middle_frame,
            fg_color=self.__WIDGET_COLOR,
            width=300,
            height=220,
            corner_radius=15,
        )
        self.__paidInvoices_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.__paidInvoices_frame.grid_propagate(False)
        self.__paidInvoices_frame.columnconfigure(0, weight=0)
        self.__paidInvoices_frame.columnconfigure(1, weight=1)
        self.__paidInvoices_frame.rowconfigure(0, weight=1)
        self.__paidInvoices_frame.rowconfigure(1, weight=1)

        label = ctk.CTkLabel(
            self.__paidInvoices_frame,
            text="Paid Invoices",
            font=CTkFont(family="Raleway SemiBold", size=30),
            text_color="white"
        )
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 0), sticky="w")

        green_square = ctk.CTkFrame(
            self.__paidInvoices_frame,
            fg_color="#39a274",
            width=100,
            height=100,
            corner_radius=10
        )
        green_square.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        green_square.grid_propagate(False)

        dollar_label = ctk.CTkLabel(
            green_square,
            text="$",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color="white"
        )
        dollar_label.place(relx=0.5, rely=0.5, anchor="center")

        value = ctk.CTkLabel(
            self.__paidInvoices_frame,
            text="1,224",
            font=ctk.CTkFont(size=45, weight="bold"),
            text_color="white"
        )
        value.grid(row=1, column=1, padx=35, sticky="w")

    def initRecentActivityFrame(self):
        self.__recentActivity_frame = ctk.CTkFrame(
            self.__middle_frame,
            fg_color="#623d40",
            width=300,
            height=220,
            corner_radius=15,
        )
        self.__recentActivity_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        self.__recentActivity_frame.grid_propagate(False)
        self.__recentActivity_frame.rowconfigure(0, weight=1)
        self.__recentActivity_frame.columnconfigure(1, weight=1)
        self.RecentActivityLabel()

    def RecentActivityLabel(self):
        self.__labelsemi_bold_font = CTkFont(family="Raleway SemiBold", size=30)
        label = ctk.CTkLabel(
            self.__recentActivity_frame,
            text="Recent Activity",
            font=self.__labelsemi_bold_font,
            text_color="white"
        )
        label.grid(row=0, column=0, sticky="nw", padx=30, pady=(40, 5))

        value = ctk.CTkLabel(
            self.__recentActivity_frame,
            text="Sent 100 Dollars $",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        value.grid(row=1, column=0, sticky="nw", padx=30, pady=(5, 30))

    def initBottomframe(self):
        self.__bottom_frame = ctk.CTkFrame(self, fg_color=self.__FRAME_COLOR, corner_radius=15)
        self.__bottom_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.__bottom_frame.grid_propagate(False)
        self.__bottom_frame.columnconfigure(0, weight=1)
        self.__bottom_frame.columnconfigure(1, weight=1)
        self.__bottom_frame.columnconfigure(2, weight=1)
        self.__bottom_frame.rowconfigure(0, weight=1)

        add_client_btn = ctk.CTkButton(
            self.__bottom_frame,
            text="Add Client",
            font=CTkFont(family="Raleway SemiBold", size=30),
            fg_color=self.__WIDGET_COLOR,
            hover_color="#3a3d44",
            text_color="white",
            corner_radius=15,
            height=220,
            command=lambda: self.controller.show_page("add_clients")
        )
        add_client_btn.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        create_invoice_btn = ctk.CTkButton(
            self.__bottom_frame,
            text="Create Invoice",
            font=CTkFont(family="Raleway SemiBold", size=30),
            fg_color=self.__WIDGET_COLOR,
            hover_color="#3a3d44",
            text_color="white",
            corner_radius=15,
            height=220,
            command=lambda: self.controller.show_page("add_invoice")
        )
        create_invoice_btn.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")

        add_payment_btn = ctk.CTkButton(
            self.__bottom_frame,
            text="Add Payment",
            font=CTkFont(family="Raleway SemiBold", size=30),
            fg_color=self.__WIDGET_COLOR,
            hover_color="#3a3d44",
            text_color="white",
            corner_radius=15,
            height=220,
            command=lambda: self.controller.show_page("payments")
        )
        add_payment_btn.grid(row=0, column=2, padx=(10, 0), pady=0, sticky="nsew")
