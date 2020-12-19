import os

from flask import Flask, url_for, flash, request, redirect, \
                  send_from_directory, render_template, jsonify,\
                  session

import stripe
from models import db, User, Item

from flask_session import Session, sessions
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from werkzeug.security import check_password_hash

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
basedir = os.path.abspath(os.path.dirname(__file__))
db_url = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite3')

UPLOAD_FOLDER = basedir + '/static/assets/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(16)

sess = Session()
db.init_app(app)
sess.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Item=Item)


@app.route('/')
def homepage():
    return render_template('main/homepage.html')


@app.route('/food')
def food():
    items = Item.query.all()
    return render_template('main/food.html', items=items)

@app.route('/product')
def product():
    items = Item.query.all()
    return render_template('main/product.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        contact_no = request.form['contact_no']
        password = request.form['password']
        check_email = User.query.filter_by(email=email).first()
        if check_email:
            flash("Email has been used already!")
            return redirect(request.url)
        new_user = User(username=username, email=email,
                        contact_number=contact_no, password=password)
        new_user.save()
        flash("You have registered succesfully")
        return redirect(url_for('login'))
    return render_template('main/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        check_user = User.query.filter_by(email=email).first()
        if not check_user:
            flash('Invalid credentials.', category='error')
            return redirect(url_for('login'))
        if check_password_hash(check_user.password, password):
            print(check_user)
            session['logged_in'] = True
            return redirect(url_for('food'))
    return render_template('main/login.html')


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/learnmore')
def learnmore():
    return render_template('main/learnmore.html')


@app.route('/about__us')
def about__us():   
    return render_template('main/about__us.html')

@app.route('/order/<int:item_id>')
def order(item_id):
    item = Item.query.get(item_id)
    return render_template('main/order.html', item=item)


# ======================= FILE UPLOAD ============================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
# ========================= STRIPE ===============================


@app.route('/payment/success/')
def success():
    return render_template('main/success.html')


@app.route('/payment/cancel/')
def cancel():
    return render_template('main/cancel.html')


@app.route('/pay')
def stripe_pay():
    return render_template('main/stripe.html')


@app.route('/create-checkout-session/<int:item_id>/<int:quantity>/', methods=['GET', 'POST'])
def create_checkout_session(item_id, quantity):
  item = Item.query.get(item_id)
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': item.name,
        },
        'unit_amount': int(item.price) * 100,
      },
      'quantity': int(quantity),
    }],
    mode='payment',
    success_url='http://127.0.0.1:5000/payment/success/',
    cancel_url='http://127.0.0.1:5000/payment/cancel/',
  )

  return jsonify(id=session.id)
# ====================================================================

if __name__ == '__main__':
    app.run(debug=True)
