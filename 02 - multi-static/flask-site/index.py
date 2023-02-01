"""
Flask application for experience puposes
"""
from datetime import timedelta
from flask import Flask, redirect, request, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/second")
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app=app)

class Users(db.Model):
    """
    User model for database
    """
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    """
    Home route
    """
    return render_template("index.html")

@app.route("/view")
def view():
    """view route
    For check all the users that are registered

    Returns:
        str: template of page
    """
    return render_template("view.html", values = Users.query.all())

@app.route("/catpage")
def cat():
    """cat route
    Just in case you wanna see a cat

    Returns:
        str: template of page
    """
    return render_template("catpage.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    """User route

    Returns:
        str: template of page
    """
    email = None
    if "user_name" in session:
        user_name = session["user_name"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name = user_name).first()
            found_user.email = email
            db.session.commit()
            flash("Email saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route

    Returns:
        str: template of the page
    """
    if request.method == "POST":
        session.permament = True
        user_name = request.form["nm"]
        session["user_name"] = user_name

        found_user = Users.query.filter_by(name = user_name).first()

        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user_name, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful")
        return redirect(url_for("user", usr=user_name))
    else:
        if "user_name" in session:
            flash("User already logged in")
            return redirect(url_for("user"))
        flash("You are not logg ed in")
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout route"""
    flash("You have been logged out", "info")
    session.pop("user_name", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=3000, debug=True)
