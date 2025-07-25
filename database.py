import sqlite3
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from models import Product, Category, Customer, Order, OrderItem, SalesData

class DatabaseManager:
    def __init__(self, db_path: str = "ecommerce.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with open('schema.sql', 'r') as f:
            schema = f.read()
        
        conn = sqlite3.connect(self.db_path)
        conn.executescript(schema)
        conn.close()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def add_category(self, category: Category) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (category.name, category.description)
        )
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return category_id
    
    def add_product(self, product: Product) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO products (name, sku, category_id, price, cost, description, stock_quantity, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (product.name, product.sku, product.category_id, float(product.price), 
             float(product.cost) if product.cost else None, product.description, 
             product.stock_quantity, product.is_active)
        )
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id
    
    def add_customer(self, customer: Customer) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (email, first_name, last_name, phone) VALUES (?, ?, ?, ?)",
            (customer.email, customer.first_name, customer.last_name, customer.phone)
        )
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return customer_id
    
    def create_order(self, order: Order, items: List[OrderItem]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_cost, tax_amount)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (order.customer_id, order.order_date or datetime.now(), order.status,
                 float(order.total_amount), float(order.shipping_cost), float(order.tax_amount))
            )
            order_id = cursor.lastrowid
            
            for item in items:
                cursor.execute(
                    """INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                       VALUES (?, ?, ?, ?, ?)""",
                    (order_id, item.product_id, item.quantity, 
                     float(item.unit_price), float(item.total_price))
                )
            
            conn.commit()
            return order_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_sales_summary(self) -> List[SalesData]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_summary")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            SalesData(
                product_name=row['product_name'],
                sku=row['sku'],
                category=row['category'],
                total_quantity_sold=row['total_quantity_sold'],
                total_revenue=Decimal(str(row['total_revenue'])),
                avg_selling_price=Decimal(str(row['avg_selling_price'])),
                number_of_orders=row['number_of_orders']
            )
            for row in rows
        ]
    
    def get_products(self) -> List[Product]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE is_active = 1")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Product(
                id=row['id'],
                name=row['name'],
                sku=row['sku'],
                category_id=row['category_id'],
                price=Decimal(str(row['price'])),
                cost=Decimal(str(row['cost'])) if row['cost'] else None,
                description=row['description'],
                stock_quantity=row['stock_quantity'],
                is_active=bool(row['is_active']),
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            )
            for row in rows
        ]