from init import db, ma
from marshmallow import fields, validate, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

class Wishlist_Item(db.Model):
    __tablename__ = 'wishlist_items'

    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    wishlist = db.relationship('Wishlist', back_populates='wishlist_items')
    book = db.relationship('Book', back_populates='wishlist_items')


class Wishlist_ItemSchema(ma.Schema):
    book = fields.Nested('BookSchema', exclude=['author_id'])
    wishlist = fields.Nested('WishlistSchema') # , exclude=['wishlist_id']
    class Meta:
        fields = ('id', 'wishlist', 'book') #, 'wishlist_id', 'book_id'
        ordered = True