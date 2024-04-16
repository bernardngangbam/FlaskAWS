from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:adminpass@flaskdb.c704aii4yrx5.ap-south-1.rds.amazonaws.com/flaskaws'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = "appsecretkey"

db = SQLAlchemy(application)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float)

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

@application.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html',books = books)

@application.route('/add', methods=['POST'])
def insert_book():
    if request.method == 'POST':
        book = Book(
            title = request.form.get('title'),
            author = request.form.get('author'),
            price = request.form.get('price')
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully")
        return redirect(url_for('index'))
    
@application.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        my_data = Book.query.get(request.form.get('id'))
        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']
        db.session.commit()
        flash("Book updated successfully")
        return redirect(url_for('index'))

@application.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book deleted successfully")
    return redirect(url_for('index'))

if __name__ == "__main__":
    application.run(debug=True)
