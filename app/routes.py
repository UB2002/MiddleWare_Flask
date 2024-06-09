from flask import jsonify, request
from . import db
from app.models import User
from .utils import compute_sha256, verify_password


def register_routes(app):
    @app.route('/')
    def home():
        return "home page"

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        salt, hashed_password = compute_sha256(password)
        new_user = User(username=username, salt=salt, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=username).first()
        if not user or not verify_password(password, user.salt, user.hashed_password):
            return jsonify({'message': 'Invalid username or password'}), 401

        return jsonify({'message': 'Login successful'}), 200

    @app.route('/get', methods=['GET'])
    def data():
        user_data = User.query.all()
        serialized_users = []
        for user in user_data:
            serialized_user = {
                'id': user.id,
                'username': user.username,
                'password': user.hashed_password
            }
            serialized_users.append(serialized_user)
        return jsonify(serialized_users)
