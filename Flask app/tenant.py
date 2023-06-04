from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "12345"

# db creation
db = SQLAlchemy(app)


class tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)

    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Tenant(id={self.id}, name='{self.name}', age={self.age})"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        age = request.form["age"]
        session["name"] = name
        found_user = tenant.query.filter_by(name=name).first()

        if found_user:
            session["name"] = found_user.name
            return redirect(url_for("login"))

        else:
            user = tenant(id, name, age)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("usr", user=name))

    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        session["name"] = name
        found_user = tenant.query.filter_by(name=name).first()
        if found_user:
            return redirect(url_for("usr", user=name))
        else:
            if "name" in session:
                return redirect(url_for("usr", user=name))
            else:
                return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/user")
def usr():
    if "name" in session:
        name = session["name"]
        return render_template("user.html", user=name)


@app.route("/database", methods=["POST", "GET"])
def database():
    content = tenant.query.all()
    return render_template("database.html", content=content)


@app.route("/logout")
def logout():
    session.pop("name", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
