from models import Product, Customer
from services import ProductService
from utils import format_price

def create_sample_catalog():
    """Create sample product catalog - USED"""
    service = ProductService()
    
    product1 = Product(1, "Laptop", 999.99, 10)
    product2 = Product(2, "Mouse", 29.99, 50)
    product3 = Product(3, "Keyboard", 79.99, 30)
    
    service.add_product(product1)
    service.add_product(product2)
    service.add_product(product3)
    
    return service

def display_catalog(service: ProductService):
    """Display product catalog - USED"""
    print("=== Product Catalog ===")
    for product_id, product in service.products.items():
        price_str = format_price(product.get_price())
        available = "Available" if product.is_available() else "Out of Stock"
        print(f"{product.name}: {price_str} - {available}")
        
        discount_price = product.apply_discount(10)
        print(f"  10% off: {format_price(discount_price)}")

def process_order():
    """Process an order - UNUSED"""
    print("Processing order...")
    pass

def send_confirmation_email(customer: Customer, order_details: dict):
    """Send order confirmation - COMPLETELY UNUSED"""
    print(f"Sending email to {customer.email}")
    print(f"Order details: {order_details}")

def calculate_loyalty_points(order_total: float) -> int:
    """Calculate loyalty points - COMPLETELY UNUSED"""
    return int(order_total * 0.1)

def main():
    """Main function"""
    print("Starting E-commerce Application")
    
    catalog = create_sample_catalog()
    display_catalog(catalog)
    
    print("\nApplication completed successfully!")

if __name__ == "__main__":
    main()
