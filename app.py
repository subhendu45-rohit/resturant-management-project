from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(hours=1)

# Menu Data
menu_data = {
    "breakfast": [
        {"name": "Puri Upma", "price": 30, "image": "images/puri_upma.jpeg"},
        {"name": "Samosa", "price": 20, "image": "images/samosa.jpeg"},
        {"name": "Dosa", "price": 40, "image": "images/dosa.jpg"},
        {"name": "Idli", "price": 30, "image": "images/idli.jpg"}
    ],
    "maincourse": [
        {"name": "Chicken Biryani", "price": 190, "image": "images/Chicken Biriyani.jpeg"},
        {"name": "Dahi Pakhala", "price": 40, "image": "images/Dahi Pakhala.jpg"},
        {"name": "Veg Biryani", "price": 150, "image": "images/veg biriyani.jpeg"},
        {"name": "Chicken Butter Masala", "price": 170, "image": "images/Chicken Butter Masala.jpeg"},
        {"name": "Paneer Butter Masala", "price": 160, "image": "images/Paneer Butter Masala.jpeg"},
        {"name": "Rice Dal", "price": 70, "image": "images/Rice Dal.jpeg"}
    ],
    "snacks": [
        {"name": "Burger", "price": 80, "image": "images/Burger.jpeg"},
        {"name": "French Fries", "price": 40, "image": "images/French Fries.jpeg"},
        {"name": "Paneer Tikka", "price": 120, "image": "images/paneer tikka.jpeg"},
        {"name": "Pizza", "price": 170, "image": "images/Pizza.jpeg"}
    ],
    "chapatis": [
        {"name": "Roti", "price": 10, "image": "images/Chapati.jpeg"},
        {"name": "Butter Naan", "price": 25, "image": "images/Butter Naan.jpeg"},
        {"name": "Paratha", "price": 20, "image": "images/Paratha.jpeg"}
    ],
    "dessert": [
        {"name": "Gulab Jamun", "price": 50, "image": "images/Gulab Jamun.jpeg"},
        {"name": "Ice Cream", "price": 40, "image": "images/Ice Cream.jpeg"},
        {"name": "Rasgulla", "price": 30, "image": "images/Rasgolla.jpeg"},
        {"name": "Chena Poda", "price": 40, "image": "images/Chena Poda.jpeg"}
    ],
    "drinks": [
        {"name": "Cold Coffee", "price": 99, "image": "images/Cold Coffee.jpeg"},
        {"name": "Mojito", "price": 99, "image": "images/Mojito.jpeg"},
        {"name": "Masala Soda", "price": 50, "image": "images/Masala Soda.jpeg"},
        {"name": "Mango Juice", "price": 50, "image": "images/Mango Juice.jpg"}
    ]
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', categories=list(menu_data.keys()))

@app.route('/menu/<category>')
def category_page(category):
    items = menu_data.get(category, [])
    if not items:
        return redirect(url_for('menu'))
    return render_template('category.html', category=category.title(), items=items)

# app.py (update add_to_cart route)
@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('name')
    item_price = int(request.form.get('price'))
    item_image = request.form.get('image')
    quantity = int(request.form.get('quantity', 1))

    cart = session.get('cart', [])
    found = False

    for item in cart:
        if item['name'] == item_name:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        cart.append({
            'name': item_name,
            'price': item_price,
            'image': item_image,
            'quantity': quantity
        })

    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart = session.get('cart', [])

    for item in cart:
        if 'quantity' not in item:
            item['quantity'] = 1

    session['cart'] = cart
    session.modified = True

    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    item_name = request.form.get('name')
    cart = session.get('cart', [])
    cart = [item for item in cart if item['name'] != item_name]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))



@app.route('/place-order', methods=['POST'])
def place_order():
    session.pop('cart', None)
    return render_template('order_confirmation.html')

# Static Pages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/book-table')
def book_table():
    return render_template('book_table.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login.html')  # No base.html

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('signup.html')  # No base.html
@app.route('/generate-bill', methods=['GET', 'POST'])
def generate_bill():
    cart_items = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    gst = round(subtotal * 0.18, 2)
    delivery_charge = 29
    grand_total = subtotal + gst + delivery_charge
    return render_template('bill.html', cart=cart_items, subtotal=subtotal, gst=gst, delivery_charge=delivery_charge, grand_total=grand_total)


menu_items = [
    {'name': 'Puri Upma'}, {'name': 'Samosa'}, {'name': 'Dosa'}, {'name': 'Idli'},
    {'name': 'Chicken Biriyani'}, {'name': 'Dahi Pakhala'}, {'name': 'Veg Biriyani'},
    {'name': 'Chicken Butter Masala'}, {'name': 'Paneer Butter Masala'}, {'name': 'Rice Dal'},
    {'name': 'Dal Makhni'}, {'name': 'Dalma'}, {'name': 'Paneer Chili'}, {'name': 'Mushroom Chili'},
    {'name': 'Burger'}, {'name': 'French Fries'}, {'name': 'Paneer Tikka'}, {'name': 'Pizza'},
    {'name': 'Veg Manchurian'}, {'name': 'Momos'}, {'name': 'Roti'}, {'name': 'Butter Naan'},
    {'name': 'Paratha'}, {'name': 'Gulab Jamun'}, {'name': 'Ice Cream'}, {'name': 'Rasagolla'},
    {'name': 'Chena Poda'}, {'name': 'Cold Coffee'}, {'name': 'Mojito'}, {'name': 'Masala Soda'},
    {'name': 'Mango Juice'}
]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    available = any(query.lower() in item['name'].lower() for item in menu_items)
    return render_template('search.html', query=query, available=available)




@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/order-online')
def order_online():
    return render_template('order_online.html')

@app.route('/order-now')
def order_now():
    return redirect(url_for('order_online'))

@app.context_processor
def inject_request():
    return dict(request=request)

if __name__ == '__main__':
    app.run(debug=True)
