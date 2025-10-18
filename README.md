# 🍽️ TableTap – QR-Driven Digital Menu & Ordering Platform

**TableTap** is a multi-tenant SaaS web application built with **Django**, designed for restaurants to digitize the dining experience.
Customers can scan a **table-specific QR code** to view a live menu, place orders, and track their status — all without downloading an app.
Restaurant owners manage menus, tables, and orders through a dynamic dashboard, while superusers oversee system-wide operations.

---

## 🧩 Key Features

### 🏗️ Core Platform

* **Multi-Tenant SaaS Architecture:** Each restaurant operates independently with isolated data.
* **Secure Authentication:** Supports role-based access for admin, restaurant owners, and customers.
* **Superuser Dashboard:** Manage restaurant accounts, data consistency, and system security.
* **Restaurant Owner Dashboard:** CRUD for menu categories, menu items, and table management.
* **QR Code Generation:** Automatically generates unique QR codes per table using the `qrcode` Python library.

### 🍽️ Customer Experience

* **Scan-to-Order:** Customers scan QR codes to access a live, table-specific digital menu.
* **Interactive Menu:** Categorized, mobile-responsive layout built with **Tailwind CSS**.
* **Instant Ordering:** Orders are sent directly to the restaurant dashboard in real time.
* **Order Confirmation:** Users receive on-screen confirmation with dynamic order summaries.

### ⚙️ Advanced Feature

* **Real-Time Order Status Dashboard:**
  Restaurant staff can view all active orders, filter by table, and update statuses (`Pending → Preparing → Completed`).
  Statuses are visually color-coded and update instantly for clarity and speed.

---

## 🖥️ Tech Stack

| Layer         | Technology                    |
| ------------- | ----------------------------- |
| **Framework** | Django                        |
| **Frontend**  | Tailwind CSS                  |
| **Database**  | MySQL (PostgreSQL compatible) |
| **QR Code**   | Python `qrcode` library       |

---

## 🗂️ Project Structure

```
📦 tabletap/
├── accounts/                 # Authentication & user management
├── restaurant/               # Owner dashboard, menu & order logic
├── customer/                 # Customer-facing QR ordering interface
├── static/                   # Tailwind CSS and assets
├── templates/                # HTML templates (landing, menu, dashboard, etc.)
├── db.sqlite3                # Development database
└── manage.py
```

---

## 🔒 Accessibility & Usability

* Semantic HTML structure for assistive technologies
* High color contrast & readable typography
* Fully keyboard-navigable interfaces
* Responsive design optimized for mobile and desktop
