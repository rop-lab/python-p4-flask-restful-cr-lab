#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    # GET method to retrieve all plants
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.serialize() for plant in plants])
    
    # POST method to add a new plant
    def post(self):
        data = request.json
        new_plant = Plant(name=data.get('name'), image=data.get('image'), price=data.get('price'))
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.serialize()), 201

class PlantByID(Resource):
    # GET method to retrieve a plant by ID
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)
        return jsonify(plant.serialize())

    # PUT method to update a plant by ID
    def put(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        data = request.json
        plant.name = data.get('name', plant.name)
        plant.image = data.get('image', plant.image)
        plant.price = data.get('price', plant.price)
        db.session.commit()
        return jsonify(plant.serialize())

    # DELETE method to delete a plant by ID
    def delete(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        db.session.delete(plant)
        db.session.commit()
        return '', 204

    # GET method to retrieve all plants (Index Route)
    def index(self):
        plants = Plant.query.all()
        return jsonify([plant.serialize() for plant in plants])

    # GET method to retrieve a plant by ID (Show Route)
    def show(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)
        return jsonify(plant.serialize())

    # POST method to add a new plant (Create Route)
    def create(self):
        data = request.json
        new_plant = Plant(name=data.get('name'), image=data.get('image'), price=data.get('price'))
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.serialize()), 201

# Add the Plants resource to the '/plants' endpoint
api.add_resource(Plants, '/plants')

# Add the PlantByID resource to the '/plants/<int:plant_id>' endpoint
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
