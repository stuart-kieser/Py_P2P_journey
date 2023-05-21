from flask import Flask, url_for, request, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# this variable, db, is the db for this entire app
# db = SQLAlchemy()
db = []


# create an app instance
app = Flask(__name__)

db_main = "register.db"

# contains the databse connection string
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + db_main


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = request.form["str"]
        db.append(form_data)
        return redirect(url_for("user_profile", user=form_data))
    else:
        return render_template("login.html")


@app.route("/users/<user>")
def user_profile(user):
    return render_template("user.html")


@app.route("/database", methods=["GET"])
def database_entries():
    if request.method == "GET":
        db = request.args.get("str")
        return render_template("_db.html", db=db)


if __name__ == "__main__":
    app.run(debug=True)

"""
just a little update, right now, i am able to create my own db 
with the list function in python to store data. 

That data is also partially callable to the database url page
I think i have figure out how the GET method works.
the error says it cannot understand the request but it does 
list it so it is being received. 
"""
