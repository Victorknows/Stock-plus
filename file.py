import sqlite3
import hashlib
import random
import string

# Database Initialization
def initialize_database():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user'
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    supplier TEXT NOT NULL,
                    category TEXT NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    product_id INTEGER,
                    user_id INTEGER,
                    quantity INTEGER,
                    order_date TEXT,
                    status TEXT,
                    approved_by_user_id INTEGER,
                    FOREIGN KEY(product_id) REFERENCES products(id),
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(approved_by_user_id) REFERENCES users(id)
                 )''')


    conn.commit()
    conn.close()


# User Authentication
def authenticate(username, password):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''SELECT id, username, role FROM users WHERE username = ? AND password = ?''',
              (username, hashlib.sha256(password.encode()).hexdigest()))
    user = c.fetchone()
    conn.close()
    return user

# Add a user
def add_user(username, password, role='user'):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password, role) VALUES (?, ?, ?)''',
              (username, hashlib.sha256(password.encode()).hexdigest(), role))
    conn.commit()
    conn.close()

# Add a product to the inventory
def add_product(name, quantity, price, supplier, category, user_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''INSERT INTO products (name, quantity, price, supplier, category, user_id) VALUES (?, ?, ?, ?, ?, ?)''',
              (name, quantity, price, supplier, category, user_id))
    conn.commit()
    conn.close()

# Place an order
def place_order(product_id, user_id, quantity):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''INSERT INTO orders (product_id, user_id, quantity, order_date, status, approved_by_user_id) 
                 VALUES (?, ?, ?, datetime('now'), 'pending', NULL)''',
              (product_id, user_id, quantity))
    conn.commit()
    conn.close()

# Approve an order
def approve_order(order_id, user_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''UPDATE orders SET status = 'approved', approved_by_user_id = ? WHERE id = ?''',
              (user_id, order_id))
    conn.commit()
    conn.close()

# View all products
def view_all_products():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM products''')
    products = c.fetchall()
    conn.close()
    return products

# View all orders
def view_all_orders():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM orders''')
    orders = c.fetchall()
    conn.close()
    return orders

# Generate random password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Main function to interact with the system
def main():
    initialize_database()

    print("Welcome to the Inventory Management System!")
    print("Please login or sign up.")

    while True:
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = authenticate(username, password)
            if user:
                print(f"Welcome, {username}!")
                break
            else:
                print("Invalid username or password. Please try again.")

        elif choice == '2':
            username = input("Enter new username: ")
            password = generate_password()
            print(f"Generated password: {password}")
            role = input("Enter user role (user/admin): ").lower()
            if role not in ['user', 'admin']:
                print("Invalid role. Defaulting to 'user'.")
                role = 'user'
            add_user(username, password, role)
            print("User created successfully! Please login with the generated password.")

        elif choice == '3':
            print("Exiting...")
            return

        else:
            print("Invalid choice. Please try again.")

    if user[2] == 'admin':
        while True:
            print("\n1. View all Products")
            print("2. Place an Order")
            print("3. View all Orders")
            print("4. Logout")
            admin_choice = input("Enter your choice: ")

            if admin_choice == '1':
                print("All Products:")
                products = view_all_products()
                for product in products:
                    print(product)

            elif admin_choice == '2':
                print("Available Products:")
                products = view_all_products()
                for product in products:
                    print(product)
                product_id = int(input("Enter product ID to order: "))
                quantity = int(input("Enter quantity: "))
                place_order(product_id, user[0], quantity)
                print("Order placed successfully!")

            elif admin_choice == '3':
                print("All Orders:")
                orders = view_all_orders()
                for order in orders:
                    print(order)

            elif admin_choice == '4':
                print("Logging out...")
                break

            else:
                print("Invalid choice. Please try again.")
    else:
        while True:
            print("\n1. Add a Product")
            print("2. Approve an Order")
            print("3. Logout")
            user_choice = input("Enter your choice: ")

            if user_choice == '1':
                name = input("Enter product name: ")
                quantity = int(input("Enter quantity: "))
                price = float(input("Enter price: "))
                supplier = input("Enter supplier: ")
                category = input("Enter category: ")
                add_product(name, quantity, price, supplier, category, user[0])
                print("Product added successfully!")

            elif user_choice == '2':
                print("Available Orders:")
                orders = view_all_orders()
                for order in orders:
                    print(order)
                order_id = int(input("Enter order ID to approve: "))
                approve_order(order_id, user[0])
                print("Order approved successfully!")

            elif user_choice == '3':
                print("Logging out...")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

