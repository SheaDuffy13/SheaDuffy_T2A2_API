from unicodedata import category
from flask import Blueprint
from init import db, bcrypt
from models.book import Book
from models.customer import Customer
from models.category import Category

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    customers = [
        Customer(
            name = 'Admin Joe',
            email='admin@example.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            # password = 'eggs',
            address = '',
            phone = '',
            is_admin=True
        ),
        Customer(
            name='John Smith',
            email='user@example.com',
            password=bcrypt.generate_password_hash('bacon').decode('utf-8'),
            # password = 'eggs',
            address = '123 road St, Suburb, QLD',
            phone = '100 200 300 1',
        )
    ]

    # Add the object as a new row to the table
    db.session.add_all(customers)
    db.session.commit()

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
    
    db.session.add_all(books)
    db.session.commit()

    categories = [
        Category(
            name = 'horror'
        ),
        Category(
            name='romance'
        ),
        Category(
            name='crime'
        ),
        Category(
            name='sci-fi'
        ),
        Category(
            name='non-fiction'
        ),
        Category(
            name='fantasy'
        ),
    ]

    # Add the object as a new row to the table
    db.session.add_all(categories)
    db.session.commit()


    print("Table seeded")