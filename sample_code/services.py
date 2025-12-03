from models import Product, Customer
from typing import List, Optional

class ProductService:
    """Service for product operations"""
    
    def __init__(self):
        self.products = {}
    
    def add_product(self, product: Product) -> None:
        """Add product to catalog - USED"""
        self.products[product.product_id] = product
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID - USED"""
        return self.products.get(product_id)
    
    def search_products(self, query: str) -> List[Product]:
        """Search products - UNUSED"""
        results = []
        for product in self.products.values():
            if query.lower() in product.name.lower():
                results.append(product)
        return results
    
    def get_out_of_stock(self) -> List[Product]:
        """Get out of stock products - UNUSED"""
        return [p for p in self.products.values() if p.stock == 0]
    
    def bulk_update_prices(self, price_map: dict) -> None:
        """Bulk update prices - COMPLETELY UNUSED"""
        for product_id, new_price in price_map.items():
            if product_id in self.products:
                self.products[product_id].price = new_price
    
    def export_catalog(self) -> dict:
        """Export catalog to dict - COMPLETELY UNUSED"""
        return {pid: p.__dict__ for pid, p in self.products.items()}


class CustomerService:
    """Service for customer operations - MOSTLY UNUSED"""
    
    def __init__(self):
        self.customers = {}
    
    def add_customer(self, customer: Customer) -> None:
        """Add customer - UNUSED"""
        self.customers[customer.customer_id] = customer
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get customer - UNUSED"""
        return self.customers.get(customer_id)
    
    def update_email(self, customer_id: int, new_email: str) -> bool:
        """Update customer email - UNUSED"""
        if customer_id in self.customers:
            self.customers[customer_id].email = new_email
            return True
        return False
    
    def get_vip_customers(self) -> List[Customer]:
        """Get VIP customers - COMPLETELY UNUSED"""
        return [c for c in self.customers.values() if c.loyalty_points > 1000]


class DiscountService:
    """Service for discount calculations - COMPLETELY UNUSED CLASS"""
    
    def __init__(self):
        self.discount_codes = {}
    
    def add_discount_code(self, code: str, percentage: float):
        self.discount_codes[code] = percentage
    
    def validate_code(self, code: str) -> bool:
        return code in self.discount_codes
    
    def get_discount_amount(self, code: str, amount: float) -> float:
        if code in self.discount_codes:
            return amount * (self.discount_codes[code] / 100)
        return 0.0
