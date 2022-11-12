from init import db, ma
from marshmallow import fields
from marshmallow import fields, validate
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # orders = db.relationship('Order', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):

    password = fields.String(required=True, validate=Regexp('^(?=\S{6,20}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
    error='Password must be more than 6 characters and contain an uppercase letter and a number')
    )

    class Meta:
        ordered = True
        fields = ('id', 'name', 'email', 'password', 'address', 'is_admin')

