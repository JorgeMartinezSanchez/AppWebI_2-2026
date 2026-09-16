from flask import Flask, render_template, request, jsonfy

import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
db = SQLAlchemy(app)


with app.app_context():
    db.create_all()

@app.route('/food', methods=['GET'])
def get_item():
    return jsonify({"mensaje": "GET recibido"})

@app.route('/food', methods=['POST'])
def create_item():
    data = request.json
    return jsonify({"mensaje": "POST recibido", "data": data}), 201

@app.route('/food/<int:food_id>', methods=['PUT'])
def update_item(food_id):
    data = request.json
    return jsonify({"mensaje": f"PUT recibido para id {food_id}", "data": data})

@app.route('/food/<int:food_id>', methods=['DELETE'])
def delete_item(food_id):
    return jsonify({"mensaje": f"DELETE recibido para id {food_id}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')