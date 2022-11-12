from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.wishlist import Wishlist, WishlistSchema
from models.wishlist_item import Wishlist_Item
from models.book import Book, BookSchema

from marshmallow.exceptions import ValidationError
import re


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')



@auth_bp.route('/register/', methods=['POST'])
def register_user():
    
    try:
        # Create a new User model instance
        user = User(
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            name = request.json['name'],
            address = request.json['address'],
            is_admin = request.json['is_admin']
        )
        # Fixes issue with fields.validate in model.user not working on password. Seems like it's evaluating the hashed password not raw input.
        if not re.match(r'^(?=\S{6,20}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$', request.json.get('password')):
            raise ValidationError("Password must be more than 6 characters and contain an uppercase letter and a number")
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        
        # Creates a wishlist and assigns it to the user
        wishlist = Wishlist(
            user_id = user.id
        )
        db.session.add(wishlist)
        db.session.commit()

        # Respond to client
        return UserSchema().dump(user), 201 #exclude=['password']
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # return UserSchema(exclude=['password']).dump(user)
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401


def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)

