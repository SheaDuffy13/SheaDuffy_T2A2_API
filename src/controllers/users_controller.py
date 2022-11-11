from flask import Blueprint, request, abort
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize


users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/display_all_users/')
def display_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)


@users_bp.route('/<int:id>/')
def get_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema().dump(user)
    else:
        return {'error': f'Book not found with id {id}'}, 404


@users_bp.route('/register/', methods=['POST'])
def user_register():
    try:
        # Create a new User model instance from the user_info
        user = User(
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            name = request.json.get('name')
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


@users_bp.route('/update_user/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(id):
    authorize()
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        user.name = request.json.get('name') or user.name
        user.email = request.json.get('email') or user.email
        user.password = request.json.get('password') or user.password
        user.address = request.json.get('address') or user.address
        user.phone = request.json.get('phone') or user.phone
        user.is_admin = request.json.get('is_admin') or user.is_admin

        db.session.commit()
        return UserSchema(exclude=['password']).dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404


@users_bp.route('/delete_user/<string:email>/', methods=['DELETE'])
@jwt_required()
def delete_user(email):
    authorize()
    stmt = db.select(User).filter_by(email=email)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f"User '{user.name}' deleted successfully"}
    else:
        return {'error': f'User not found with email {email}'}, 404