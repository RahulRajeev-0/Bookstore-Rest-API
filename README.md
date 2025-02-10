# Bookstore Application Backend 

### API Documentation 
```
https://documenter.getpostman.com/view/31743247/2sAYX9mLAU
```

# 📚 Bookstore API

## 📝 Overview
This is the **backend API** for a **Bookstore Application**, built using **Django REST Framework (DRF)**. The API supports **JWT-based authentication** and allows users to manage books, reviews, and authors.

## 🚀 Features
- **JWT Authentication** (Login & Signup)
- CRUD operations for books and reviews
- Soft delete functionality for books
- Author management
- Filtering books by authors
- Secure endpoints requiring authentication

## 🏗️ Installation Guide

### Prerequisites
- Python 3.8+
- Virtual Environment (`venv`)
- PostgreSQL (or SQLite for development)

### 🔧 Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/bookstore-api.git
   cd bookstore-api
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables** (Create a `.env` file)
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3  # Change this for production
   ```

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## 🔑 Authentication (JWT)
The API uses **JWT (JSON Web Token)** for authentication.
- **Signup**: `POST /api/auth/signup/`
- **Login**: `POST /api/auth/login/` → Returns an `access_token` & `refresh_token`
- **Refresh Token**: `POST /api/auth/token/refresh/`

👉 **Important:** Apart from **signup and login**, every other endpoint **requires an `Authorization: Bearer <access_token>` header** in the request.

## 📌 API Documentation
For detailed API endpoints and request/response formats, refer to the **API documentation**:
🔗 **[API Docs](https://documenter.getpostman.com/view/31743247/2sAYX9mLAU)**

## ✅ Running Tests
To run unit tests, execute:
```bash
python manage.py test
```

### 🔍 Test Cases Ensure:
- Authentication via JWT works correctly
- Books and reviews are created, updated, and deleted as expected
- Soft deletion functionality is working
- Protected endpoints reject unauthorized access

## 📜 License
This project is licensed under the **MIT License**.

---
🚀 Happy Coding!

