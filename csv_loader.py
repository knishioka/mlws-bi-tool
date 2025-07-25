import csv
import os
from typing import List
from decimal import Decimal
from datetime import datetime
from database import DatabaseManager
from models import Category, Product, Customer, Order, OrderItem

class CSVLoader:
    def __init__(self, db_path: str = "ecommerce.db", data_dir: str = "data"):
        self.db = DatabaseManager(db_path)
        self.data_dir = data_dir
    
    def load_categories(self) -> List[int]:
        category_ids = []
        csv_path = os.path.join(self.data_dir, "categories.csv")
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = Category(
                    name=row['name'],
                    description=row['description']
                )
                category_id = self.db.add_category(category)
                category_ids.append(category_id)
        
        return category_ids
    
    def load_products(self) -> List[int]:
        product_ids = []
        csv_path = os.path.join(self.data_dir, "products.csv")
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    name=row['name'],
                    sku=row['sku'],
                    category_id=int(row['category_id']),
                    price=Decimal(row['price']),
                    cost=Decimal(row['cost']) if row['cost'] else None,
                    description=row['description'],
                    stock_quantity=int(row['stock_quantity']),
                    is_active=bool(int(row['is_active']))
                )
                product_id = self.db.add_product(product)
                product_ids.append(product_id)
        
        return product_ids
    
    def load_customers(self) -> List[int]:
        customer_ids = []
        csv_path = os.path.join(self.data_dir, "customers.csv")
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer = Customer(
                    email=row['email'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    phone=row['phone']
                )
                customer_id = self.db.add_customer(customer)
                customer_ids.append(customer_id)
        
        return customer_ids
    
    def load_orders_and_items(self):
        orders_path = os.path.join(self.data_dir, "orders.csv")
        items_path = os.path.join(self.data_dir, "order_items.csv")
        
        # Load order items into memory first
        order_items_dict = {}
        with open(items_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                order_id = int(row['order_id'])
                if order_id not in order_items_dict:
                    order_items_dict[order_id] = []
                
                item = OrderItem(
                    product_id=int(row['product_id']),
                    quantity=int(row['quantity']),
                    unit_price=Decimal(row['unit_price']),
                    total_price=Decimal(row['total_price'])
                )
                order_items_dict[order_id].append(item)
        
        # Load orders and create them with their items
        with open(orders_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                order_id = int(row['id'])
                order = Order(
                    customer_id=int(row['customer_id']),
                    order_date=datetime.fromisoformat(row['order_date']),
                    status=row['status'],
                    total_amount=Decimal(row['total_amount']),
                    shipping_cost=Decimal(row['shipping_cost']),
                    tax_amount=Decimal(row['tax_amount'])
                )
                
                items = order_items_dict.get(order_id, [])
                self.db.create_order(order, items)
    
    def load_all_data(self):
        print("Loading data from CSV files...")
        
        print("1. Loading categories...")
        category_ids = self.load_categories()
        print(f"   Loaded {len(category_ids)} categories")
        
        print("2. Loading products...")
        product_ids = self.load_products()
        print(f"   Loaded {len(product_ids)} products")
        
        print("3. Loading customers...")
        customer_ids = self.load_customers()
        print(f"   Loaded {len(customer_ids)} customers")
        
        print("4. Loading orders and order items...")
        self.load_orders_and_items()
        print("   Orders and items loaded")
        
        print("Data loading completed successfully!")

if __name__ == "__main__":
    loader = CSVLoader("ecommerce_csv.db")
    loader.load_all_data()