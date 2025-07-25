from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

@dataclass
class Category:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    sku: str = ""
    category_id: Optional[int] = None
    price: Decimal = Decimal('0.00')
    cost: Optional[Decimal] = None
    description: Optional[str] = None
    stock_quantity: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Customer:
    id: Optional[int] = None
    email: str = ""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Order:
    id: Optional[int] = None
    customer_id: int = 0
    order_date: Optional[datetime] = None
    status: str = "pending"
    total_amount: Decimal = Decimal('0.00')
    shipping_cost: Decimal = Decimal('0.00')
    tax_amount: Decimal = Decimal('0.00')

@dataclass
class OrderItem:
    id: Optional[int] = None
    order_id: int = 0
    product_id: int = 0
    quantity: int = 0
    unit_price: Decimal = Decimal('0.00')
    total_price: Decimal = Decimal('0.00')

@dataclass
class SalesData:
    product_name: str = ""
    sku: str = ""
    category: str = ""
    total_quantity_sold: int = 0
    total_revenue: Decimal = Decimal('0.00')
    avg_selling_price: Decimal = Decimal('0.00')
    number_of_orders: int = 0