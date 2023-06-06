from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "12345"
app.permanent_session_lifetime = timedelta(days=5)

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
        return f"Tenant:id={self.id}, name='{self.name}', age={self.age})"


class room(db.Model):
    roomnum = db.Column(db.Integer, primary_key=True)
    tenant_1 = db.Column(db.Integer, db.ForeignKey("tenant.id"))
    tenant_2 = db.Column(db.String, db.ForeignKey("tenant.id"))

    tenant_1_id = db.relationship("tenant", foreign_keys=[tenant_1])
    tenant_2_id = db.relationship("tenant", foreign_keys=[tenant_2])

    def __init__(self, roomnum, tenant_1, tenant_2):
        self.roomnum = roomnum
        self.tenant_1 = tenant_1
        self.tenant_2 = tenant_2

    def __repr__(self):
        return f"Room: {self.roomnum}, T1: {self.tenant_1}, T2: {self.tenant_2}"


def create_rooms():
    rooms = []
    for i in range(500):
        room_ = room(i, None, None)
        rooms.append(room_)
    return rooms


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
            flash("You already have an account.", "info")
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
        session.permanent = True
        id = request.form["id"]
        name = request.form["name"]
        session["name"] = name
        found_user = tenant.query.filter_by(name=name).first()
        if found_user:
            return redirect(url_for("usr", user=name))
        else:
            flash("Account details do not exist.")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/<user>")
def usr(user):
    if "name" in session:
        name = session.get("name")
    all_rooms = room.query.all()
    return render_template("user.html", user=name, all_rooms=all_rooms)


@app.route("/database", methods=["POST", "GET"])
def database():
    content = tenant.query.all()

    if request.method == "POST":
        if request.form.get("view") == "tenant":
            return redirect(url_for("usr"))

    return render_template("database.html", content=content)


@app.route("/remove_tenant/<int:tenant_id>", methods=["POST"])
def remove_tenant(tenant_id):
    tenant_to_remove = tenant.query.get(tenant_id)
    if tenant_to_remove:
        db.session.delete(tenant_to_remove)
        db.session.commit()
        flash(f"{tenant_to_remove} removed successfully", "success")
    else:
        flash(f"{tenant_to_remove} does not exist.")
    return redirect(url_for("database"))


@app.route("/logout")
def logout():
    if "name" in session:
        session.pop("name", None)
        flash("You have been logged out", "info")
        return redirect(url_for("login"))
    else:
        flash("You haven't logged in.", "info")
        return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

rooms = create_rooms()
with app.app_context():
    for room_ in rooms:
        db.session.add(room_)
    db.session.commit()
    
