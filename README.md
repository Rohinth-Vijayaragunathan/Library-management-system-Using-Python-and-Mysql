# Library Management System

A **Python & MySQL based Library Management System** that allows admins to manage books and users to issue and return books.

---

## Features

### Admin
- Add, update, delete, and view books
- Search books by ID
- Secure admin login

### User
- View available books
- Issue books (quantity tracked automatically)
- Return books with fine calculation for overdue returns
- Secure user login

---

## Prerequisites

- Python 3.x
- MySQL Server
- Python library `pymysql`

Install dependencies using pip:

pip install pymysql

## Admin Menu

1. **Add book** – Add a new book to the library database.  
2. **Search book** – Search for a book by its ID.  
3. **View book** – View all books in the library.  
4. **Update book** – Update details of an existing book.  
5. **Delete book** – Remove a book from the library database.  
6. **Exit** – Exit the admin menu.

## User Menu

1. **View book** – View all available books in the library.  
2. **Issue book** – Borrow a book (quantity is updated automatically).  
3. **Return book** – Return a borrowed book (fines applied if overdue).  
4. **Logout** – Exit the user menu and return to the main menu.
