from datetime import date
import pymysql

connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "library_DB"
)

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Admin(admin_id INT PRIMARY KEY,username varchar(30),password varchar(30))")
print("table admin created successfully")

cursor.execute("CREATE TABLE IF NOT EXISTS User(user_id INT PRIMARY KEY,username VARCHAR(30),password VARCHAR(30))")
print("table user created successfully")

cursor.execute("CREATE TABLE IF NOT EXISTS Books(book_id INT PRIMARY KEY,title VARCHAR(30),author VARCHAR(30),quantity INT)")
print("table books created successfully")

cursor.execute("""CREATE TABLE IF NOT EXISTS Issued_books( issue_id INT PRIMARY KEY AUTO_INCREMENT,user_id INT,book_id INT,issue_date DATE,
return_date DATE,fine INT DEFAULT 0)""")
print("table issued books created successfully)
      
connection.commit()

def admin_login():
    u = input("enter username: ")
    p = input("enter password: ")
    cursor.execute("select * from Admin where username = %s and password = %s",(u,p))

    if cursor.fetchone():
        admin_menu()
    else:
        print("Invalid admin login")

def user_login():
    u = input("enter username: ")
    p = input("enter password: ")

    cursor.execute("select * from User where username = %s and password = %s",(u,p))
    user = cursor.fetchone()

    if user:
        user_menu(user[0])
    else:
        print("Invalid user login")
                    # admin functions
def add_book(title,author,quantity):
    sql = "INSERT INTO Books (title,author,quantity) values (%s,%s,%s)"
    values = (title,author,quantity)
    cursor.execute(sql,values)
    connection.commit()
    print("book added successfully")

def search_book(book_id):
    cursor.execute("select * from Books where book_id = %s",(book_id,))
    row = cursor.fetchone()

    if row:
        print("book found ",row)
    else:
        print("book not found")

def view_book():
    cursor.execute("select * from Books")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def update_book(book_id,title,author,quantity):
    sql = "update Books set title = %s, author = %s, quantity = %s where book_id = %s"
    values = (book_id,title,author,quantity)
    cursor.execute(sql,values)
    connection.commit()
    print("book updated successfully")

def delete_book(book_id):
    cursor.execute("delete from Books where book_id = %s",(book_id,))
    connection.commit()
    print("book deleted successfully")

def admin_menu():
    while True:
        print("1. add book")
        print("2. search book")
        print("3. view book")
        print("4. update book")
        print("5. delete book")
        print("6. exiting program")
        
        choice = int(input("enter the choice: "))

        if choice == 1:
            title = input("enter title: ")
            author = input("enter author name: ")
            quantity = input("enter number of quantity: ")
            add_book(title,author,quantity)
        elif choice == 2:
            book_id = input("enter book-id to search: ")
            search_book(book_id)
        elif choice == 3:
            view_book()
        elif choice == 4:
            book_id = input("enter the book-id to update: ")
            title = input("enter new title: ")
            author = input("enter new author: ")
            quantity = input("enter new quantity: ")
            update_book(book_id,title,author,quantity)
        elif choice == 5:
            book_id = input("enter book_id to delete: ")
            delete_book(book_id)
        elif choice == 6:
            print("exiting program")
            break

# user functions
def issue_book(user_id):
    book_id = int(input("enter book-id: "))
    cursor.execute("select quantity from Books where book_id = %s",(book_id,))
    qty = cursor.fetchone()

    if qty and qty[0] > 0:
        cursor.execute("insert into Issued_books (user_id,book_id,issue_date) values %s,%s,%s",(user_id,book_id,date.today()))
        cursor.execute("update Books set quantity = quantity - 1 where book_id = %s",(book_id,))
        connection.commit()
        print("book issued!")
    else:
        print("book not available!")

def return_book(user_id):
    issue_id = int(input("enter issue_id: "))
    cursor.execute("select issue_date,book_id from Issued_Books where issue_id = %s and user_id = %s",(issue_id,user_id))
    record = cursor.fetchone()

    if record:
        issue_id = record[0]
        book_id = record[1]
        days = (date.today() - issue_date).days
        fine = 0

        if days > 7:
            fine = (days - 7)*5

        cursor.execute("update Issued_Books set return_date = %s,fine = %s where issue_id=%s",(date.today(),fine,issue_id)) 
        cursor.execute("update Books set quantity = quantity + 1 where book_id=%s",(book_id,))
        connection.commit()
        print("book returned | fine: ",fine)
    else:
        print("Invalid issue-id")

# user menu
def user_menu(user_id):
    while True:
        print("1. view book")
        print("2. issue book")
        print("3. return book")
        print("4. logout")

        choice = int(input("enter choice: "))
        
        if choice == 1:
            view_book()
        elif choice == 2:
            issue_book(user_id)
        elif choice == 3:
            return_book(user_id)
        else:
            print("logout from user menu")
            break
    
# main menu
while True:
    print("\n1. admin login\n2. user login\n3. Exit")
    choice = int(input("enter choice: "))

    if choice == 1:
        admin_login()
    elif choice == 2:
        user_login()
    else:
        print("exiting program")
        break
