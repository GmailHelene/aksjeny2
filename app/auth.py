from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User
from app.forms import LoginForm, RegistrationForm

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # Check if there's a next parameter to redirect to
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Redirect to next page after successful login
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        # Check if there's a next parameter to redirect to
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        # Pass next parameter to login page
        next_page = request.args.get('next')
        if next_page:
            return redirect(url_for("auth.login", next=next_page))
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate current password
        if not current_user.check_password(current_password):
            flash('Nåværende passord er feil.', 'error')
            return render_template('change_password.html')
            
        # Validate new password
        if new_password != confirm_password:
            flash('De nye passordene stemmer ikke overens.', 'error')
            return render_template('change_password.html')
            
        if len(new_password) < 6:
            flash('Passord må være minst 6 tegn.', 'error')
            return render_template('change_password.html')
            
        # Update password
        try:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Passord oppdatert!', 'success')
            return redirect(url_for('main.settings'))
        except Exception as e:
            flash('Feil ved oppdatering av passord.', 'error')
            db.session.rollback()
            
    return render_template('change_password.html')


