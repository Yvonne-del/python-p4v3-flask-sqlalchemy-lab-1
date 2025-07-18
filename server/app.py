# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_view_by_id(id):
    quake = Earthquake.query.filter(Earthquake.id == id).first()
    
    if quake:
        d = {
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
        }

        return make_response(jsonify(d), 200)
    else:
        response = {
                    "message": f"Earthquake {id} not found."
                    }
        return make_response(jsonify(response), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = Earthquake.query.filter(Earthquake.magnitude >= magnitude).count()
    arr = []
    for i in range(len(quakes)):
        v = {
            'id': quakes[i].id,
            'location': quakes[i].location,
            'magnitude': quakes[i].magnitude,
            'year': quakes[i].year
        }
        arr.append(v)
        
    response = {
        'count': count,
        'quakes': arr
    }
    return make_response(jsonify(response), 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
