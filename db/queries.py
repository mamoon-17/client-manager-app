import mysql.connector
from mysql.connector import Error

class Queries:
    
    def __init__(self, connection):
        self.__cursor = connection.cursor()
        self.create_clients_table()
        self.create_invoices_table()
        self.create_inventory_items_table()
        self.create_activity_logs_table()
        self.create_payments_table()
        self.apply_constraints()

    def create_clients_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS clients (
                client_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) UNIQUE NOT NULL,
                company_name VARCHAR(100),
                notes TEXT
            );
            """
            self.__cursor.execute(query)
            print("Table 'clients' created or already exists.")
        except Error as e:
            print(f"Error creating clients table: {e}")

    def create_invoices_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                due_date DATE NOT NULL,
                invoice_date DATE NOT NULL,
                description TEXT,
                bank_name VARCHAR(100) NOT NULL,
                account_number VARCHAR(50) NOT NULL, 
                status ENUM('PAID', 'UNPAID') NOT NULL DEFAULT 'UNPAID',
                FOREIGN KEY (bank_name) REFERENCES clients(bank_name),
                FOREIGN KEY (account_number) REFERENCES clients(account_number),
                FOREIGN KEY (client_id) REFERENCES clients(client_id)
            );
            """
            self.__cursor.execute(query)
            print("Table 'invoices' created or already exists.")
        except Error as e:
            print(f"Error creating invoices table: {e}")

    def create_inventory_items_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS inventory_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                invoice_id INT NOT NULL,
                description TEXT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
            );
            """
            self.__cursor.execute(query)
            print("Table 'inventory_items' created or already exists.")
        except Error as e:
            print(f"Error creating inventory_items table: {e}")

    def create_activity_logs_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS activity_logs (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT,
                activity_type VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(client_id)
            );
            """
            self.__cursor.execute(query)
            print("Table 'activity_logs' created or already exists.")
        except Error as e:
            print(f"Error creating activity_logs table: {e}")

    def create_payments_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                invoice_id INT NOT NULL,
                amount_paid DECIMAL(10, 2) NOT NULL,
                payment_date DATE NOT NULL,
                FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
            );
            """
            self.__cursor.execute(query)
            print("Table 'payments' created or already exists.")
        except Error as e:
            print(f"Error creating payments table: {e}")

    def apply_constraints(self):
        try:
            # Check if constraints already exist before adding, otherwise MySQL will raise an error
            constraints = [
                "ALTER TABLE payments ADD CONSTRAINT chk_amount_paid_positive CHECK (amount_paid >= 0)",
                "ALTER TABLE inventory_items ADD CONSTRAINT chk_quantity_positive CHECK (quantity >= 0)",
                "ALTER TABLE inventory_items ADD CONSTRAINT chk_unit_price_positive CHECK (unit_price >= 0)"
            ]
            for constraint in constraints:
                try:
                    self.__cursor.execute(constraint)
                except Error as inner_e:
                    if "Duplicate" not in str(inner_e):
                        print(f"Constraint error: {inner_e}")
            print("Constraints applied.")
        except Error as e:
            print(f"Error applying constraints: {e}")

    def close(self):
        if self.__cursor:
            self.__cursor.close()
            print("Cursor closed.")

    def __del__(self):
        self.close()
