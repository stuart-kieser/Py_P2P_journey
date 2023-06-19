from flask_sqlalchemy import SQLAlchemy

# base class that we inherit from
# from sqlalchemy.orm import DeclarativeBas

# import flask to iclude browser based app
from flask import Flask, url_for, request, render_template, session, redirect

# imported to create permanent session
from datetime import timedelta

"""
The foreign key fetches the ssn from the table people.ssn
This key refers to the owner of that object
"""


# class Thing(Base):
#    __tablename__ = "things"
#    tid = Column("tid", Integer, primary_key=True)
#    description = Column("description", String)
#    owner = Column(Integer, ForeignKey("people.ssn"))

""" create object to insert into database, new entries will use this object to be unique"""

#    def __init__(self, tid, description, owner):
#        self.tid = tid
#        self.description = description
#        self.owner = owner

#    def __repr__(self):
#        return f"Code:{self.tid}, {self.description} owned by {self.owner}"


"""
create an engine, each db has its own start up, in memory dbs reset every time
below we are connecting to an sqlite db, Base.metadata takes the classes extended from base and creates those tables
"""

# Engine = create_engine("sqlite:///mydb.db", echo=True)
# Base.metadata.create_all(bind=Engine)


"""
Session creates a session that is used as a constructor to add the python object to a db
session.add() is used to add the object to a session, and object must be in a session to commit
session.commit() is used to commit the data update to the db
"""
# Session = sessionmaker(bind=Engine)


"""
Query is used to fetch data from the database
there are fine tuned ways of fetching data such as filtering
"""
# results = session.query(Person).all()

# create the flask app
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=7)

# initialize db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"

db = SQLAlchemy(app)


class Person(db.Model):
    # sets the table name for the database
    # specify column (attributes to an object)
    # ssn is unique identifier
    # ssn = Column("ssn", Integer, primary_key=True)

    """
    The process for creating columns is, create a python attr such as firstname
    specify that it is a column and then what data type it could be
    """
    firstname = db.Column("firstname", db.String, primary_key=True, unique=True)
    lastname = db.Column("lastname", db.String)
    age = db.Column("age", db.Integer)
    password = db.Column("password", db.String)

    """ create object to insert into database, new entries will use this object to be unique"""


db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        fname_ = request.form["fname_"]
        password = request.form["password_"]
        print(f"login in detailes aqquired: FIRSTNAME:{fname_}, PWD:{password}")
        found_user = db.Query
        if found_user:
            session["fname_"] = found_user.firstname
            return redirect(url_for("user", usr=fname_))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")


# registration is working now
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        fname = request.form["fname_"]
        lname = request.form["lname_"]
        age = request.form["age_"]
        password = request.form["password_"]
        users_ = db.Query(Person).all()
        user_ = Person(fname, lname, age, password)
        if user_ in users_:
            return redirect(url_for("login"))
        else:
            db.session.add(user_)
            db.session.commit()
        return redirect(url_for("user", usr=fname))
    else:
        return render_template("register.html")


@app.route("/<usr>")
def user(usr):
    return render_template("user.html")


@app.route("/database")
def data_base():
    results = db.session.query(Person.firstname, Person.lastname, Person.password).all()
    print(results)
    session
    return render_template("_database.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
