import json
import csv
from datetime import datetime
from typing import Any, Dict, List

def format_price(price: float) -> str:
    """Format price with currency - USED"""
    return f"${price:.2f}"

def format_date(date: datetime) -> str:
    """Format date - UNUSED"""
    return date.strftime("%Y-%m-%d %H:%M:%S")

def validate_email(email: str) -> bool:
    """Validate email format - UNUSED"""
    return "@" in email and "." in email.split("@")[1]

def generate_invoice_number() -> str:
    """Generate unique invoice number - COMPLETELY UNUSED"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"INV-{timestamp}"

def calculate_shipping_cost(weight: float, distance: float) -> float:
    """Calculate shipping cost - COMPLETELY UNUSED"""
    base_cost = 5.0
    weight_cost = weight * 0.5
    distance_cost = distance * 0.1
    return base_cost + weight_cost + distance_cost

def export_to_json(data: Dict[str, Any], filename: str) -> None:
    """Export data to JSON - COMPLETELY UNUSED"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def export_to_csv(data: List[Dict], filename: str) -> None:
    """Export data to CSV - COMPLETELY UNUSED"""
    if not data:
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def sanitize_input(user_input: str) -> str:
    """Sanitize user input - COMPLETELY UNUSED"""
    dangerous_chars = ['<', '>', '&', '"', "'"]
    sanitized = user_input
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized
