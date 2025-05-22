from flask import Flask, jsonify
from generate_mock_data import get_mock_products

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def api_products():
    """API endpoint to get mock product data."""
    products = get_mock_products()
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)
