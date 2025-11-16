from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    password: str = ""
    is_admin: bool = False

@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0
    stock: int = 0
    flavor: str = ""
    image_url: str = ""

@dataclass
class Order:
    id: Optional[int] = None
    user_id: int = 0
    order_date: str = ""
    status: str = "Pending"
    total_price: float = 0.0

@dataclass
class OrderItem:
    id: Optional[int] = None
    order_id: int = 0
    product_id: int = 0
    quantity: int = 0
    price_per_unit: float = 0.0
