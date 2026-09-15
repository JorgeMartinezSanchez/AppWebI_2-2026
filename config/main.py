from flask import Flask, render_template, request, jsonfy
import SQLAlchemy

app = Flask(__name__)

@app.route('/food', methods=['GET'])
def get_item():
    return jsonify({"mensaje": "GET recibido"})

@app.route('/item', methods=['POST'])
def create_item():
    data = request.json
    return jsonify({"mensaje": "POST recibido", "data": data}), 201

@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    return jsonify({"mensaje": f"PUT recibido para id {item_id}", "data": data})

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return jsonify({"mensaje": f"DELETE recibido para id {item_id}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')