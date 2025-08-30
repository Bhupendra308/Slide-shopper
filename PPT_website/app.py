from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from db_handler import (
    db, init_db,
    get_all_products, get_products_by_ids,
    create_user, get_user_by_email,
    store_order, store_contact, store_booking, add_product
)
from db_handler import db, User, Product, Booking, Order, Contact


from sqlalchemy import or_
from db_handler import db, User
import os
app = Flask(__name__)
app.secret_key = "supersecretkey"  # ⚠️ Change for production

# Init DB
init_db(app)

# ---------------------------
# ROUTES
# ---------------------------


from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash("Please login first.", "warning")
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash("Admin access required.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


UPLOAD_FOLDER = 'static/ppts'
ALLOWED_EXTENSIONS = {'ppt', 'pptx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price', 0.0)   # 🟢 get price from form
        file = request.files.get('file')

        if not title or not file:
            flash("Title and file are required.", "danger")
            return redirect(url_for('admin_dashboard'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # ✅ Ensure upload folder exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Save file
            file.save(filepath)

            # File size
            file_size = os.path.getsize(filepath)

            # ✅ Add to DB (now using price + file_size + filepath)
            add_product(
                title=title,
                description=description,
                filename=filename,
                price=float(price),
                filepath=filepath,   # ✅ matches function signature
                file_size=file_size
            )


            flash("PPT uploaded successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid file type.", "danger")
            return redirect(url_for('admin_dashboard'))

    # GET request: show all uploaded PPTs
    products = get_all_products()
    return render_template('admin_dashboard.html', products=products)



@app.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)


# --- USER AUTH ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if get_user_by_email(email):
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        # ⚠️ Do NOT hash here, create_user() already hashes
        create_user(name, email, password)

        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

        if user and check_password_hash(user.password, password):
            # store session info
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin  # keep track of admin role

            flash("Login successful!", "success")

            # redirect based on role
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash("Invalid username/email or password!", "danger")

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login to view your dashboard.", "warning")
        return redirect(url_for("login"))

    if session.get("is_admin"):  
        flash("Admins should use the admin panel.", "info")
        return redirect(url_for("admin_dashboard"))

    user = User.query.get(session["user_id"])

    # Fetch user's orders (history)
    orders = Order.query.filter_by(user_id=user.id).all()

    # Optional: Fetch items in cart from session
    cart_items = []
    if "cart" in session and session["cart"]:
        cart_items = get_products_by_ids(session["cart"])

    return render_template("dashboard.html", user=user, orders=orders, cart_items=cart_items)


# --- CART ---
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    if product_id not in session['cart']:
        session['cart'].append(product_id)
        flash("Product added to cart!", "success")
    else:
        flash("Product already in cart.", "info")

    return redirect(url_for('shop'))



@app.route('/cart')
def cart():
    if 'cart' not in session or len(session['cart']) == 0:
        flash("Your cart is empty.", "info")
        return render_template('cart.html', cart_items=[])

    product_ids = session['cart']
    cart_items = get_products_by_ids(product_ids)
    return render_template('cart.html', cart_items=cart_items)


# --- PLACE ORDER ---
@app.route('/place_order')
def place_order():
    if 'user_id' not in session:
        flash("Please login to place order.", "warning")
        return redirect(url_for('login'))

    if 'cart' not in session or len(session['cart']) == 0:
        flash("Cart is empty!", "info")
        return redirect(url_for('cart'))

    for product_id in session['cart']:
        store_order(session['user_id'], product_id)

    session['cart'] = []  # empty cart after placing order
    flash("Order placed successfully!", "success")
    return redirect(url_for('dashboard'))



# --- CONTACT ---
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        store_contact(name, email, message)
        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


# --- BOOKINGS ---
@app.route('/buy/<int:ppt_id>', methods=['POST'])
def buy_ppt(ppt_id):
    if "user_id" not in session:
        flash("Please login first to buy.", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Check if ppt exists
    ppt = Product.query.get(ppt_id)
    if not ppt:
        flash("PPT not found.", "danger")
        return redirect(url_for("shop"))

    # Determine if download link is needed
    if ppt.file_size > 5 * 1024 * 1024:  # e.g., >5MB
        download_link = url_for('static', filename=f'ppts/{ppt.filename}', _external=True)
    else:
        download_link = None

    # Store order in DB with new fields
    order = store_order(user_id=user_id, product_id=ppt_id, download_link=download_link)

    flash(f"You bought '{ppt.title}' successfully!", "success")
    return redirect(url_for("dashboard"))



# --- SHOP PAGE ---
@app.route('/shop')
def shop():
    ppts = get_all_products()
    return render_template('shop.html', ppts=ppts)



# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ensure all tables exist
    app.run(debug=True)
