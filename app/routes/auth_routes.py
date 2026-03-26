from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from . import main
from ..models import User
from .. import db

#####################
# USER MANAGEMENT
#####################

@main.route("/admin/users", methods=["GET", "POST"])
@login_required
def manage_users():

    # ✅ Only admin access
    if current_user.role != "admin":
        flash("Access denied", "danger")
        return redirect(url_for("main.user_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password")
        role = request.form.get("role")

        # ✅ Validation
        if not username or not password:
            flash("Username and password are required", "danger")
            return redirect(url_for("main.manage_users"))

        if len(password) < 4:
            flash("Password must be at least 4 characters", "warning")
            return redirect(url_for("main.manage_users"))

        # ✅ Check duplicate
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("main.manage_users"))

        # ✅ Create user
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

    # ✅ Prevent redirect loop if already logged in
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

    forecast = get_forecast()
    city = "Macheke,ZW"

    return render_template(
        "admin_dashboard.html",
        forecast=forecast,
        city=city
    )

@main.route("/user/dashboard")
@login_required
def user_dashboard():

    from .weather_routes import get_forecast

    forecast = get_forecast()
    city = "Macheke,ZW"

    return render_template(
        "user_dashboard.html",
        forecast=forecast,
        city=city
    )