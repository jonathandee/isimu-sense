import re
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from .weather_routes import get_forecast
from sqlalchemy.exc import IntegrityError
from ..models import Animal, Planting, InventoryItem
from . import main
from ..models import User
from .. import db

#####################
# USER MANAGEMENT
#####################

def is_strong_password(password):
    return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$', password)


@main.route("/admin/users", methods=["GET", "POST"])
@login_required
def manage_users():

    #Only admin access
    if current_user.role != "admin":
        flash("Access denied", "danger")
        return redirect(url_for("main.user_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        #Basic validation
        if not username or not password:
            flash("Username and password are required", "danger")
            return redirect(url_for("main.manage_users"))

        #Confirm password check
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("main.manage_users"))

        #Strong password validation
        if not is_strong_password(password):
            flash(
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character",
                "danger"
            )
            return redirect(url_for("main.manage_users"))

        #Check duplicate username
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("main.manage_users"))

        #Create user
        user = User(username=username, role=role)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            flash("User created successfully", "success")

        except IntegrityError:
            db.session.rollback()
            flash("Error creating user. Try again.", "danger")

        return redirect(url_for("main.manage_users"))

    #GET request
    users = User.query.all()
    return render_template("manage_users.html", users=users)

#####################
# EDIT USER
#####################

@main.route("/admin/users/edit/<int:id>", methods=["POST"])
@login_required
def edit_user(id):

    if current_user.role != "admin":
        abort(403)

    user = User.query.get_or_404(id)

    username = request.form.get("username", "").strip()
    role = request.form.get("role")

    if not username:
        flash("Username cannot be empty", "danger")
        return redirect(url_for("main.manage_users"))

    # Prevent duplicate username
    existing_user = User.query.filter_by(username=username).first()
    if existing_user and existing_user.id != user.id:
        flash("Username already taken", "danger")
        return redirect(url_for("main.manage_users"))

    # Prevent removing your own admin rights
    if user.id == current_user.id and role != "admin":
        flash("You cannot remove your own admin rights", "warning")
        return redirect(url_for("main.manage_users"))

    user.username = username
    user.role = role

    db.session.commit()

    flash("User updated successfully", "success")
    return redirect(url_for("main.manage_users"))

#####################
# DELETE USER
#####################

@main.route("/admin/users/delete/<int:id>")
@login_required
def delete_user(id):

    if current_user.role != "admin":
        abort(403)

    user = User.query.get_or_404(id)

    # Prevent deleting yourself
    if user.id == current_user.id:
        flash("You cannot delete your own account", "warning")
        return redirect(url_for("main.manage_users"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully", "success")
    return redirect(url_for("main.manage_users"))

#####################
# LOGIN
#####################

@main.route("/", methods=["GET", "POST"])
def login():

    #Prevent redirect loop if already logged in
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("main.admin_dashboard"))
        else:
            return redirect(url_for("main.user_dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            if user.role == "admin":
                return redirect(url_for("main.admin_dashboard"))
            else:
                return redirect(url_for("main.user_dashboard"))

        flash("Invalid username or password", "danger")

    return render_template("index.html")

#####################
# LOGOUT
#####################

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("main.login"))

#####################
# DASHBOARDS
#####################

@main.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        abort(403)

    from .weather_routes import get_forecast
    from ..models import Planting, InventoryItem, Animal 
    from .. import db

    # Weather
    forecast = get_forecast()
    city = "Macheke,ZW"

    crop_count = Planting.query.count()
    livestock_count = Animal.query.count()  
    inventory_count = InventoryItem.query.count()

    balance = 0

    return render_template(
        "admin_dashboard.html",
        forecast=forecast,
        city=city,
        crop_count=crop_count,
        livestock_count=livestock_count,
        inventory_count=inventory_count,
        balance=balance
    )

@main.route("/user/dashboard")
@login_required
def user_dashboard():

    #Weather
    forecast = get_forecast()
    city = "Macheke,ZW"

    crop_count = Planting.query.count()
    livestock_count = Animal.query.count()
    inventory_count = InventoryItem.query.count()

    #balance = 0

    return render_template(
        "user_dashboard.html",
        forecast=forecast,
        city=city,
        crop_count=crop_count,
        livestock_count=livestock_count,
        inventory_count=inventory_count,
        balance=balance
    )