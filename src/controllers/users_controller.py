from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User, UserSchema
from controllers.auth_controller import authorize
from init import db, bcrypt


users_bp = Blueprint('users', __name__, url_prefix='/users')


# ADMIN ROUTES ----------------------------------------------------------------------

# Route for admins to see all users
@users_bp.route('/')
@jwt_required()
def display_users():
    authorize()
    # Select all users
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    # Return UserSchema of users selected with stmt
    return UserSchema(many=True, exclude=['password', 'wishlist']).dump(users)


# Route for admins to see all admin users
@users_bp.route('/admins/')
@jwt_required()
def diaply_all_admins():
    authorize()
    # Select users with is_admin set to True
    stmt = db.select(User).filter_by(is_admin=True)
    admins = db.session.scalars(stmt)
    # Return UserSchema of users selected with stmt
    return UserSchema(many=True, exclude=['password']).dump(admins)


# Route for admins to see a specific user's details
@users_bp.route('/<int:id>/')
@jwt_required()
def display_one_user(id):
    authorize()
    # Select user with id in url
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Return UserSchema of users selected with stmt
        return UserSchema(exclude=['password', 'wishlist']).dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404

# Route for admins to update any user, exluding password field
@users_bp.route('/update_user/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_selected_user(id):
    authorize()
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Load UserSchema data in order to access validation rules
        data = UserSchema().load(request.json)
        # Updates user detail in the database based on json request or lack of
        user.name = request.json.get('name') or user.name
        user.email = request.json.get('email') or user.email
        # Solves issue with updating boolean values to False
        if request.json.get('is_admin') is not None:
            user.is_admin = request.json.get('is_admin')
        else:
            user.is_admin = user.is_admin
        # Commit session to databse
        db.session.commit()
        # Dsiplays updated user info to client
        return UserSchema(exclude=['password']).dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404


# Route for admins to delete any user
@users_bp.route('/delete_user/<int:id>/', methods=['DELETE'])
@jwt_required()
def admin_delete_user(id):
    authorize()
    # Select user with id in url
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Delete user and commit
        db.session.delete(user)
        db.session.commit()
        # Respond to client
        return {'message': f"User '{user.email}' deleted successfully"}
    else:
        return {'error': f'User not found with id {id}'}, 404


# GENERIC USER ROUTES ----------------------------------------------------------------------

# Route for users to update their own details
@users_bp.route('/update_account/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_account():
    # Determines current user
    user_id = get_jwt_identity()
    # Selects user from database based on user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # Load UserSchema data to access validation rules
        data = UserSchema().load(request.json)
        # Update user details in database based on json request or leave as is
        user.name = request.json.get('name') or user.name
        user.email = request.json.get('email') or user.email
        # So excluding password key doesn't throw and error
        if request.json.get('password'):
            # Hashes password and stores in databse
            user.password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf8')
        # # Commit session to databse
        db.session.commit()
        # Dsiplays updated user info to client
        return UserSchema(exclude=['wishlist', 'password']).dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404


# Route for users to delete their own account
@users_bp.route('/delete_account/', methods=['DELETE'])
@jwt_required()
def delete_account():
    # Determines current user
    user_id = get_jwt_identity()
    # Selects user from database based on user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # Deletes user from database
        db.session.delete(user)
        # Commits the change
        db.session.commit()
        # Respond to client
        return {'message': f"User '{user.email}' deleted successfully"}
    else:
        return {'error': f'User not found with id {id}'}, 404