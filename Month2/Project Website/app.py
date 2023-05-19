from flask import Flask, url_for, request, render_template, session, redirect

db = []
# create an app instance
app = Flask(__name__)


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
        db_data = request.form[str(db)]
        return render_template("database_entries", db_data=db_data)


if __name__ == "__main__":
    app.run(debug=True)

"""
just a little update, right now, i am able to creat my own db 
with the list function in python to store data. 

That data is also partially callable to the database url page
I think i have figer out how the GET method works.
the error says is cannot understand the request but it does 
list it so it is being received. 
"""
