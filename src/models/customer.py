from init import db, ma
from marshmallow import fields

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    phone = db.Column(db.int)
    is_admin = db.Column(db.Boolean, default=False)

    # orders = db.relationship('Order', back_populates='user', cascade='all, delete')

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'address', 'phone', 'is_admin')
