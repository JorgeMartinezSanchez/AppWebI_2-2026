import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models.models import Base, Food

app = Flask(__name__)

engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def food_to_dict(food):
    return {
        "id": str(food.id),
        "food_category_id": str(food.food_category_id),
        "name": food.name,
        "description": food.description,
        "price": float(food.price) if food.price is not None else None,
    }


@app.route('/food', methods=['GET'])
def get_foods():
    session = Session()
    try:
        foods = session.query(Food).all()
        result = [food_to_dict(f) for f in foods]
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return jsonify(result)


@app.route('/food/<uuid:food_id>', methods=['GET'])
def get_food(food_id):
    session = Session()
    food = session.get(Food, food_id)
    session.close()
    if food is None:
        return jsonify({"error": "no encontrado"}), 404
    return jsonify(food_to_dict(food))


@app.route('/food', methods=['POST'])
def create_food():
    try:
        data = request.json
        session = Session()
        food = Food(
            food_category_id=data["food_category_id"],
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
        )
        session.add(food)
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({"error": str(e)}), 400
    finally: 
        session.commit()
        result = food_to_dict(food)
        session.close()

    return jsonify(result), 201


@app.route('/food/<uuid:food_id>', methods=['PUT'])
def update_food(food_id):
    try:
        data = request.json
        session = Session()
        food = session.get(Food, food_id)
        if food is None:
            session.close()
            return jsonify({"error": "no encontrado"}), 404
        for campo in ("food_category_id", "name", "description", "price"):
            if campo in data:
                setattr(food, campo, data[campo])
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        result = food_to_dict(food)
        session.close()
    return jsonify(result)


@app.route('/food/<uuid:food_id>', methods=['DELETE'])
def delete_food(food_id):
    try:
        session = Session()
        food = session.get(Food, food_id)
        if food is None:
            session.close()
            return jsonify({"error": "no encontrado"}), 404
        session.delete(food)
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
    return jsonify({"mensaje": "eliminado"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')