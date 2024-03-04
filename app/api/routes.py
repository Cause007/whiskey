from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whiskey, whiskey_schema, whiskeys_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'key': 'value'}

# create entry
@api.route('/whiskeys',methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    brand = request.json['brand']
    name = request.json['name']
    region = request.json['region']
    type = request.json['type']
    abv = request.json['abv']
    price = request.json['price']
    user_token = current_user_token.token
    
    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey(brand, name, region, type, abv, price, user_token=user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

# retrieve ALL entries
@api.route('/whiskeys', methods = ['GET'])
@token_required
def get_whiskeys(current_user_token):
    a_user = current_user_token.token
    whiskeys = Whiskey.query.filter_by(user_token = a_user).all()
    response = whiskeys_schema.dump(whiskeys)
    return jsonify(response)

# retrieve ONE entry
@api.route('/whiskeys/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    a_user = current_user_token.token
    whiskey = Whiskey.query.get(id)
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

# update entry
@api.route('/whiskey/<id>', methods = ['POST','PUT'])
@token_required
def update_whiskey(current_user_token,id):
    whiskey = Whiskey.query.get(id)
    whiskey.brand = request.json['brand']
    whiskey.name = request.json['name']
    whiskey.region = request.json['region']
    whiskey.type = request.json['type']
    whiskey.abv = request.json['abv']
    whiskey.price = request.json['price']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

# delete entry 
@api.route('whiskey/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

