from decimal import Decimal
from datetime import datetime, timedelta
import random
from database import DatabaseManager
from models import Category, Product, Customer, Order, OrderItem

def generate_sample_data():
    db = DatabaseManager("ecommerce_sample.db")
    
    # Categories
    categories = [
        Category(name="Electronics", description="Electronic devices and accessories"),
        Category(name="Clothing", description="Apparel and fashion items"),
        Category(name="Books", description="Books and educational materials"),
        Category(name="Home & Garden", description="Home improvement and garden supplies"),
        Category(name="Sports", description="Sports and outdoor equipment")
    ]
    
    category_ids = []
    for category in categories:
        category_id = db.add_category(category)
        category_ids.append(category_id)
    
    # Products
    products_data = [
        ("Smartphone X1", "PHONE001", 0, Decimal("699.99"), Decimal("400.00"), 50),
        ("Wireless Headphones", "AUDIO001", 0, Decimal("159.99"), Decimal("80.00"), 100),
        ("Laptop Pro", "COMP001", 0, Decimal("1299.99"), Decimal("800.00"), 25),
        ("Cotton T-Shirt", "CLOTH001", 1, Decimal("24.99"), Decimal("12.00"), 200),
        ("Jeans Classic", "CLOTH002", 1, Decimal("59.99"), Decimal("30.00"), 150),
        ("Programming Guide", "BOOK001", 2, Decimal("39.99"), Decimal("15.00"), 75),
        ("Garden Hose", "GARDEN001", 3, Decimal("29.99"), Decimal("15.00"), 40),
        ("Tennis Racket", "SPORT001", 4, Decimal("89.99"), Decimal("45.00"), 30),
        ("Running Shoes", "SPORT002", 4, Decimal("119.99"), Decimal("60.00"), 80),
        ("Coffee Maker", "HOME001", 3, Decimal("79.99"), Decimal("40.00"), 60)
    ]
    
    product_ids = []
    for name, sku, cat_idx, price, cost, stock in products_data:
        product = Product(
            name=name,
            sku=sku,
            category_id=category_ids[cat_idx],
            price=price,
            cost=cost,
            stock_quantity=stock,
            description=f"High quality {name.lower()}"
        )
        product_id = db.add_product(product)
        product_ids.append(product_id)
    
    # Customers
    customers_data = [
        ("john.doe@email.com", "John", "Doe", "555-0101"),
        ("jane.smith@email.com", "Jane", "Smith", "555-0102"),
        ("bob.wilson@email.com", "Bob", "Wilson", "555-0103"),
        ("alice.brown@email.com", "Alice", "Brown", "555-0104"),
        ("charlie.davis@email.com", "Charlie", "Davis", "555-0105"),
        ("diana.miller@email.com", "Diana", "Miller", "555-0106"),
        ("edward.jones@email.com", "Edward", "Jones", "555-0107"),
        ("fiona.garcia@email.com", "Fiona", "Garcia", "555-0108")
    ]
    
    customer_ids = []
    for email, first, last, phone in customers_data:
        customer = Customer(
            email=email,
            first_name=first,
            last_name=last,
            phone=phone
        )
        customer_id = db.add_customer(customer)
        customer_ids.append(customer_id)
    
    # Generate orders over the last 30 days
    base_date = datetime.now() - timedelta(days=30)
    
    for day in range(30):
        order_date = base_date + timedelta(days=day)
        num_orders = random.randint(2, 8)
        
        for _ in range(num_orders):
            customer_id = random.choice(customer_ids)
            
            # Create order items
            items = []
            num_items = random.randint(1, 4)
            total_amount = Decimal('0.00')
            
            selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
            
            for product_id in selected_products:
                # Get product price (simplified - in real app would query DB)
                product_idx = product_ids.index(product_id)
                unit_price = products_data[product_idx][3]  # price from products_data
                quantity = random.randint(1, 3)
                total_price = unit_price * quantity
                
                item = OrderItem(
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                items.append(item)
                total_amount += total_price
            
            # Add shipping and tax
            shipping_cost = Decimal('9.99') if total_amount < 50 else Decimal('0.00')
            tax_amount = total_amount * Decimal('0.08')  # 8% tax
            final_total = total_amount + shipping_cost + tax_amount
            
            order = Order(
                customer_id=customer_id,
                order_date=order_date,
                status="completed",
                total_amount=final_total,
                shipping_cost=shipping_cost,
                tax_amount=tax_amount
            )
            
            db.create_order(order, items)
    
    print(f"Sample data generated successfully!")
    print(f"- {len(categories)} categories")
    print(f"- {len(products_data)} products")
    print(f"- {len(customers_data)} customers")
    print(f"- Orders generated for 30 days")

if __name__ == "__main__":
    generate_sample_data()