from flask import Flask, request, jsonify

app = Flask(__name__)
def get_api_data(api_url):
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None

api_url = "http://localhost:3000"

products = get_api_data(api_url)

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify({"product": product})
    return jsonify({"message": "Product not found"}), 404

@app.route('/admin/products', methods=['POST'])
def create_product():
    new_product = {
        'id': len(products) + 1,
        'code': request.json['code'],
        'name': request.json['name'],
        'description': request.json['description'],
        'price': request.json['price'],
        'quantity': request.json['quantity'],
        'inventoryStatus': request.json['inventoryStatus'],
        'category': request.json['category'],
        'image': request.json['image'],
        'rating': request.json['rating']

    }
    products.append(new_product)
    return jsonify({"message": "Product created", "product": new_product}), 201

@app.route('/admin/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        product['code'] = request.json.get('code', product['code'])
        product['name'] = request.json.get('name', product['name'])
        product['description'] = request.json.get('description', product['description'])
        product['price'] = request.json.get('price', product['price'])
        product['quantity'] = request.json.get('quantity', product['quantity'])
        product['inventoryStatus'] = request.json.get('inventoryStatus', product['inventoryStatus'])
        product['category'] = request.json.get('category', product['category'])
        product['image'] = request.json.get('image', product['image'])
        product['rating'] = request.json.get('rating', product['rating'])
        return jsonify({"message": "Product updated", "product": product})
    return jsonify({"message": "Product not found"}), 404

@app.route('/admin/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({"message": "Product deleted"})


