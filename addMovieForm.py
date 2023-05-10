from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AddMovieForm(FlaskForm):
    review = StringField(label="Movie Title:")
    submit = SubmitField(label="Add Movie")