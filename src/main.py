from flask import Flask
from init import db, ma

app = Flask(__name__)

@app.route('/')
def home():
    return 'hello world'


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
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            address = '',
            phone = '',
            is_admin=True
        ),
        Customer(
            name='John Smith',
            email='user@example.com',
            password=bcrypt.generate_password_hash('bacon').decode('utf-8')
            address = '123 road St, Suburb, QLD',
            phone = '100 200 300 1',
        )
    ]

    books = [
        Book(
            title = 'Lord of the Rings: Fellowship of the Ring',
            author = 'J. R. R. Tolkien',
            description = 'An epic fantasy',
            category = 'fantasy'
        ),
        Book(
            title = 'Lord of the Rings: The Two Towers',
            author = 'J. R. R. Tolkien',
            description = 'An epic fantasy',
            category = 'fantasy'
        ),
        Book(
            title = 'Lord of the Rings: Return of the King',
            author = 'J. R. R. Tolkien',
            description = 'An epic fantasy',
            category = 'fantasy'
        ),
        Book(
            title = 'Sense and Sensibility',
            author = 'Jane Austin',
            description = 'idk',
            category = 'romance'
        )
        Book(
            title = 'Twilight',
            author = 'Stephenie Meyer',
            description = 'Hold on tight spider monkey',
            category = 'romance'
        )
        Book(
            title = 'Misery',
            author = 'Stephen King',
            description = 'crazy lady break ankles',
            category = 'horror'
        )
        Book(
            title = 'The Green Mile',
            author = 'Stephen King',
            description = 'sad boi',
            category = 'horror'
        )
    ]
    # Add the object as a new row to the table
    db.session.add_all(books)
    db.session.add_all(customers)
    # commit the changes
    db.session.commit()
    print("Table seeded")