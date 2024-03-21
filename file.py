import sqlite3


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

def authenicate(username,pasword):
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
    
