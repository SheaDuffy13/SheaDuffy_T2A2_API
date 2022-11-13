from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.wishlist import Wishlist, WishlistSchema
from models.wishlist_item import Wishlist_Item
from models.book import Book
from init import db


wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

# Route to get current user's wishlist
@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_wishlist():
    # Determines current user
    user_id = get_jwt_identity()
    # Selects wishlist where the user id is the current user
    stmt = db.select(Wishlist).where(Wishlist.user_id==user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
        # Display current user's wishlist
        return WishlistSchema(exclude=['user']).dump(wishlist)
    else:
        return {'error': 'Wishlist empty'}, 404


# Route to add item to current user wishlist, checks if book already present
@wishlist_bp.route('/add/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def add_to_order(id):
    # Determines current user
    user_id = get_jwt_identity()
    # Selects wishlist from database based on current user
    stmt = db.select(Wishlist).where(Wishlist.user_id==user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
        # Selects book with id in url
        book_stmt = db.select(Book).where(Book.id==id)
        book = db.session.scalar(book_stmt)
        # Looks for wishlist_item where the wishlist id and book id match the previous 2 stmts
        wish_item_stmt = db.select(Wishlist_Item).where(Wishlist_Item.wishlist==wishlist, Wishlist_Item.book==book)
        wish_item = db.session.scalar(wish_item_stmt)
        # If wish_item is False, then the book is not already in the wishlist
        if not wish_item:
            # A new instance of wish_item is created
            wishlist_item = Wishlist_Item(
                # wishlist id is set to that of the previous wishlist stmt
                wishlist_id = wishlist.id,
                # Book id set to the one from the url
                book_id = id
                )
        else:
            return {'error': f'Book with id {id} already in wishlist'}, 404
        # Commit changes
        db.session.add(wishlist_item)
        db.session.commit()
        # Respond to client
        return WishlistSchema(exclude=['user']).dump(wishlist), 201
    else:
        return {'error': f'Wishlist not found for user with id {user_id}'}, 404


# Deletes a wishlist item
@wishlist_bp.route('/delete/<int:item_id>/', methods=['DELETE'])
@jwt_required()
def delete_wishlist_item(item_id):
    # Determines current user
    user_id = get_jwt_identity()
    # Selects wishlist from database based on current user
    stmt = db.select(Wishlist).where(Wishlist.user_id==user_id)
    wishlist = db.session.scalar(stmt)
    if wishlist:
        # Selects wishlist_item with id in url
        stmt = db.select(Wishlist_Item).filter_by(id=item_id)
        wishlist_item = db.session.scalar(stmt)
        if wishlist_item:
            # Delete wishlist item
            db.session.delete(wishlist_item)
            db.session.commit()
            # Respond to client
            return {'message': f'Wishlist item {item_id} deleted from wishlist'}
        else:
            return {'error': f'Wishlist item {item_id} not found in wishlist'}, 404



