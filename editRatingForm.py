from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField


class EditRatingForm(FlaskForm):
    rating = StringField(label="New Rating")
    book_id = HiddenField(label="Book ID")
    submit = SubmitField(label="Submit")
