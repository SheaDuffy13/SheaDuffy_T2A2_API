# @app.route('/cart/<int:product_id>', methods=['POST'])
# def add_to_cart(product_id):

#     product = Product.query.filter(Product.id == product_id)
#     cart_item = CartItem(product=product)
#     db.session.add(cart_item)
#     db.session.commit()