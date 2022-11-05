from flask import Flask
from init import db, ma, bcrypt, jwt
from models.user import User, UserSchema
from models.book import Book, BookSchema
from models.category import Category, CategorySchema
from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
from controllers.cli_controller import db_commands
from controllers.books_controller import books_bp
from controllers.categories_controller import categories_bp
from controllers.auth_controller import auth_bp
import os

def create_app():
    app = Flask(__name__)

    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(books_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(auth_bp)

    return app
