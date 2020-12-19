from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__: str = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    contact_no = db.Column(db.Integer)
    password = db.Column(db.String)

    def __init__(self, username, email, contact_number, password):
        self.username = username
        self.email = email
        self.contact_no = contact_number
        assert isinstance(password, str)
        self.password = generate_password_hash(password)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise e

class Item(db.Model):
    __tablename__: str = 'items'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    tag = db.Column(db.String(15))
    image_name = db.Column(db.String)

    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price


# class OrderItem(db.Model):
#     __tablename__:str = 'orderitems'
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
#     order = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
#     complete = db.Column(db.Boolean, default=0)
#     quantity = db.Column(db.Integer, nullable=False)
#
#     def get_total_quantity_price(self):
#         total = 0
#         item = Item.query.get(self.item_id)
#         total = item.price * self.quantity
#         return total
#
#     @property
#     def get_category(self):
#         item = Item.query.get(self.item_id)
#         return item.category
#
#
# class Order(db.Model):
#     __tablename__:str = 'orders'
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     orderitems = db.relationship('OrderItem', backref='Order',
#                                lazy='dynamic')
#     supplier_complete = db.Column(db.Boolean, default=0)
#     buyer_confirm = db.Column(db.Boolean, default=0)
#     complete = db.Column(db.Boolean, default=0)
