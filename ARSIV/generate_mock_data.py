import json

def get_mock_products():
    """Generates a list of mock product data."""
    products = [
        {
            "id": 1,
            "name": "Laptop",
            "description": "A high-performance laptop suitable for all your needs.",
            "price": 1200.00
        },
        {
            "id": 2,
            "name": "Coffee Mug",
            "description": "A ceramic coffee mug to keep your beverages warm.",
            "price": 15.99
        },
        {
            "id": 3,
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with long battery life.",
            "price": 25.50
        },
        {
            "id": 4,
            "name": "Keyboard",
            "description": "Mechanical keyboard with RGB lighting.",
            "price": 75.00
        },
        {
            "id": 5,
            "name": "Webcam",
            "description": "HD webcam for video conferencing.",
            "price": 45.00
        },
        {
            "id": 6,
            "name": "Desk Lamp",
            "description": "Adjustable LED desk lamp.",
            "price": 30.25
        },
        {
            "id": 7,
            "name": "Notebook",
            "description": "A5 lined notebook for your notes and ideas.",
            "price": 7.99
        }
    ]
    return products

if __name__ == "__main__":
    mock_data = get_mock_products()
    print(json.dumps(mock_data, indent=4))
