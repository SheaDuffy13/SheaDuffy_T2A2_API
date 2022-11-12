from marshmallow import fields, validate, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError
from init import db, ma



class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    wishlist_items = db.relationship('Wishlist_Item', back_populates='wishlist', cascade='all, delete')
    user = db.relationship('User', back_populates='wishlist')


class WishlistSchema(ma.Schema):
    wishlist_items = fields.List(fields.Nested('Wishlist_ItemSchema', exclude=['wishlist']))
    # books =          fields.List(fields.Nested('BookSchema', exclude=['author']))

    class Meta:
        ordered = True
        fields = ('id', 'user_id', 'user', 'wishlist_items') #'user', 