from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://127.0.0.1:27017/pythonreactdb'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

@app.route('/users', methods=['POST'])  ## Create user on DB
def createUser():
    id = db.insert({
        'name' : request.json['name'],
        'email' : request.json['email'],
        'password' : request.json['password']
    })
    
    return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])  ## Get all users from DB
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password':doc['password']
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])  ## Get an user from DB
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    print(user)
    return jsonify({
        '_id':str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

@app.route('/user/<id>', methods=['DELETE'])  ## Delete user on DB
def deleteUser(id):
    db.delete_one({'_id':ObjectId(id)})
    return jsonify({'message':'User deleted'})

@app.route('/user/<id>', methods=['PUT'])  ## Update user on DB
def updateUser(id):
    db.update_one({'_id': ObjectId(id)},{'$set':{
        'name':request.json['name'],
        'email':request.json['email'],
        'password':request.json['password']
    }})
    return jsonify({'message':'User updated'})

if __name__ == "__main__":
    app.run(debug=True)