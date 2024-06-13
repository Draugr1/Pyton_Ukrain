from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///infrastructure1.db'

db = SQLAlchemy(app)

class Infrastructure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    position = db.Column(db.String(50))

    def __init__(self, name, type, position):
        self.name = name
        self.type = type
        self.position = position

with app.app_context():
    db.create_all()

@app.route('/add_infrastructure', methods=['POST'])
def add_infrastructure():
    name = request.form['name']
    type = request.form['type']
    position = request.form['position']
    infrastructure = Infrastructure(name, type, position)
    db.session.add(infrastructure)
    db.session.commit()
    return {"message": "Infrastructure added successfully"}

@app.route('/get_infrastructure/<int:id>')
def get_infrastructure(id):
    infrastructure = Infrastructure.query.get(id)
    if infrastructure:
        return jsonify({
            'id': infrastructure.id,
            'name': infrastructure.name,
            'type': infrastructure.type,
            'position': infrastructure.position
        })
    else:
        return {'error': 'Infrastructure not found'}, 404

@app.route('/delete_infrastructure/<int:id>', methods=['DELETE'])
def delete_infrastructure(id):
    infrastructure = Infrastructure.query.get(id)
    if infrastructure:
        db.session.delete(infrastructure)
        db.session.commit()
        return {'message': 'Infrastructure deleted successfully'}
    else:
        return {'error': 'Infrastructure not found'}, 404

@app.route('/get_all_infrastructure', methods=['GET'])
def get_all_infrastructure():
    infrastructures = Infrastructure.query.all()
    result = []
    for infrastructure in infrastructures:
        result.append({
            'id': infrastructure.id,
            'name': infrastructure.name,
            'type': infrastructure.type,
            'position': infrastructure.position
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

    # import requests as r
    # res = r.post(url = "http://127.0.0.1:5000/add_infrastructure", data = {'name': 'Brige', "type": "Makarovsky", "position": "Makarov St."})
    # res = r.post(url="http://127.0.0.1:5000/add_infrastructure", data={'name': 'Tower', "type": "White Tower", "position": "Uralmash"})
    # res = r.get(url = "http://127.0.0.1:5000/get_infrastructure/1")
    # res = r.get(url = "http://127.0.0.1:5000/get_all_infrastructure")
    # res = r.delete(url = "http://127.0.0.1:5000/delete_infrastructure/1")


