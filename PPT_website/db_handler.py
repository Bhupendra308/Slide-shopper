# db_handler.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
db = SQLAlchemy()
from datetime import datetime
import os
# ---------------------------
# MODELS
# ---------------------------

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    thumbnail = db.Column(db.String(200))
    file_path = db.Column(db.String(300))
    file_size = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(200))



class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    ppt_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")  # pending/delivered
    download_link = db.Column(db.String(300))  # For large files
    email_sent = db.Column(db.Boolean, default=False)

    product = db.relationship("Product", backref="orders")




class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)


# ---------------------------
# DB INIT
# ---------------------------

def init_db(app):
    """Initialize the SQLAlchemy database with Flask app."""
    # Example MySQL connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bhupendra.2004@localhost/ppt_store'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


# ---------------------------
# USER FUNCTIONS
# ---------------------------

def create_user(username, email, password, is_admin=False):
    hashed_pw = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_pw, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    return user




def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


# ---------------------------
# PRODUCT FUNCTIONS
# ---------------------------


# db_handler.py
def add_product(title, description, filename, price, filepath, file_size):
    new_product = Product(
        title=title,
        description=description,
        price=price,
        filename=filename,
        file_path=filepath,
        file_size=file_size,
        created_at=datetime.utcnow(),
        thumbnail=None
    )
    db.session.add(new_product)
    db.session.commit()



def get_all_products():
    return Product.query.all()


def get_products_by_ids(ids_list):
    return Product.query.filter(Product.id.in_(ids_list)).all()


# ---------------------------
# ORDER FUNCTIONS
# ---------------------------

def store_order(user_id, product_id, download_link=None):
    order = Order(user_id=user_id, product_id=product_id, download_link=download_link)
    db.session.add(order)
    db.session.commit()
    return order



# ---------------------------
# BOOKING FUNCTIONS
# ---------------------------

def store_booking(name, email, ppt_id):
    booking = Booking(name=name, email=email, ppt_id=ppt_id)
    db.session.add(booking)
    db.session.commit()


# ---------------------------
# CONTACT FUNCTIONS
# ---------------------------

def store_contact(name, email, message):
    contact = Contact(name=name, email=email, message=message)
    db.session.add(contact)
    db.session.commit()
