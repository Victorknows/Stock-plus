import sqlite3
import random

def initialize_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTO INCREMENT,
        username VARCHAR (200),
        role VARCHAR (200),
        created_at TIMESTAMP
    )
    ''')
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS products(
                  id INEGER PRIMARY KEY AUTOINCREMENT,
                  name VARCHAR (200),
                  category VARCHAR(200),
                  amount INTEGER,
                  quantity INTEGER,
                  user_id integer [ref: > users.id])''')
            
    c.execute('''
              CREATE TABLE IF NOT EXISTS orders(
                  id INTEGER PRIMARYKEY AUTOINCREMENT,
                  quantity INTEGER,
                  order_date timestamp,
                  status VARCHAR(200),
                  user_id INTEGER [ref: >users.id],
                  product_id INTEGER [ref: > products,id])''')          

def authenicate(username, pasword):
    conn= sqlite3.connect('database.id')
    c = conn.cursor()
    c.execute('''INSERT INTO user (username,password, role) VALUES (?,?,?)''',
              (username, hashlib.sha256(password.encode()).hexdigest(), role)
              ())
    conn.commit()
    conn.close()
    
def add_user(username, password, role='user'):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO user (username, password, role) VALUES (?, ?, ?)''',
              (username, hashlib.sha256(password.encode()).hexdigest(), role))
    conn.commit()
    conn.close()
    
def add_product(name, quantity, price, supplier, category, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()        
    c.execute('''INSER INTO proucts (name, quantity, price, supplier, category, user_id) VALUES(?, ?, ?, ?, ?, ?)''',
              (name, quantity, price, supplier, category,user_id))
    conn.commit()
    conn.close()
    
def place_order(product_id, user_id, quantity):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO orders (product_id, user_id, quantity, order_date, status)
              VALUES(?,?,?, datetime('now), 'pending')''',
              (product_id, user_id, quantity))
    conn.commit()    
    conn.close()
    
def view_all_products():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM products''')
    products = c.fetchall()
    conn.close()
    return products    

def view_all_orders():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM orders''')
    orders = c.fetchall()
    conn.close()
    return orders 

def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def main():
    initialize_database()
    
    print("Welcome to StockPlus")
    print("Please Login or Signup")
    
    while True:
        print("1. Login")
        print("1. Signup")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Enter your username: ")
            password = input("Input your password: ")
            user = authenicate(username, password)
            
            if user:
                print(f"Welcome {username}")
                break
            
            else:
                print("Invalid username or password")
                
        elif choice == "2":
            username = input("Create a new user: ")
            password = generate_random_password()
            print(f"Your password: {password}")
            role = input("Enter your role (user/admin): ").lower()
            if role not in ['user', 'admin']:
                print("Invalid role")
                role = 'user'
            add_user(username, password, role)
            print("User created Succesfully. Please login")
                        
        elif choice == "3":
            print("Exiting.....")
            return
        
        else: 
            print("Invalid choice")        