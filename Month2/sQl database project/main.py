"""
# sql turns python object into data base entry
# create_engine creates an engine that we connect to for the database
# ForeignKey i belive is the key to the database that we define
"""

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR

# base class that we inherit from
from sqlalchemy.orm import DeclarativeBase

# makes session we can do stuff to the db
from sqlalchemy.orm import sessionmaker

# import flask to iclude browser based app
from flask import Flask, url_for, request, render_template, session, redirect


class Base(DeclarativeBase):
    pass


class Person(Base):
    # sets the table name for the database
    __tablename__ = "people"

    # specify column (attributes to an object)
    # ssn is unique identifier
    ssn = Column("ssn", String, primary_key=True)

    """
    The process for creating columns is, create a python attr such as firstname
    specify that it is a column and then what data type it could be
    """

    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    """ create object to insert into database, new entries will use this object to be unique"""

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    # allows us to choose how we print a person or what we see when we call that person
    def __repr__(self):
        return f"({self.ssn})"


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

Engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=Engine)


"""
Session creates a session that is used as a constructor to add the python object to a db
session.add() is used to add the object to a session, and object must be in a session to commit
session.commit() is used to commit the data update to the db
"""
Session = sessionmaker(bind=Engine)


"""
Query is used to fetch data from the database
there are fine tuned ways of fetching data such as filtering
"""
# results = session.query(Person).all()

# create the flask app
app = Flask(__name__)

session = Session()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        user_ssn = request.form["ssn"]
        user_name = request.form["usr"]
        results = session.query(Person.ssn, Person.firstname)
        if user_name == Person.firstname and user_ssn == Person.ssn:
            redirect(url_for("user"))
    else:
        return render_template("login.html")
    # come back and look at login authentication


@app.route("/database")
def data_base():
    results = session.query(Person.ssn).all()
    print(results)
    return render_template("_database.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
