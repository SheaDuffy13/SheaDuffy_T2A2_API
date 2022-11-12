import os
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
# from models.user import User, UserSchema
from models.wishlist import Wishlist, WishlistSchema
from models.wishlist_item import Wishlist_Item
from models.book import Book, BookSchema
# from models.user import User

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

# Get current user wishlist
@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()
    stmt = db.select(Wishlist).where(Wishlist.user_id==user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
       return WishlistSchema(exclude=['user']).dump(wishlist)
    else:
        return {'error': 'Wishlist empty'}, 404


# Creates an wishlist and adds the first item to it
@wishlist_bp.route('/', methods=['POST'])
@jwt_required()
def create_wishlist():
    # Creates the wishlist and assigns it to the user
    wishlist = Wishlist(
        user_id = get_jwt_identity()
    )
    db.session.add(wishlist)
    db.session.commit()
    # Creates the first wishlist item and assigns it to the wishlist
    wishlist_items = WishlistItem(
        wishlist_id = wishlist.id
    )
    db.session.add(wishlist_items)
    db.session.commit()
    return WishlistSchema(exclude=['user']).dump(wishlist), 201



# Adds a wishlist item to an existing wishlist
@wishlist_bp.route('/add/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def add_to_order(id):
    # Determines current user
    user_id = get_jwt_identity()
    # Selects wishlist from database based on user_id
    stmt = db.select(Wishlist).where(Wishlist.user_id==user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
        # book_stmt = db.select(Book).where(Book.id==id)
        book_stmt = db.select(Book).where(Book.id==id)
        book = db.session.scalar(book_stmt)

        # wish_item_stmt = db.select(Wishlist_Item).where(Wishlist_Item==wishlist, Wishlist_Item.book==book)
        wish_item_stmt = db.select(Wishlist_Item).where(Wishlist_Item.wishlist==wishlist, Wishlist_Item.book==book)
        wish_item = db.session.scalar(wish_item_stmt)

        if not wish_item:
            wishlist_item = Wishlist_Item(
                wishlist_id = wishlist.id,
                # book_id = request.json['book_id']
                book_id = id
                )
        else:
            return {'error': f'Book with id {id} already in wishlist'}, 404
        db.session.add(wishlist_item)
        db.session.commit()
        return WishlistSchema(exclude=['user']).dump(wishlist), 201
    else:
        return {'error': f'Wishlist not found for user with id {user_id}'}, 404


# Deletes a wishlist item
@wishlist_bp.route('/delete/<int:item_id>/', methods=['DELETE'])
@jwt_required()
def delete_wishlist_item(item_id):
    # Determines current user
    user_id = get_jwt_identity()
    # Selects wishlist from database based on user_id
    stmt = db.select(Wishlist).where(Wishlist.user_id==user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
        stmt = db.select(Wishlist_Item).filter_by(id=item_id)
        wishlist_item = db.session.scalar(stmt)
        if wishlist_item:
            db.session.delete(wishlist_item)
            db.session.commit()
            return {'message': f'Wishlist item {item_id} deleted from wishlist'}
        else:
            return {'error': f'Wishlist item {item_id} not found in wishlist'}, 404



