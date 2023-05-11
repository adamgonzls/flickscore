from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from editMovieForm import EditMovieForm
from addMovieForm import AddMovieForm
import os
import requests

app = Flask(__name__)
app.secret_key = "iwearmysunglassesatnight"
bootstrap = Bootstrap5(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flickscore.db"
db.init_app(app)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_SEARCH_URL = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&language=en-US&query="
TMDB_MOVIE_URL = f"https://api.themoviedb.org/3/movie/"
TMDB_PARAMS = {"api_key": TMDB_API_KEY}
TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w500"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250))

# new_movie = Movie(id=1, title="Moana", year=2016, rating=9.3, ranking=5, description="In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches Moana's island, she answers the Ocean's call to seek out the Demigod to set things right.", img_url="https://m.media-amazon.com/images/M/MV5BMjI4MzU5NTExNF5BMl5BanBnXkFtZTgwNzY1MTEwMDI@._V1_.jpg")


with app.app_context():
    db.create_all()
    # db.session.add(new_movie)
    # db.session.commit()


@app.route("/", methods=["GET", "POST"])
def home():
    all_movies = db.session.query(Movie).all()
    all_movies = db.session.query(Movie).order_by(Movie.rating.desc()).all()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        movie_title = add_movie_form.title.data
        query = f"{movie_title}&page=1&include_adult=false"
        movie_res = requests.get(f"{TMDB_SEARCH_URL}{query}")
        movie_res.raise_for_status()
        movies_json = movie_res.json()["results"]
        # print(movies_json)
        return render_template("selectMovie.html", movies=movies_json)
    return render_template("addMovie.html", form=add_movie_form)


@app.route("/find")
def find_movie():
    movie_id = request.args.get("movie_id")
    edit_movie_form = EditMovieForm()
    selected_movie_res = requests.get(url=f"{TMDB_MOVIE_URL}{movie_id}", params=TMDB_PARAMS)
    selected_movie_res.raise_for_status()
    selected_movie_json = selected_movie_res.json()
    # print(selected_movie_json)
    movie = Movie(
        title=selected_movie_json['title'],
        year=selected_movie_json['release_date'],
        description=selected_movie_json['overview'],
        img_url=f"{TMDB_IMG_BASE}{selected_movie_json['poster_path']}"
    )
    db.session.add(movie)
    db.session.commit()
    selected_movie = movie
    return redirect(url_for("edit_movie", id=movie.id))
    # return render_template("editMovie.html", form=edit_movie_form, movie=selected_movie)


@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    movie_id = request.args.get("id")
    selected_movie = Movie.query.filter_by(id=movie_id).first()
    edit_movie_form = EditMovieForm()
    if edit_movie_form.validate_on_submit():
        new_rating = edit_movie_form.rating.data
        new_review = edit_movie_form.review.data
        movie_to_update = db.session.get(Movie, movie_id)
        if new_rating:
            movie_to_update.rating = new_rating
            db.session.commit()
        if new_review:
            movie_to_update.review = new_review
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("editMovie.html", form=edit_movie_form, movie=selected_movie)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie_to_delete = db.session.get(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
