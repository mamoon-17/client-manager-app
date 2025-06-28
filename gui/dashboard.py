import customtkinter as ctk
from customtkinter import CTkFont

class Dashboard(ctk.CTkFrame):
    def __init__(self, root, db):
        super().__init__(root)

        self.__db = db
        # Pre-declare frames (safe access)
        self.__root = root
        self.__main_frame = None
        self.__top_frame = None
        self.__middle_frame = None
        self.__bottom_frame = None
        self.__totalClients_frame = None
        self.__totalInvoices_frame = None
        self.__paidInvoices_frame = None
        self.__recentActivity_frame = None
        self.__addClient_frame = None
        self.__createInvoice_frame = None
        self.__addPayment_frame = None

        # Colors
        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"
        
        self.__semi_bold_font = None

        # Init layout
        self.initMainframe()

    def initMainframe(self):
        self.__main_frame = ctk.CTkFrame(
            self.__root, fg_color=self.__FRAME_COLOR, corner_radius=0
        )
        self.__main_frame.grid(row=0, column=1, sticky="nsew")

        # Allow vertical resizing
        self.__main_frame.rowconfigure(0, weight=1)
        self.__main_frame.rowconfigure(1, weight=1)
        self.__main_frame.rowconfigure(2, weight=1)
        self.__main_frame.columnconfigure(0, weight=1)

        self.initTopframe()
        self.initMiddleframe()
        self.initBottomframe()

    def initTopframe(self):
        self.__top_frame = ctk.CTkFrame(
            self.__main_frame, fg_color=self.__FRAME_COLOR, corner_radius=15
        )
        self.__top_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        self.__top_frame.grid_propagate(False)

        self.__top_frame.columnconfigure(0, weight=1)  # <-- added: enable first column to expand
        self.__top_frame.columnconfigure(1, weight=1)  # <-- added: enable second column to expand
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
        self.__totalClients_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.__totalClients_frame.grid_propagate(False)
        self.__totalClients_frame.columnconfigure(0, weight=1)
        self.__totalClients_frame.rowconfigure(0, weight=1)
        self.totalClientsLabel()

    def totalClientsLabel(self):
        self.__labelsemi_bold_font = CTkFont(family="Raleway SemiBold", size=28)
        totalClients_Label = ctk.CTkLabel(
        self.__totalClients_frame,
        text="Total Clients",
        font=self.__labelsemi_bold_font,
        text_color="white",               # Valid for CTkLabel
        height=150
        )
        totalClients_Label.grid(row=0, column=0, sticky="nw", padx=60, pady=(20, 0))

        totalClients_Value = ctk.CTkLabel(
        self.__totalClients_frame,
        text="146",  # Dynamic value can go here
        font=ctk.CTkFont(size=32, weight="bold"),  # You can tweak font
        text_color="white"
        )
        totalClients_Value.grid(row=1, column=0, sticky="nw", padx=60, pady=(0, 50))


    def initTotalInvoicesFrame(self):
        self.__totalInvoices_frame = ctk.CTkFrame(
        self.__top_frame,
        fg_color=self.__WIDGET_COLOR,
        width=300,
        height=220,
        corner_radius=15,
    )
        self.__totalInvoices_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        self.__totalInvoices_frame.grid_propagate(False)
        self.__totalInvoices_frame.rowconfigure(0, weight=1)
        self.__totalInvoices_frame.columnconfigure(1, weight=1)


    def initMiddleframe(self):
        self.__middle_frame = ctk.CTkFrame(
            self.__main_frame, fg_color=self.__FRAME_COLOR, corner_radius=15
        )
        self.__middle_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.__middle_frame.grid_propagate(False)

        self.__middle_frame.columnconfigure(0, weight=1)  # <-- added: enable first column to expand
        self.__middle_frame.columnconfigure(1, weight=1)  # <-- added: enable second column to expand
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
        self.__paidInvoices_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.__paidInvoices_frame.grid_propagate(False)
        self.__paidInvoices_frame.columnconfigure(0, weight=1)
        self.__paidInvoices_frame.rowconfigure(0, weight=1)

    def initRecentActivityFrame(self):
        self.__recentActivity_frame = ctk.CTkFrame(
        self.__middle_frame,
        fg_color=self.__WIDGET_COLOR,
        width=300,
        height=220,
        corner_radius=15,
    )
        self.__recentActivity_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        self.__recentActivity_frame.grid_propagate(False)
        self.__recentActivity_frame.rowconfigure(0, weight=1)
        self.__recentActivity_frame.columnconfigure(1, weight=1)

    def initBottomframe(self):
        self.__bottom_frame = ctk.CTkFrame(
            self.__main_frame, fg_color=self.__FRAME_COLOR, corner_radius=15
        )
        self.__bottom_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.__bottom_frame.grid_propagate(False)

        self.__bottom_frame.columnconfigure(0, weight=1)  # <-- added: enable first column to expand
        self.__bottom_frame.columnconfigure(1, weight=1)  # <-- added: enable second column to expand
        self.__bottom_frame.columnconfigure(2, weight=1)  # <-- added: enable second column to expand
        self.__bottom_frame.rowconfigure(0, weight=1)

        self.initAddClientFrame()
        self.initCreateInvoiceFrame()
        self.initaddPaymentFrame()

    def initAddClientFrame(self):
        self.__addClient_frame = ctk.CTkFrame(
            self.__bottom_frame,
            fg_color=self.__WIDGET_COLOR,
            width=300,
            height=220,
            corner_radius=15,
        )
        self.__addClient_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.__addClient_frame.grid_propagate(False)
        self.__addClient_frame.columnconfigure(0, weight=1)
        self.__addClient_frame.rowconfigure(0, weight=1)

    def initCreateInvoiceFrame(self):
        self.__createInvoice_frame = ctk.CTkFrame(
        self.__bottom_frame,
        fg_color=self.__WIDGET_COLOR,
        width=300,
        height=220,
        corner_radius=15,
    )
        self.__createInvoice_frame.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")
        self.__createInvoice_frame.grid_propagate(False)
        self.__createInvoice_frame.rowconfigure(0, weight=1)
        self.__createInvoice_frame.columnconfigure(1, weight=1)

    def initaddPaymentFrame(self):
        self.__addPayment_frame = ctk.CTkFrame(
        self.__bottom_frame,
        fg_color=self.__WIDGET_COLOR,
        width=300,
        height=220,
        corner_radius=15,
    )
        self.__addPayment_frame.grid(row=0, column=2, padx=(10, 0), pady=0, sticky="nsew")
        self.__addPayment_frame.grid_propagate(False)
        self.__addPayment_frame.rowconfigure(0, weight=1)
        self.__addPayment_frame.columnconfigure(2, weight=1)