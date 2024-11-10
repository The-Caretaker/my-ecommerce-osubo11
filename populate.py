from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if different
db = client['ecommerce_db'] # Database name
product_collection = db.products  # Collection name

# Sample product data
products = [
    {
        "name": "Wireless Mouse",
        "description": "A smooth and reliable wireless mouse.",
        "category": "Electronics",
        "price": 15.99
    },
    {
        "name": "Bluetooth Speaker",
        "description": "Portable Bluetooth speaker with excellent sound quality.",
        "category": "Electronics",
        "price": 49.99
    },
    {
        "name": "Running Shoes",
        "description": "Comfortable running shoes for all-day wear.",
        "category": "Footwear",
        "price": 75.00
    },
    {
        "name": "Office Chair",
        "description": "Ergonomic office chair with lumbar support.",
        "category": "Furniture",
        "price": 150.00
    },
    {
        "name": "Coffee Maker",
        "description": "Brews rich and flavorful coffee in minutes.",
        "category": "Home Appliances",
        "price": 35.50
    },
    {
        "name": "Yoga Mat",
        "description": "Non-slip yoga mat for safe and comfortable workouts.",
        "category": "Fitness",
        "price": 20.00
    },
    {
        "name": "Desk Lamp",
        "description": "LED desk lamp with adjustable brightness.",
        "category": "Home Decor",
        "price": 22.50
    },
    {
        "name": "Smart Watch",
        "description": "Track your fitness and receive notifications.",
        "category": "Electronics",
        "price": 120.00
    },
    {
        "name": "Water Bottle",
        "description": "Insulated water bottle keeps drinks cold for hours.",
        "category": "Accessories",
        "price": 12.99
    },
    {
        "name": "Cookware Set",
        "description": "Non-stick cookware set with pots and pans.",
        "category": "Kitchen",
        "price": 80.00
    }
]

# Insert sample data into the products collection
product_collection.insert_many(products)
print("Database populated with sample products.")
