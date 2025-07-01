# gui/page_manager.py
from gui.dashboard import Dashboard
from gui.invoice_form import InvoicesPage
from gui.clients import Clients

class PageManager:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.pages = {}

    def show_page(self, name):
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["column"]) == 1:
                widget.grid_forget()

        if name == "dashboard":
            if "dashboard" not in self.pages:
                self.pages["dashboard"] = Dashboard(self.root, self.db)
            self.pages["dashboard"].grid(row=0, column=1, sticky="nsew")

        elif name == "invoices":
            if "invoices" not in self.pages:
                self.pages["invoices"] = InvoicesPage(self.root, self.db)
            self.pages["invoices"].grid(row=0, column=1, sticky="nsew")

        elif name == "clients":
            if "clients" not in self.pages:
                self.pages["clients"] = Clients(self.root, self.db)
            self.pages["clients"].grid(row=0, column=1, sticky="nsew")
