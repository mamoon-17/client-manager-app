# gui/page_manager.py
from gui.dashboard import Dashboard
from gui.invoices import InvoicesPage
from gui.clients import Clients
from gui.add_clients import AddClientsPage
from gui.invoice_form import AddInvoicesPage
from gui.payments import PaymentsPage


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
                self.pages["dashboard"].inject_controller(self)
            self.pages["dashboard"].grid(row=0, column=1, sticky="nsew")

        elif name == "invoices":
            if "invoices" not in self.pages:
                self.pages["invoices"] = InvoicesPage(self.root, self.db)
                self.pages["invoices"].inject_controller(self)
            self.pages["invoices"].grid(row=0, column=1, sticky="nsew")

        elif name == "add_invoice":
            if "add_invoice" not in self.pages:
                self.pages["add_invoice"] = AddInvoicesPage(self.root, self.db)
                self.pages["add_invoice"].inject_controller(self) 
            self.pages["add_invoice"].grid(row=0, column=1, sticky="nsew")

        elif name == "clients":
            if "clients" not in self.pages:
                self.pages["clients"] = Clients(self.root, self.db)
                self.pages["clients"].inject_controller(self)
            self.pages["clients"].grid(row=0, column=1, sticky="nsew")

        elif name == "add_clients":
            if "add_clients" not in self.pages:
                self.pages["add_clients"] = AddClientsPage(self.root, self.db)
                self.pages["add_clients"].inject_controller(self)
            self.pages["add_clients"].grid(row=0, column=1, sticky="nsew")
        
        elif name == "payments":
            if "payments" not in self.pages:
                self.pages["payments"] = PaymentsPage(self.root, self.db)
                self.pages["payments"].inject_controller(self)
            self.pages["payments"].grid(row=0, column=1, sticky="nsew")

    def get_page(self, name):
        return self.pages.get(name)

