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

# @app.route('/api/cupcakes')
# def all_cupcakes():
#     cupcakes=Cupcake.query.all()
#     return render_template('index.html', cupcakes=cupcakes)
    

