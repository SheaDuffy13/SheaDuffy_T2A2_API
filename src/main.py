from flask import Flask
from init import db, ma, bcrypt, jwt
from models.customer import Customer, CustomerSchema
from models.book import Book, BookSchema
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

app.config ['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)




# Define a custom CLI (terminal) command. Run with "flask create" in terminal.
@app.cli.command('create')
def create_all():
    db.create_all()
    print("Tables created")

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")

@app.cli.command('seed')
def seed_db():
    customers = [
        Customer(
            name = 'Admin Joe',
            email='admin@example.com',
            # password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            password = 'eggs',
            address = '',
            phone = '',
            is_admin=True
        ),
        Customer(
            name='John Smith',
            email='user@example.com',
            # password=bcrypt.generate_password_hash('bacon').decode('utf-8'),
            password = 'eggs',
            address = '123 road St, Suburb, QLD',
            phone = '100 200 300 1',
        )
    ]

    books = [
        Book(
            title = 'Lord of the Rings: Fellowship of the Ring',
            author = 'J. R. R. Tolkien',
            description = 'They\'re taking the hobbits to Isengard',
            category = 'fantasy'
        ),
        Book(
            title = 'Lord of the Rings: The Two Towers',
            author = 'J. R. R. Tolkien',
            description = 'They\'re taking the hobbits to Isengard',
            category = 'fantasy'
        ),
        Book(
            title = 'Lord of the Rings: Return of the King',
            author = 'J. R. R. Tolkien',
            description = 'They\'re taking the hobbits to Isengard',
            category = 'fantasy'
        ),
        Book(
            title = 'Sense and Sensibility',
            author = 'Jane Austin',
            description = 'ye olde jaunt',
            category = 'romance'
        ),
        Book(
            title = 'Twilight',
            author = 'Stephenie Meyer',
            description = 'Hold on tight spider monkey',
            category = 'romance'
        ),
        Book(
            title = 'Misery',
            author = 'Stephen King',
            description = 'crazy lady break ankles',
            category = 'horror'
        ),
        Book(
            title = 'The Call of Cthulhu',
            author = 'H. P. Lovecraft',
            description = 'calamari boi',
            category = 'horror'
        )
    ]
    # Add the object as a new row to the table
    db.session.add_all(books)
    db.session.add_all(customers)
    # commit the changes
    db.session.commit()
    print("Table seeded")