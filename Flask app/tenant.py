from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db creation
db = SQLAlchemy()
db.init_app(app)


class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        db.add(id, name)
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
