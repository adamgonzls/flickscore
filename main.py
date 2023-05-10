from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from editMovieForm import EditMovieForm
from addMovieForm import AddMovieForm

app = Flask(__name__)
app.secret_key = "iwearmysunglassesatnight"
bootstrap = Bootstrap5(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flickscore.db"
db.init_app(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250), nullable=False)

# new_movie = Movie(id=1, title="Moana", year=2016, rating=9.3, ranking=5, description="In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches Moana's island, she answers the Ocean's call to seek out the Demigod to set things right.", img_url="https://m.media-amazon.com/images/M/MV5BMjI4MzU5NTExNF5BMl5BanBnXkFtZTgwNzY1MTEwMDI@._V1_.jpg")

with app.app_context():
    db.create_all()
    # db.session.add(new_movie)
    # db.session.commit()


movie_list = [{
        "id": 1,
        "title": "Matrix",
        "rating": 5.5,
        "description": "lots of words"
    },
    {
        "id": 2,
        "title": "Die Hard",
        "rating": 9.5,
        "description": "John McClain handles business!"
    }]


@app.route("/", methods=["GET", "POST"])
def home():
    all_movies = db.session.query(Movie).all()
    return render_template('index.html', movies=all_movies)


@app.route("/add")
def add_movie():
    return render_template(("addMovie.html"))


@app.route("/edit", methods=['GET', 'POST'])
def edit_movie():
    movie_id = request.args.get("id")
    selected_movie = Movie.query.filter_by(id=movie_id).first()
    edit_movie_form = EditMovieForm()
    if edit_movie_form.validate_on_submit():
        new_rating = edit_movie_form.rating.data
        new_review = edit_movie_form.review.data
        movie_to_update = Movie.query.get(movie_id)
        if new_rating:
            movie_to_update.rating = new_rating
            db.session.commit()
        if new_review:
            movie_to_update.review = new_review
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("editMovie.html", form=edit_movie_form, movie=selected_movie)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
