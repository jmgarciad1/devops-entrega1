from flask import Flask, jsonify, request, Blueprint
from blacklists.src.commands.authenticate import Authenticate
from blacklists.src.commands.create_blacklist import CreateBlacklist
from blacklists.src.commands.get_blacklist import GetBlacklist
from blacklists.src.errors.errors import TokenInvalid
blacklists_blueprint = Blueprint('blacklists', __name__)


@blacklists_blueprint.route('/blacklists', methods=['POST'])
def create():
    userId = Authenticate(request.headers).execute()

    if not userId:
        raise TokenInvalid()
    
    ip = request.remote_addr
    item = CreateBlacklist(request.get_json(), ip).execute()

    return jsonify(item), 201


@blacklists_blueprint.route('/blacklists/<email>', methods=['GET'])
def show(email):
    userId = Authenticate(request.headers).execute()

    if not userId:
        raise TokenInvalid()
    
    response = GetBlacklist(email).execute()

    return jsonify(response)

@blacklists_blueprint.route('/', methods=['GET'])
def status():

    return jsonify({'status': 'ok'}), 200
