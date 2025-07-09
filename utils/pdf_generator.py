from fpdf import FPDF
from datetime import datetime

class InvoicePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "INVOICE", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def invoice_body(self, invoice, client):
        self.set_font("Arial", size=12)
        self.cell(100, 10, f"Client Name: {client['name']}", ln=True)
        self.cell(100, 10, f"Email: {client['email']}", ln=True)
        self.cell(100, 10, f"Phone: {client['phone']}", ln=True)
        self.cell(100, 10, f"Company: {client['company_name']}", ln=True)
        self.ln(10)
        self.cell(100, 10, f"Invoice Date: {invoice['invoice_date']}", ln=True)
        self.cell(100, 10, f"Due Date: {invoice['due_date']}", ln=True)
        self.cell(100, 10, f"Amount: ${invoice['amount']}", ln=True)
        self.multi_cell(0, 10, f"Description: {invoice['description']}")
        self.cell(100, 10, f"Status: {invoice['status']}", ln=True)

def generate_invoice_pdf(invoice, client, save_path):
    pdf = InvoicePDF()
    pdf.add_page()
    pdf.invoice_body(invoice, client)
    pdf.output(save_path)
