from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
from marshmallow.validate import Regexp

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    # address = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    wishlist = db.relationship('Wishlist', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):

    password = fields.String(required=True, validate=Regexp('^(?=\S{6,20}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
    error='Password must be more than 6 characters and contain an uppercase letter and a number')
    )
    email = fields.String(required=True, validate=Length(min=1, max=20, error='Email cannot be empty'))
    wishlist = fields.List(fields.Nested('WishlistSchema', exclude=['user']))

    class Meta:
        ordered = True
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'wishlist')

