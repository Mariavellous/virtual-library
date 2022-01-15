from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "elephant"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my-library.db'
# If you get a deprecation warning in the console that's related to SQL_ALCHEMY_TRACK_MODIFICATIONS. You can silence it with:
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a table in this database called book
class Book(db.Model):
# There are four fields with respective limitations
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(250), unique=True, nullable=False)
  author = db.Column(db.String(250), nullable=False)
  rating = db.Column(db.Float, nullable=False)


db.create_all()

@app.route('/')
def home():
  books = Book.query.all()
  print(books)
  return render_template('index.html', data=books, length=len(books))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
      title = request.form["title"]
      author = request.form["author"]
      rating = request.form["rating"]
      book = Book(title=title, author=author, rating=rating)
      db.session.add(book)
      db.session.commit()

      # NOTE: You can use the redirect method from flask to redirect to another route
      # e.g. in this case to the home page after the form has been submitted.
      return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
  if request.method == "GET":
    book = Book.query.filter_by(id=book_id).first()
    return render_template("edit.html", book_id=book_id, book=book)
  else:
    if request.method == "POST":
      book_to_update = Book.query.get(book_id)
      book_to_update.rating = request.form["rating"]
      db.session.commit()
      return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

