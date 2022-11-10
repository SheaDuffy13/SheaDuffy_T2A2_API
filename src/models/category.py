from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = db.relationship('Book', back_populates='category')

    # orders = db.relationship('Order', back_populates='book', cascade='all, delete')

class CategorySchema(ma.Schema):
    books = fields.List(fields.Nested('BookSchema', exclude=['category']))

    class Meta:
        ordered = True
        fields = ('id', 'name', 'books')
