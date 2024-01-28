from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Welcome to the superheroes API</h1>'

# Get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

# Get a specific hero by ID
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        result = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": hero_power.power.id, "name": hero_power.power.name, "description": hero_power.power.description}
                for hero_power in hero.hero_powers
            ],
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Hero not found"}), 404

# Get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

# Get a specific power by ID
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return make_response(jsonify({'error': 'Power not found'}), 404)

# Update a power by ID
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        data = request.get_json()
        power.description = data.get('description', power.description)
        try:
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 400)
    else:
        return make_response(jsonify({'error': 'Power not found'}), 404)

# Create a new HeroPower
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if hero_id is None or power_id is None or strength is None:
        return make_response(jsonify({'errors': ['Missing required data']}), 400)

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return make_response(jsonify({'errors': ['Hero or Power not found']}), 404)

    new_hero_power = HeroPower(hero=hero, power=power, strength=strength)

    try:
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': [{'id': power.id, 'name': power.name, 'description': power.description}]})
    except Exception as e:
        return make_response(jsonify({'errors': [str(e)]}), 400)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
