import tkinter as tk

class Dashboard:
    def __init__(self, db):
        self.__db = db

        self.root = tk.Tk()
        self.root.title("Client Manager")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.resizable(True, True)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        main_frame = tk.Frame(self.root, bg="white")
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        label = tk.Label(main_frame, text="Welcome to Client Manager", font=("Arial", 32), bg="white")
        label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def run(self):
        self.root.mainloop()
