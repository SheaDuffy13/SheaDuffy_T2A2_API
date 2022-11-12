import os
from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.user import User, UserSchema
from models.wishlist import Wishlist, WishlistSchema
from models.wishlist_item import Wishlist_Item, Wishlist_ItemSchema
from models.user import User

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

# Get current user wishlist
@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()
    stmt = db.select(Wishlist).where(Wishlist.user_id==user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
       return WishlistSchema().dump(wishlist)
    else:
        return {'error': 'Wishlist empty'}, 404


# # Creates an wishlist and adds the first item to it
# @wishlist_bp.route('/', methods=['POST'])
# @jwt_required()
# def create_order():
#     # Creates the wishlist and assigns it to the user
#     order = Order(
#         user_id = get_jwt_identity(),
#         date = date.today()
#     )
#     db.session.add(order)
#     db.session.commit()
#     # Creates the first wishlist item and assigns it to the wishlist
#     order_items = OrderItem(
#         order_id = order.id,
#         food_id = request.json['food_id'],
#         quantity = request.json['quantity']
#     )
#     db.session.add(order_items)
#     db.session.commit()

#     return OrderSchema().dump(order), 201



# Adds a wishlist item to an existing wishlist
@wishlist_bp.route('/add/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def add_to_order(id):
    # Determines current user
    user_id = get_jwt_identity()
    # Selects user from database based on user_id
    stmt = db.select(Wishlist).filter_by(user_id=user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
        wishlist_item = Wishlist_Item(
            wishlist_id = wishlist.id,
            book_id = request.json['book_id'],
                    # = request.json.get('title')
        )
        db.session.add(wishlist_item)
        db.session.commit()
        return WishlistSchema().dump(wishlist), 201
    else:
        return {'error': f'Wishlist not found with id {id}'}, 404


# Deletes a wishlist item
@wishlist_bp.route('/<int:item_id>/', methods=['DELETE'])
@jwt_required()
def delete_wishlist_item(item_id):
    # Determines current user
    user_id = get_jwt_identity()
    # Selects user from database based on user_id
    stmt = db.select(Wishlist).filter_by(user_id=user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
        stmt = db.select(Wishlist_Item).filter_by(id=item_id)
        wishlist_item = db.session.scalar(stmt)
        if wishlist_item:
            db.session.delete(wishlist_item)
            db.session.commit()
            return {'message': f'Wishlist item {item_id} deleted from wishlist {id}'}
        else:
            return {'error': f'Wishlist item {item_id} not found in wishlist {id}'}, 404



# Check if the user_id for the order matches the user_id of the user making the request
# def check_owner():
#     user_id = get_jwt_identity()
#     wishlist_id = request.view_args['id']
#     stmt = db.select(Wishlist).filter_by(id=wishlist_id)
#     order = db.session.scalar(stmt)
#     if order.user_id != int(user_id):
#         abort(401)


