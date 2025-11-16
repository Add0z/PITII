import sys
import os
import sqlite3

# Add the parent directory to the Python path to allow for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import database as db
from data.data_models import User, Product

def seed_data():
    """Populates the database with mock data."""
    
    # Ensure tables are created
    db.create_tables()
    print("Tables created or already exist.")

    # --- Mock Users ---
    users = [
        User(name="Admin User", email="admin@cupcake.com", password="admin123", is_admin=True),
        User(name="Customer User", email="customer@cupcake.com", password="customer123", is_admin=False)
    ]

    print("Seeding users...")
    for user in users:
        try:
            db.add_user(user)
            print(f"  - Added user: {user.email}")
        except sqlite3.IntegrityError:
            print(f"  - User {user.email} already exists. Skipping.")

    # --- Mock Products ---
    products = [
        Product(name="Classic Vanilla", description="A timeless vanilla cupcake with creamy frosting.", price=2.50, stock=50, flavor="Vanilla", image_url="images/classic_vanilla.jpg"),
        Product(name="Rich Chocolate", description="Decadent chocolate cupcake with a fudge center.", price=3.00, stock=40, flavor="Chocolate", image_url="images/rich_chocolate.jpg"),
        Product(name="Red Velvet", description="Classic red velvet with cream cheese frosting.", price=3.25, stock=30, flavor="Red Velvet", image_url="images/red_velvet.jpg"),
        Product(name="Lemon Zest", description="A zesty lemon cupcake with a light citrus glaze.", price=2.75, stock=25, flavor="Lemon", image_url="images/lemon_zest.jpg"),
        Product(name="Carrot Cake", description="Spiced carrot cupcake with walnuts and cream cheese frosting.", price=3.50, stock=20, flavor="Carrot", image_url="images/carrot_cake.jpg"),
        Product(name="Strawberry Bliss", description="Sweet strawberry cupcake with fresh berry frosting.", price=3.00, stock=35, flavor="Strawberry", image_url="images/strawberry_bliss.jpg"),
        Product(name="Chocolate Peanut Butter", description="A perfect combo of chocolate cake and peanut butter frosting.", price=3.50, stock=20, flavor="Chocolate", image_url="images/chocolate_peanut_butter.jpg"),
    ]

    print("\nSeeding products...")
    # To avoid duplicates, we'll only add if the database is empty
    if not db.get_all_products():
        for product in products:
            db.add_product(product)
            print(f"  - Added product: {product.name}")
    else:
        print("  - Products table is not empty. Skipping product seeding.")

    print("\nMock data seeding complete!")

if __name__ == "__main__":
    seed_data()
