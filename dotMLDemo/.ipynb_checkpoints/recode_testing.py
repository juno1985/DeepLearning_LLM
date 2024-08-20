import random
import sqlite3
import unittest
from datetime import datetime, timedelta
from typing import Dict, List
import doctml_recode

class MyTestCase(unittest.TestCase):
    @staticmethod
    def create_dummy_data():
        conn = sqlite3.connect('shopy.db')
        c = conn.cursor()

        # skip function if tables already exist
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='my_orders'")
        if c.fetchone() is not None:
            return "Table already exists!"

        # Create tables
        c.execute('''
             CREATE TABLE my_orders (
                 id INTEGER PRIMARY KEY,
                 booking_date DATE,
                 country_id INTEGER,
                 status TEXT,
                 total INTEGER
             );
         ''')

        c.execute('''
             CREATE TABLE my_order_items (
                 id INTEGER PRIMARY KEY,
                 order_id INTEGER,
                 product_id INTEGER,
                 quantity INTEGER,
                 price INTEGER
             );
         ''')

        # Populate tables
        statuses = ['confirmed', 'shipped', 'delivered', 'cancelled']

        for i in range(1, 501):
            booking_date = datetime.now() - timedelta(days=random.randint(0, 60))
            country_id = random.randint(60, 75)
            status = random.choice(statuses)
            total = random.randint(5, 250)

            c.execute('INSERT INTO my_orders VALUES (?, ?, ?, ?, ?)', (i, booking_date, country_id, status, total))

            # For each order, create 1-5 order items
            for j in range(random.randint(1, 5)):
                product_id = random.randint(1, 20)
                quantity = random.randint(1, 10)
                price = random.randint(1, 100)
                c.execute('INSERT INTO my_order_items VALUES (?, ?, ?, ?, ?)',
                          (i * 10 + j, i, product_id, quantity, price))

        # Save (commit) the changes
        conn.commit()

        # Close the connection
        conn.close()

        return "table created!"
    @staticmethod
    def execute_against_dummy_data(query: str) -> List[Dict]:
        conn = sqlite3.connect('shopy.db')
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        conn.close()
        return rows
    
    def test_simple_test1(self):
        self.create_dummy_data()
        result = self.execute_against_dummy_data("select strftime('%Y-%m',my_orders.booking_date) as booking_date_month,sum(my_order_items.quantity) as sum_quantity from my_orders left join my_order_items on my_orders.id=my_order_items.order_id group by 1")
        print(result)

if __name__ == '__main__':
    unittest.main()