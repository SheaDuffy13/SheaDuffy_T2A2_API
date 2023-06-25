from marshmallow import fields
from init import db, ma


class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    # Set colums of table to be created in database
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Set relationships of table to other tables
    wishlist_items = db.relationship('Wishlist_Item', back_populates='wishlist', cascade='all, delete')
    user = db.relationship('User', back_populates='wishlist')


class WishlistSchema(ma.Schema):
    wishlist_items = fields.List(fields.Nested('Wishlist_ItemSchema', exclude=['wishlist']))

    class Meta:
        ordered = True
        fields = ('id', 'user_id', 'user', 'wishlist_items')