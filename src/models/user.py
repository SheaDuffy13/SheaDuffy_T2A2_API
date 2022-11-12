from marshmallow import fields, validates
from marshmallow.validate import Regexp, re
from marshmallow.exceptions import ValidationError
from init import db, ma


class User(db.Model):
    __tablename__ = 'users'
    # Set colums of table to be created in database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Set relationships of table to other tables
    wishlist = db.relationship('Wishlist', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    wishlist = fields.List(fields.Nested('WishlistSchema', exclude=['user', 'user_id']))

    # Validation of fields
    name = fields.String(validate=Regexp(
        '[A-Za-z\.]{2,25}( [A-Za-z\.]{2,25})?',
        error='Name must be more than 2 characters and not contain numbers'
        ))
    password = fields.String(validate=Regexp(
        '^(?=\S{6,20}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
        error='Password must be more than 6 characters and contain an uppercase letter and a number'
        ))

    @validates('email')
    def email_is_not_valid(self, email):
        email_regex_pattern = re.compile("[\w\.]+@+[\w\.]+\.[\w]+")
        if(not email_regex_pattern.match(email)):
            raise ValidationError("Not a valid email address.")

    class Meta:
        ordered = True
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'wishlist')

