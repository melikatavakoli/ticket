# 🎫 Ticket Management System / سیستم مدیریت تیکت

## 🌐 English Version

This is a **Ticket Management System** built with **Django** and **Django REST Framework**.
It allows users and staff to create, reply, and track tickets in a professional workflow.

### ✨ Features

* 🆕 **Create, update, and manage tickets**
* 👥 **Assign staff to tickets**
* ⚡ **Set ticket priorities and types**
* 📊 **Track ticket status** (Open, In Progress, Closed)
* ⏱️ **User-friendly relative timestamps**
* 📎 **Attachments for ticket details**
* 🔒 **Permission control** (Admin, Staff, User)
* 🌐 **API ready for frontend integration**

### 🛠️ Tech Stack

* 🐍 Python 3.11+
* 🖥️ Django 4.3+
* ⚡ Django REST Framework 3.20+
* 🗄️ PostgreSQL (optional, default SQLite)
* 🔑 JWT Authentication
* 🔍 Django Filter & Search
* 📁 File upload support

### 🚀 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/ticket-system.git
cd ticket-system
```

2. **Create virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Apply migrations**:

```bash
python manage.py migrate
```

5. **Create superuser**:

```bash
python manage.py createsuperuser
```

6. **Run server**:

```bash
python manage.py runserver
```
