from typing import List, Dict, Any
from decimal import Decimal
from datetime import datetime, timedelta
from database import DatabaseManager
from models import SalesData

class SalesAnalyzer:
    def __init__(self, db_path: str = "ecommerce_sample.db"):
        self.db = DatabaseManager(db_path)
    
    def get_sales_summary(self) -> List[SalesData]:
        return self.db.get_sales_summary()
    
    def get_top_selling_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        sales_data = self.get_sales_summary()
        sorted_products = sorted(sales_data, key=lambda x: x.total_quantity_sold, reverse=True)
        
        return [
            {
                "product_name": product.product_name,
                "sku": product.sku,
                "category": product.category,
                "quantity_sold": product.total_quantity_sold,
                "revenue": float(product.total_revenue),
                "avg_price": float(product.avg_selling_price)
            }
            for product in sorted_products[:limit]
        ]
    
    def get_revenue_by_category(self) -> Dict[str, float]:
        sales_data = self.get_sales_summary()
        category_revenue = {}
        
        for product in sales_data:
            category = product.category
            revenue = float(product.total_revenue)
            
            if category in category_revenue:
                category_revenue[category] += revenue
            else:
                category_revenue[category] = revenue
        
        return dict(sorted(category_revenue.items(), key=lambda x: x[1], reverse=True))
    
    def get_daily_sales_report(self, days: int = 7) -> List[Dict[str, Any]]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            DATE(o.order_date) as sale_date,
            COUNT(DISTINCT o.id) as total_orders,
            SUM(o.total_amount) as total_revenue,
            AVG(o.total_amount) as avg_order_value,
            SUM(oi.quantity) as total_items_sold
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        WHERE o.order_date >= date('now', '-{} days')
        GROUP BY DATE(o.order_date)
        ORDER BY sale_date DESC
        """.format(days)
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "date": row['sale_date'],
                "total_orders": row['total_orders'],
                "total_revenue": float(row['total_revenue']),
                "avg_order_value": float(row['avg_order_value']),
                "total_items_sold": row['total_items_sold']
            }
            for row in rows
        ]
    
    def print_sales_report(self):
        print("=== E-COMMERCE SALES REPORT ===\n")
        
        # Top selling products
        print("TOP 5 SELLING PRODUCTS:")
        top_products = self.get_top_selling_products(5)
        for i, product in enumerate(top_products, 1):
            print(f"{i}. {product['product_name']} ({product['sku']})")
            print(f"   Category: {product['category']}")
            print(f"   Quantity Sold: {product['quantity_sold']}")
            print(f"   Revenue: ${product['revenue']:.2f}")
            print(f"   Avg Price: ${product['avg_price']:.2f}\n")
        
        # Revenue by category
        print("REVENUE BY CATEGORY:")
        category_revenue = self.get_revenue_by_category()
        for category, revenue in category_revenue.items():
            print(f"- {category}: ${revenue:.2f}")
        print()
        
        # Daily sales (last 7 days)
        print("DAILY SALES (LAST 7 DAYS):")
        daily_sales = self.get_daily_sales_report(7)
        for day in daily_sales:
            print(f"{day['date']}: {day['total_orders']} orders, ${day['total_revenue']:.2f} revenue")

if __name__ == "__main__":
    analyzer = SalesAnalyzer()
    analyzer.print_sales_report()