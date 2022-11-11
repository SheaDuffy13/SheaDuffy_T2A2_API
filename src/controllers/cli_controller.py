from unicodedata import category
from flask import Blueprint
from init import db, bcrypt
from models.book import Book
from models.user import User
from models.author import Author
# from models.category import Category

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
    users = [
        User(
            name = 'Admin Joe',
            email='admin@example.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            address = '',
            phone = '155620024',
            is_admin=True
        ),
        User(
            name='John Smith',
            email='user@example.com',
            password=bcrypt.generate_password_hash('bacon').decode('utf-8'),
            # password = 'eggs',
            address = '123 road St, Suburb, QLD',
            phone = '1002003001',
        )
    ]

    # Add the object as a new row to the table
    db.session.add_all(users)
    db.session.commit()

    # categories = [
    #     Category(
    #         name = 'horror'
    #     ),
    #     Category(
    #         name='romance'
    #     ),
    #     Category(
    #         name='fantasy'
    #     ),
    # ]

    # # Add the object as a new row to the table
    # db.session.add_all(categories)
    # db.session.commit()

    authors = [
        Author(
            name = 'Jay Kristoff',
            bio = 'A bio on this author'
        ),
        Author(
            name='Jane Austin',
            bio = 'A bio on this author'
        ),
        Author(
            name='Stephenie Meyer',
            bio = 'A bio on this author'
        ),
        Author(
            name='Stephen King',
            bio = 'A bio on this author'
        ),
        Author(
            name='H. P. Lovecraft',
            bio = 'A bio on this author'
        ),
    ]

    # Add the object as a new row to the table
    db.session.add_all(authors)
    db.session.commit()

    books = [
        Book(
            title = 'Nevernight',
            # author = 'Jay Kristoff',
            author = authors[0],
            description = 'A booky book',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'fantasy'
            # category_id = categories[2].id
            # category = categories[2]
        ),
        Book(
            title = 'Empire Of The Vampire',
            # author = 'Jay Kristoff',
            author = authors[0],
            description = 'A booky book book',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'fantasy'
            # category_id = categories[2].id
            # category = categories[2]
        ),
        Book(
            title = 'Sense And Sensibility',
            # author = 'Jane Austin',
            author = authors[1],
            description = 'Ye olde jaunt',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'romance'
            # category_id = categories[1].id
            # category = categories[1]
        ),
        Book(
            title = 'Twilight',
            # author = 'Stephenie Meyer',
            author = authors[2],
            description = 'Hold on tight spider monkey',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'romance'
            # category_id = categories[1].id
            # category = categories[1]
        ),
        Book(
            title = 'Misery',
            # author = 'Stephen King',
            author = authors[3],
            description = 'crazy lady break ankles',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'horror'
            # category_id = categories[0].id
            # category = categories[0]
        ),
        Book(
            title = 'The Call Of Cthulhu',
            # author = 'H. P. Lovecraft',
            author = authors[4],
            description = 'calamari boi',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'horror'
            # category_id = categories[0].id
            # category = categories[0]
        )
    ]
    
    db.session.add_all(books)
    db.session.commit()


    print("Table seeded")