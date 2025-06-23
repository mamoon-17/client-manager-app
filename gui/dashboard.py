import customtkinter as ctk

class Dashboard:
    def __init__(self, db):
        self.__db = db

        # Pre-declare frames (safe access)
        self.__root = None
        self.__main_frame = None
        self.__sidebar_frame = None
        self.__top_frame = None
        self.__middle_frame = None
        self.__bottom_frame = None
        self.__totalClients_frame = None

        # Colors
        self.__SIDEBAR_COLOR = "#303338"
        self.__WIDGET_COLOR = "#303339"
        self.__FRAME_COLOR = "#23262b"
        self.__temp_color = "#747679"

        # Appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        # Root window
        self.__root = ctk.CTk()
        self.__root.title("Client Manager")
        self.__root.state("zoomed")

        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        self.__root.geometry(f"{screen_width}x{screen_height}")
        self.__root.minsize(800, 600)
        self.__root.resizable(True, True)

        self.__root.rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=0)
        self.__root.columnconfigure(1, weight=1)

        # Init layout
        self.initSidebar()
        self.initMainframe()

    def initSidebar(self):
        self.__sidebar_frame = ctk.CTkFrame(
            self.__root, fg_color=self.__SIDEBAR_COLOR, corner_radius=0, width=310
        )
        self.__sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.__sidebar_frame.grid_propagate(False)

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
            self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15
        )
        self.__top_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        self.__top_frame.grid_propagate(False)
        self.__top_frame.columnconfigure(0, weight=1)
        self.__top_frame.rowconfigure(0, weight=1)

        self.initTotalClientsFrame()

    def initMiddleframe(self):
        self.__middle_frame = ctk.CTkFrame(
            self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15
        )
        self.__middle_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.__middle_frame.grid_propagate(False)

    def initBottomframe(self):
        self.__bottom_frame = ctk.CTkFrame(
            self.__main_frame, fg_color=self.__WIDGET_COLOR, corner_radius=15
        )
        self.__bottom_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.__bottom_frame.grid_propagate(False)

    def initTotalClientsFrame(self):
        self.__totalClients_frame = ctk.CTkFrame(
            self.__top_frame,
            fg_color=self.__temp_color,
            width=300,
            height=220,
            corner_radius=15,
        )
        self.__totalClients_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        self.__totalClients_frame.grid_propagate(False)

    def run(self):
        self.__root.mainloop()