from flask import Blueprint, request, abort
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/users/')
def get_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)    