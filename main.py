from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from editRatingForm import EditRatingForm

app = Flask(__name__)
app.secret_key = "iwearmysunglassesatnight"
bootstrap = Bootstrap5(app)

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
    return render_template('index.html', movies=movie_list)


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    edit_rating_form = EditRatingForm()
    # if edit_rating_form.validate_on_submit():
    #     print(edit_rating_form.book_id.data)
    #     print(edit_rating_form)
    return f"<p>{id}</p>"

if __name__ == '__main__':
    app.run(debug=True)