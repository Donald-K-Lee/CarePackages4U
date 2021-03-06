	# import pyrebase

# config = {
#   "apiKey": "AIzaSyCw8B4O1W2QWvJxLiKkYU7jV1gdxiJ7fN4",
#   "authDomain": "team-ambition---xdhacks-covid.firebaseapp.com",
#   "databaseURL": "https://team-ambition---xdhacks-covid.firebaseio.com",
#   "projectId": "team-ambition---xdhacks-covid",
#   "storageBucket": "team-ambition---xdhacks-covid.appspot.com",
#   "messagingSenderId": "871510031672",
#   "appId": "1:871510031672:web:19d87bd70ed2dcce6fd5cd",
#   "measurementId": "G-S0G3TL5TXP"
# }

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()

# firebase database above
# flask below

from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

import os

from wtf import *

date_format='%Y/%m/%d %H:%M:%S %Z'

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

# ----- auto update css begin
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
# ----- auto update css end

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

app.config['SECRET_KEY'] = 'idk'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	list = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(30), nullable=False)
	age = db.Column(db.Integer, nullable=False)
	email = db.Column(db.String(100), nullable=False)
	tel = db.Column(db.String(30), nullable=False)
	city = db.Column(db.String(30), nullable=False)
	category = db.Column(db.String(30), nullable=False)
	date = db.Column(db.DateTime, default=datetime.now)
	about = db.Column(db.String(100), nullable=False)

# ----- reset data in case of error
# db.create_all()
# ----- print db
# t = User.query.all()
# print(t)
# ----- manual delete by id
# t = User.query.get(13)
# db.session.delete(t)
# db.session.commit()

# ----- change datetime
# t = User.query.get(7)
# print(t.date.strftime(date_format))
# t.date = t.date.astimezone(pytz.timezone('US/Pacific'))
# print(t.date.strftime(date_format))
# db.session.commit()

# ----- add test
#     return '<h1>Added New User!</h1>'
# test = User(list='random stuff', name='test', age=20, email='test@example.com', number='123456789', city='Vancouver', category='test', about='something about me')
# db.session.add(test)
# db.session.commit()

# ----- add test 2
# @app.route('/<list>/<name>/<age>/<email>/<number>/<city>/<category>/<about>')
# def index(list,name,age,email,number,city,category,about):
#     user = User(list=list,name=name,age=age,email=email,number=number,city=city,category=category,about=about)
#     db.session.add(user)
#     db.session.commit()

# ----- check test
# @app.route('/<name>')
# def get_user(name):
# 	user = User.query.filter_by(name=name).first()

# 	return f'<h1>age: { user.age }</h1><br><h1>email: { user.email }</h1>'

# ----- routes below

@app.route('/')
@app.route('/index.html')
def base_page():
	posts = User.query.all()
	return render_template('index.html', posts=posts[::-1], len=len(posts))

@app.route('/Create.html', methods=['GET', 'POST'])
def create_page():
	cform = CreateForm()
	if request.method == 'POST' and cform.validate_on_submit:
		result = request.form
		results = []
		for key,value in result.items():
			results.append(value)
		print(results)
		post = User(list=results[0],name=results[1],age=results[2],email=results[3],tel=results[4],city=results[5],category=results[6],about=results[7])
		db.session.add(post)
		db.session.commit()
		p = User.query.get(post.id)
		print(p.date.strftime(date_format))
		p.date = p.date.astimezone(pytz.timezone('US/Pacific'))
		print(p.date.strftime(date_format))
		db.session.commit()
		flash('You have successfully posted your list!')
		return redirect(url_for('base_page'))

	return render_template('Create.html', form=cform)

@app.route('/About.html')
def about_page():
	return render_template('About.html')

@app.route('/FAQ.html')
def faq_page():
	return render_template('FAQ.html')

@app.route('/Listing.html/<post_id>')
def listing_page(post_id):
	post = User.query.get(post_id)
	return render_template('Listing.html', post=post, date=post.date.strftime(date_format))

if __name__ == "__main__":
	app.run(host='0.0.0.0')