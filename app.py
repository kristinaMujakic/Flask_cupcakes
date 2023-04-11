"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '555'

with app.app_context():
    connect_db(app)


@app.route('/')
def homepage():
    '''Render homepage'''

    return render_template('index.html')


@app.route('/api/cupcakes')
def all_cupcakes():
    '''Data about all cupcakes'''

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cup_id>')
def single_cupcake(cup_id):
    '''Data about a single cupcake'''
    cupcake = Cupcake.query.get_or_404(cup_id)

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Create a cupcake with the Cupcake model'''

    new_cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'],
                          rating=request.json['rating'], image=request.json['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:cup_id>', methods=['PATCH'])
def update_cupcake(cup_id):
    '''Updates a particular cupcake'''

    cupcake = Cupcake.query.get_or_404(cup_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cup_id>', methods=['DELETE'])
def delete_cupcake(cup_id):
    '''Deletes a particular cupcake'''

    cupcake = Cupcake.query.get_or_404(cup_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Cupcake removed!')
