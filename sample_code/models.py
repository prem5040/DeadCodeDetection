from datetime import datetime
from typing import List, Optional

class Product:
    """Product model"""
    
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.created_at = datetime.now()
    
    def get_price(self) -> float:
        """Get product price - USED"""
        return self.price
    
    def apply_discount(self, percentage: float) -> float:
        """Apply discount - USED"""
        return self.price * (1 - percentage / 100)
    
    def update_stock(self, quantity: int) -> None:
        """Update stock quantity - UNUSED"""
        self.stock += quantity
    
    def is_available(self) -> bool:
        """Check availability - USED"""
        return self.stock > 0
    
    def get_tax(self) -> float:
        """Calculate tax - UNUSED"""
        return self.price * 0.1
    
    def archive_product(self) -> None:
        """Archive old product - COMPLETELY UNUSED"""
        self.archived = True
        self.archived_at = datetime.now()


class Customer:
    """Customer model"""
    
    def __init__(self, customer_id: int, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.loyalty_points = 0
    
    def get_name(self) -> str:
        """Get customer name - USED"""
        return self.name
    
    def add_loyalty_points(self, points: int) -> None:
        """Add loyalty points - UNUSED"""
        self.loyalty_points += points
    
    def redeem_points(self, points: int) -> bool:
        """Redeem loyalty points - UNUSED"""
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            return True
        return False
    
    def get_tier(self) -> str:
        """Get customer tier - COMPLETELY UNUSED"""
        if self.loyalty_points > 1000:
            return "Gold"
        elif self.loyalty_points > 500:
            return "Silver"
        return "Bronze"


class Order:
    """Order model - COMPLETELY UNUSED CLASS"""
    
    def __init__(self, order_id: int, customer_id: int):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = []
        self.total = 0.0
    
    def add_item(self, product_id: int, quantity: int, price: float):
        self.items.append({
            'product_id': product_id,
            'quantity': quantity,
            'price': price
        })
        self.calculate_total()
    
    def calculate_total(self):
        self.total = sum(item['price'] * item['quantity'] for item in self.items)
    
    def apply_coupon(self, code: str) -> bool:
        return False
