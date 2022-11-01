from init import db, ma
from marshmallow import fields

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category = db.Column(db.String, nullable=False)

    # orders = db.relationship('Order', back_populates='book', cascade='all, delete')

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'description', 'category')

