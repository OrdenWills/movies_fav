
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, FloatField
from data_manager import DataManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-list.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    review = db.Column(db.String(120))
    img_url = db.Column(db.String(120))

    def __repr__(self):
        return f"<Movies{Movies.title}>"


class EditForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 eg 7.5", [validators.DataRequired("rating require, takes a number")])
    review = StringField("Your review", [validators.DataRequired("review required")])
    submit = SubmitField("Done")


class AddForm(FlaskForm):
    title = StringField("Movie Title", [validators.DataRequired("please input the name of movie you want to add")])
    submit = SubmitField("Add Movie")

# db.create_all()

# new_movie = Movies(
#     title="phone booth",
#     year=2002,
#     description="publicist start shepard finds himself trapped in a phone booth, pinned down by an extortionist's"
#                 " sniper rifle. Unable to leave or receive outside help, Stuart's negotiation "
#                 "with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


@app.route("/")
def home():
    all_movies = Movies.query.order_by(desc(Movies.rating))
    return render_template("index.html", movies=all_movies)


@app.route("/edit<id>", methods=["POST", "GET"])
def edit_page(id):
    form = EditForm()

    if form.validate_on_submit():
        new_rating = form.rating.data
        new_review = form.review.data
        updated_movie = Movies.query.get(id)
        updated_movie.rating = new_rating
        updated_movie.review = new_review
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form)


@app.route("/add", methods=["POST", "GET"])
def add_page():
    form = AddForm()
    data = DataManager()
    if form.validate_on_submit():
        name = form.title.data
        movies_data = data.send_request(name)
        return render_template("select.html", movies_data=movies_data)
    return render_template("add.html", form=form)


@app.route("/delete<id>")
def delete_row(id):
    movie_to_delete = Movies.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/select")
def select_movie():
    data = DataManager()
    movie_id = int(request.args.get('id'))
    # print(type(movie_id))
    movie_detail = data.get_details(movie_id)
    print(movie_detail)
    # print(movie_detail['genere'])
    title = movie_detail["title"]
    year = int(movie_detail["release_date"].split("-")[0])
    description = movie_detail["overview"]
    img_url = f"https://image.tmdb.org/t/p/w500{movie_detail['poster_path']}"
    new_movie = Movies(title=title, year=year, description=description, img_url=img_url)
    db.session.add(new_movie)
    db.session.commit()
    current_id = len(Movies.query.all())
    return redirect(url_for("edit_page", id=current_id))


if __name__ == '__main__':
    app.run(debug=True)
