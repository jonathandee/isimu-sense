from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import main
from ..models import User


#       ADD USER        #
#_______________________#

from flask_login import login_required, current_user
from .. import db
from ..models import User


@main.route("/admin/users", methods=["GET", "POST"])
@login_required
def manage_users():

    # Only admin should access
    if current_user.role != "admin":
        flash("Access denied", "danger")
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        user = User(username=username, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User created successfully", "success")

        return redirect(url_for("main.manage_users"))

    users = User.query.all()

    return render_template("manage_users.html", users=users)


#####################
#       LOG IN      #
#####################

@main.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.dashboard"))

        flash("Invalid username or password", "danger")

    return render_template("index.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))