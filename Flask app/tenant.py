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
        return f"Tenant:id={self.id}, name='{self.name}', age={self.age}"


class room(db.Model):
    roomnum = db.Column(db.Integer, primary_key=True)
    tenant_1 = db.Column(db.Integer, db.ForeignKey("tenant.id"))
    tenant_2 = db.Column(db.Integer, db.ForeignKey("tenant.id"))

    tenant_1_id = db.relationship("tenant", foreign_keys=[tenant_1])
    tenant_2_id = db.relationship("tenant", foreign_keys=[tenant_2])

    def __init__(self, roomnum, tenant_1, tenant_2):
        self.roomnum = roomnum
        self.tenant_1 = tenant_1
        self.tenant_2 = tenant_2

    def __repr__(self):
        return f"Room: {self.roomnum}, T1: {self.tenant_1}, T2: {self.tenant_2}"


def create_rooms():
    existing_rooms = room.query.all()
    if existing_rooms:
        return existing_rooms
    else:
        rooms = []
        for i in range(10):
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


@app.route("/<user>", methods=["GET", "POST"])
def usr(user):
    user_obj = tenant.query.filter_by(name=user).first()

    if user_obj is None:
        return redirect(url_for("database"))

    user_id = user_obj.id

    tenant_room = room.query.filter_by(tenant_1=user_id).first()
    if not tenant_room:
        tenant_room = room.query.filter_by(tenant_2=user_id).first()

    return render_template("user.html", user=user, tenant_room=tenant_room)


@app.route("/database", methods=["POST", "GET"])
def database():
    content = tenant.query.all()
    if request.method == "POST":
        tenant_id = request.form.get("view_tenant")
        if tenant_id:
            return redirect(url_for("usr", user=tenant_id))

    return render_template("database.html", content=content)


@app.route("/remove_tenant/<int:tenant_id>", methods=["POST"])
def remove_tenant(tenant_id):
    tenant_to_remove = tenant.query.filter_by(id=tenant_id).first()
    room_to_evict = room.query.filter_by(tenant_1=tenant_id).first()
    print(f"tenant and room found [{tenant_to_remove}], Room: {room_to_evict}")
    if not room_to_evict:
        room_to_evict = room.query.filter_by(tenant_2=tenant_id).first()
    if tenant_to_remove:
        if room_to_evict.tenant_1:
            room_to_evict.tenant_1 = None
        else:
            room_to_evict.tenant_2 = None
        db.session.commit()
        print("commiting to database...")
    db.session.delete(tenant_to_remove)
    db.session.commit()
    flash(f"{tenant_to_remove} removed successfully", "success")
    return redirect(url_for("database"))


@app.route("/edit/<int:tenant_id>", methods=["POST", "GET"])
def edit(tenant_id):
    rooms = room.query.all()
    # roomnum = request.form["room.roomnum"]
    if request.method == "POST":
        room_num = request.form.get("room_num")
        tenant_room = room.query.filter_by(roomnum=room_num).first()
        if tenant_room:
            if tenant_room.tenant_1 == None:
                tenant_room.tenant_1 = tenant_id
            elif tenant_room.tenant_2 == None:
                tenant_room.tenant_2 = tenant_id
            print("commiting to databas...")
            db.session.commit()
            return redirect(url_for("usr", user=tenant_id))
    return render_template("edit.html", tenant_id=tenant_id, rooms=rooms)


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
        rooms = create_rooms()
        for room_ in rooms:
            db.session.add(room_)
            db.session.commit()
    app.run(debug=True)
