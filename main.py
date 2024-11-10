from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
import hashlib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce_db']

users_collection = db['users']
products_collection = db['products']
interactions_collection = db['user_interactions']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalog', methods=['GET'])
def get_catalog():
    products = products_collection.find()
    product_list = []
    for product in products:
        product_list.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "description": product["description"],
            "category": product["category"],
            "price": product["price"],
            "image_url": product.get("image_url", "")
        })
    return jsonify(product_list)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password_hash = data.get('password')

    if not username or not email or not password_hash:
        return jsonify({"message": "All fields are required"}), 400

    existing_user = users_collection.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        return jsonify({"message": "User with this username or email already exists"}), 409

    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": password_hash
    })

    return jsonify({"message": "User registered successfully", "success": True}), 201

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    product = {
        "name": data['name'],
        "description": data['description'],
        "category": data['category'],
        "price": data['price']
    }
    products_collection.insert_one(product)
    return jsonify({"message": "Product added successfully"}), 201

@app.route('/search_products', methods=['GET'])
def search_products():
    query = request.args.get('query')
    if not query:
        return jsonify([])

    search_results = products_collection.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}}
        ]
    })

    products = []
    for product in search_results:
        products.append({
            "name": product["name"],
            "description": product["description"],
            "category": product["category"],
            "price": product["price"]
        })

    return jsonify(products)


@app.route('/interact', methods=['POST'])
def interact():
    data = request.json
    interaction = {
        "user_id": data['user_id'],
        "product_id": data['product_id'],
        "interaction_type": data['interaction_type'],
        "timestamp": data.get('timestamp', pd.Timestamp.now())
    }
    interactions_collection.insert_one(interaction)
    return jsonify({"message": "Interaction recorded"}), 201


def get_user_product_matrix():
    interactions = list(interactions_collection.find())
    df = pd.DataFrame(interactions)
    user_product_matrix = df.pivot_table(index='user_id', columns='product_id', aggfunc='size', fill_value=0)
    return user_product_matrix

@app.route('/recommend/<user_id>', methods=['GET'])
def recommend(user_id):
    matrix = get_user_product_matrix()
    if user_id not in matrix.index:
        return jsonify({"message": "User has no interactions"}), 404
    
    user_vector = matrix.loc[user_id].values.reshape(1, -1)
    similarity_matrix = cosine_similarity(user_vector, matrix)
    recommendations = matrix.columns[np.argsort(similarity_matrix.flatten())[::-1]]
    recommended_products = list(products_collection.find({"_id": {"$in": recommendations[:5]}}))
    return jsonify(recommended_products)


if __name__ == '__main__':
    app.run(debug=True)
