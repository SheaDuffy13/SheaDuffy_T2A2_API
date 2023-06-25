from datetime import timedelta
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity
from models.wishlist import Wishlist
from models.user import User, UserSchema
from init import db, bcrypt


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Route to register new users
@auth_bp.route('/register/', methods=['POST'])
def register_user():
    try:
        # Load UserSchema in order to access validation rules
        data = UserSchema().load(request.json)
        # Create a new User model instance
        user = User(
            # Fill user fields with json requests
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            name = request.json['name'],
            is_admin = request.json['is_admin']
        )
        # Add and commit user to database
        db.session.add(user)
        db.session.commit()
        
        # Creates a wishlist and assigns it to the user
        wishlist = Wishlist(
            user_id = user.id
        )
        # Add and commit wishlist to database
        db.session.add(wishlist)
        db.session.commit()

        # Respond to client
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


# Route to log in user
@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    # Assign stmt selection to variable
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # Create login token for user
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # Respond to client
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401


# Checks if user is admin
def authorize():
    # Gets current user id
    user_id = get_jwt_identity()
    # Selects user from database based on current user id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)

