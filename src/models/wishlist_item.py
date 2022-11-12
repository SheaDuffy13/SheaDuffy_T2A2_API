from init import db, ma
from marshmallow import fields

class Wishlist_Item(db.Model):
    __tablename__ = 'wishlist_items'
    # Set colums of table to be created in database
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    # Set relationships of table to other tables
    wishlist = db.relationship('Wishlist', back_populates='wishlist_items')
    book = db.relationship('Book', back_populates='wishlist_items')


class Wishlist_ItemSchema(ma.Schema):
    # Displays nested book data of wishlist_item
    book = fields.Nested('BookSchema', exclude=['author_id'])
    class Meta:
        fields = ('id', 'wishlist', 'book')
        ordered = True


    # wishlist = fields.Nested('WishlistSchema')      removed
