from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

movie_list = [{
        "title": "Matrix",
        "rating": 5.5,
        "description": "lots of words"
    },
    {
        "title": "Die Hard",
        "rating": 9.5,
        "description": "John McClain handles business!"
    }]

@app.route("/")
def home():
    return render_template('index.html', movies=movie_list)

if __name__ == '__main__':
    app.run(debug=True)