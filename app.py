from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

app.app_context().push()
connect_db(app)

@app.route('/')
def index():
    cupcakes=Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def all_cupcakes():
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)
# to.dict() is called to turn each cupcake into a dictionary. This allows us to convert a model instance (Cupcake) to JSON for use in Flask routes or API responses.

@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():
    
    data = request.json
    
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image']
    )
    
    db.session.add(new_cupcake)
    db.session.commit()
    
    res_json = jsonify(new_cupcake.to_dict())
    return(res_json, 201)
    

@app.route('/api/cupcakes/<int:cup_id>')
def single_cupcake(cup_id):
    cupcake = Cupcake.query.get_or_404(cup_id)
    return jsonify(cupcake = cupcake.to_dict())
# the id of the item must be consistent all throughout. see: cup_id anf notice where it is being use... in the URL, as a paramater, and through the get_or_404. 