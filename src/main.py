from flask import Flask
from init import db, ma, bcrypt, jwt
from models.user import User, UserSchema
from models.book import Book, BookSchema
from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
from controllers.cli_controller import db_commands
from controllers.books_controller import books_bp
from controllers.authors_controller import authors_bp
from controllers.users_controller import users_bp
from controllers.auth_controller import auth_bp
from marshmallow.exceptions import ValidationError

import os

def create_app():
    app = Flask(__name__)

    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400

    @app.errorhandler(ValueError)
    def value_err(err):
        return {"error": str(err)}, 400

    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You are not authorized to perform this action'}, 401

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 400


    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    return app
