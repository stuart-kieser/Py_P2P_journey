from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# creates instance of an app
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/public")
def public():
    # access database and print the entire thing in order
    return render_template("public.html")


@app.route("/database")
def database():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
