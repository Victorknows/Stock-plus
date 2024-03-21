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

