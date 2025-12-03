def validate_product_name(name: str) -> bool:
    """Validate product name"""
    return len(name) >= 3 and len(name) <= 100

def validate_price(price: float) -> bool:
    """Validate price"""
    return price > 0 and price < 1000000

def validate_stock(stock: int) -> bool:
    """Validate stock quantity"""
    return stock >= 0

def validate_customer_name(name: str) -> bool:
    """Validate customer name"""
    return len(name) >= 2 and name.replace(" ", "").isalpha()

def validate_phone_number(phone: str) -> bool:
    """Validate phone number"""
    digits = ''.join(filter(str.isdigit, phone))
    return len(digits) >= 10 and len(digits) <= 15
EOFALL

# Create analytics.py (completely unused module)
cat > sample_code2/analytics.py << 'EOFALL'
"""
Analytics and reporting - COMPLETELY UNUSED MODULE
"""
from typing import List, Dict
from datetime import datetime, timedelta

def calculate_revenue(orders: List[Dict]) -> float:
    """Calculate total revenue"""
    return sum(order.get('total', 0) for order in orders)

def get_best_selling_products(orders: List[Dict], limit: int = 10) -> List[Dict]:
    """Get best selling products"""
    product_counts = {}
    for order in orders:
        for item in order.get('items', []):
            product_id = item['product_id']
            product_counts[product_id] = product_counts.get(product_id, 0) + item['quantity']
    
    sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_products[:limit]

def calculate_average_order_value(orders: List[Dict]) -> float:
    """Calculate average order value"""
    if not orders:
        return 0.0
    return calculate_revenue(orders) / len(orders)

def get_customer_lifetime_value(customer_id: int, orders: List[Dict]) -> float:
    """Calculate customer lifetime value"""
    customer_orders = [o for o in orders if o.get('customer_id') == customer_id]
    return calculate_revenue(customer_orders)

def generate_sales_report(start_date: datetime, end_date: datetime) -> Dict:
    """Generate sales report for date range"""
    return {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': 0.0,
        'total_orders': 0,
        'average_order_value': 0.0
    }
