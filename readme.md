# Client Manager App

A sleek, modern client and invoice management system built with **Python**, **CustomTkinter**, and **MySQL**, designed for freelancers, agencies, or small businesses to efficiently manage clients, tasks, and payments.

---

## Features

- Add, view, and manage clients (with encrypted notes).
- Create, track, and manage invoices.
- **Generate PDF invoices** using `fpdf` for sharing and archiving.
- **Send invoices via email** using Gmail SMTP with secure `.env` app credentials.
- Task list with filters (priority, starred, completed).
- Dashboard showing:
  - Total clients
  - Total invoices
  - Paid invoice summary
  - Recent activity feed
- Activity log to track user actions (e.g., tasks, clients).
- Modular navigation system using a custom `PageManager`.

---

## 🛠 Tech Stack

| Layer          | Tech                                                            |
| -------------- | --------------------------------------------------------------- |
| UI Framework   | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| DBMS           | MySQL                                                           |
| Queries        | Raw SQL (`mysql-connector-python`)                              |
| Encryption     | Fernet (for secure notes)                                       |
| PDF Generator  | [fpdf](https://pyfpdf.readthedocs.io/en/latest/)                |
| Email Sender   | Python's `smtplib` + Gmail App Password                         |
| Styling        | Material-inspired dark theme                                    |
| Python Version | 3.10+                                                           |

---

## Project Structure

```

client-manager-app/
├── db/
│   └── db\_config.py              # MySQL connection + cursor
├── gui/
│   ├── root\_window\.py            # Root CTk app setup
│   ├── page\_manager.py           # Handles page navigation
│   ├── dashboard.py              # Dashboard page
│   ├── clients.py                # All clients list
│   ├── add\_clients.py            # Add client form
│   ├── invoices.py               # Invoice list
│   ├── invoice\_form.py           # Add invoice form
│   ├── activity\_log\_page.py      # Activity log viewer
│   ├── TasksPage.py              # Task manager with filters
├── utils/
│   ├── encryption.py             # Note encryption helpers
│   ├── email\_utils.py            # Email sending helpers (SMTP)
│   └── pdf\_generator.py          # FPDF invoice generator
├── .env                          # Environment secrets (NOT committed)
├── main.py                       # App entry point
└── requirements.txt

```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mamoon-17/client-manager-app.git
cd client-manager-app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root with your Gmail SMTP credentials:

```
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

### 4. Run the app

```bash
python main.py
```

---

## Design Philosophy

This app follows:

- Modular, page-based GUI architecture
- Clean, dark UI with CustomTkinter
- PDF and email integrations for real-world use
- Minimal dependencies, extensible logic
- Designed to help freelancers and small teams track clients and tasks efficiently
