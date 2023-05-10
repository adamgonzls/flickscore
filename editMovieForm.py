from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField


class EditMovieForm(FlaskForm):
    rating = FloatField(label="Your rating out of 10:")
    review = StringField(label="Your review:")
    submit = SubmitField(label="Submit")
