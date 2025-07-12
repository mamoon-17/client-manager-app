import customtkinter as ctk
from customtkinter import CTkFont

class Root:
    def __init__(self):
        self.__root = None
        self.__sidebar_frame = None
        self.controller = None
        self.__SIDEBAR_COLOR = "#303338"
        self.__semi_bold_font = None

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Root window
        self.__root = ctk.CTk()
        self.__root.title("Client Manager")
        self.__root.state("zoomed")

        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight() - 70
        self.__root.geometry(f"{screen_width}x{screen_height}")
        self.__root.minsize(1024, 700)
        self.__root.resizable(True, True)

        self.__root.rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=0)
        self.__root.columnconfigure(1, weight=1)

        # Initialize
        self.initSidebar()

    def initSidebar(self):
        self.__sidebar_frame = ctk.CTkFrame(
            self.__root, fg_color=self.__SIDEBAR_COLOR, corner_radius=0, width=294
        )
        self.__sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.__sidebar_frame.grid_propagate(False)

        self.__sidebar_frame.columnconfigure(0, weight=1)
        self.DashboardButton()
        self.ClientButton()
        self.InvoiceButton()
        # self.TasksButton()  # ✅ Tasks button instead of payments
        self.addSidebarSeparator()
        self.QuitButton()

    def DashboardButton(self):
        self.__semi_bold_font = CTkFont(family="Raleway SemiBold", size=24)
        dashboard_Button = ctk.CTkButton(
            self.__sidebar_frame,
            text="Dashboard",
            font=self.__semi_bold_font,
            fg_color=self.__SIDEBAR_COLOR,
            text_color="white",
            hover_color="#3b4147",
            corner_radius=10,
            height=60,
            width=210,
            command=self.on_dashboard_click
        )
        dashboard_Button.grid(row=0, column=0, sticky="n", padx=10, pady=(50, 10))

    def ClientButton(self):
        client_button = ctk.CTkButton(
            self.__sidebar_frame,
            text="Clients",
            font=self.__semi_bold_font,
            fg_color=self.__SIDEBAR_COLOR,
            text_color="white",
            hover_color="#3b4147",
            corner_radius=10,
            height=60,
            width=210,
            command=self.on_clients_click
        )
        client_button.grid(row=1, column=0, sticky="n", padx=10, pady=10)

    def InvoiceButton(self):
        invoice_button = ctk.CTkButton(
            self.__sidebar_frame,
            text="Invoices",
            font=self.__semi_bold_font,
            fg_color=self.__SIDEBAR_COLOR,
            text_color="white",
            hover_color="#3b4147",
            corner_radius=10,
            height=60,
            width=210,
            command=self.on_invoices_click
        )
        invoice_button.grid(row=2, column=0, sticky="n", padx=10, pady=10)

    # def TasksButton(self):  # ✅ New method for tasks list
    #     tasks_button = ctk.CTkButton(
    #         self.__sidebar_frame,
    #         text="Tasks List",
    #         font=self.__semi_bold_font,
    #         fg_color=self.__SIDEBAR_COLOR,
    #         text_color="white",
    #         hover_color="#3b4147",
    #         corner_radius=10,
    #         height=60,
    #         width=210,
    #         command=self.on_tasks_click
    #     )
    #     tasks_button.grid(row=3, column=0, sticky="n", padx=10, pady=10)

    def QuitButton(self):
        quit_button = ctk.CTkButton(
            self.__sidebar_frame,
            text="⏻ Quit",
            font=self.__semi_bold_font,
            fg_color=self.__SIDEBAR_COLOR,
            text_color="white",
            hover_color="#3b4147",
            corner_radius=10,
            height=60,
            width=210,
            command=self.quit_app
        )
        quit_button.grid(row=4, column=0, sticky="n", padx=10, pady=(10, 10))

    def addSidebarSeparator(self):
        separator = ctk.CTkLabel(
            self.__sidebar_frame,
            text="─" * 40,
            text_color="#555"
        )
        separator.grid(row=3, column=0, pady=(10, 5))

    def inject_controller(self, controller):
        self.controller = controller

    def on_dashboard_click(self):
        if self.controller:
            self.controller.show_page("dashboard")

    def on_invoices_click(self):
        if self.controller:
            self.controller.show_page("invoices")

    def on_clients_click(self):
        if self.controller:
            self.controller.show_page("clients")

    # def on_tasks_click(self):  # ✅ Routing logic for tasks
    #     if self.controller:
    #         self.controller.show_page("tasks")

    def quit_app(self):
        self.__root.destroy()

    def get_root(self):
        return self.__root

    def run(self):
        self.__root.mainloop()
