import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from generate_mock_data import get_mock_products

app = Flask(__name__)
CORS(app)

PRODUCTS_FILE = "products.json"

def load_products():
    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return get_mock_products()

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

@app.route('/api/products', methods=['GET'])
def api_products():
    products = load_products()
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def update_products():
    products = request.get_json()
    if not isinstance(products, list):
        return jsonify({"error": "Invalid data format"}), 400
    save_products(products)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)