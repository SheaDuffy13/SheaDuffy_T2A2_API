# T2A2 - API Webserver

## **Endpoints**:

### AUTHORIZATION

### **auth/register/** 

- Methods: POST
- Arguments: None
- Authorization: None
- Description: Register user and assign them a wishlist
- Form Data: email, password, name, is_admin
- Response: UserSchema, exclude=password

### **auth/login/**

- Methods: POST
- Arguments: None
- Authorization: Must have registered account
- Description: Log user into site
- Form Data: email, password
- Response: email, token, is_admin

### USERS

### **/users/**

- Methods: GET
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Return all users
- Form Data: None
- Response: UserSchema, exclude=password


### **/users/admins/**

- Methods: GET
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Return all admin users
- Form Data: None
- Response: UserSchema, exclude=password

### **/users/<int:id>/**

- Methods: GET
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Return user with id
- Form Data: None
- Response: UserSchema, exclude=password

### **/users/update_user/<int:id>/**

- Methods: PUT, PATCH
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Update any user account
- Form Data: name, email, is_admin
- Response: UserSchema, exclude=password

### **/users/delete_user/<int:id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Delete any user
- Form Data: None
- Response: "{user.email} deleted successfully"

### **/users/update_account/**

- Methods: PUT, PATCH
- Arguments: None
- Authorization: Bearer token
- Description: Update current user's account
- Form Data: name, email, password
- Response: UserSchema, exclude=password

### **/users/delete_account/**

- Methods: DELETE
- Arguments: None
- Authorization: Bearer token
- Description: Delete current user's account
- Form Data: None
- Response: "User {user.email} deleted successfully"

### BOOKS

### **/books/**

- Methods: GET
- Arguments: None
- Description: Return all books
- Form Data: None
- Response: BookSchema

### **/books//<int:book_id>/**

- Methods: GET
- Arguments: id
- Description: Return book with id
- Form Data: None
- Response: BookSchema

### **/books/search/**

- Methods: GET
- Arguments: None
- Description: Return books by title or author name
- Form Data: "title" or "author"
- Response: BookSchema or AuthorSchema(with books)

### **/books/add_book/**

- Methods: POST
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Add book to database
- Form Data: title, author_id, description, price, date_published, in_stock, category
- Response: BookSchema, 201

### **/books/update_book/<int:id>/**

- Methods: PUT, PATCH
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Update book
- Form Data: title, author_id, description, price, date_published, in_stock, category
- Response: BookSchema

### **/books/delete_book/<int:id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Delete book
- Form Data: None
- Response: return {'message': f"Book '{book.title}' deleted successfully"}

### AUTHORS

### /**authors**/

- Methods: GET
- Arguments: None
- Description: Return all authors
- Form Data: None
- Response: AuthorSchema excluding books

### **/authors/<int:id>/**

- Methods: GET
- Arguments: id
- Description: Returns AuthorSchema and all books associated
- Form Data: None
- Response: AuthorSchema with nested books

### **/authors/add_author/**

- Methods: POST
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Add author to database
- Form Data: name, bio
- Response: AuthorSchema

### **/authors/update_author/<int:id>/**

- Methods: PUT, PATCH
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Update author
- Form Data: name, bio
- Response: AuthorSchema exclude books

### **/authors/delete_author/<int:id>/**

- Methods: DELETE
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Delete Author
- Form Data: None
- Response: "Author {author.name} deleted successfully"

### WISHLIST

### **/wishlist/**

- Methods: GET
- Arguments: None
- Authorization: Bearer token
- Description: Return user's wishlist
- Form Data: None
- Response: WishlistSchema

### **/wishlist/add/<int:id>**

- Methods: PUT, PATCH
- Arguments: id
- Authorization: Bearer token
- Description: Add book to current user's wishlist
- Form Data: None
- Response: 
  - WishlistSchema else: 'error': f'Book with id {id} already in wishlist', 412

### **/wishlist/delete/<int:item_id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token
- Description: Delete book from current user's wishlist
- Form Data: None
- Response: 
  - 'Wishlist item {item_id} deleted from wishlist else: 
  - 'Wishlist item {item_id} not found in wishlist'

-----------------------------------------------

## ERD

![ERD](./docs/API%20ERD.png)