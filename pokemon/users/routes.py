from flask import Blueprint, render_template, request, redirect, flash, url_for
from pokemon.extensions import db, bcrypt
from pokemon.models import User
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin

users_bp = Blueprint('users', __name__, template_folder='templates')


# ⭐ กัน open redirect
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# ================= USERS PAGE =================
@users_bp.route('/users')
@login_required
def users():
    return render_template('index.html', title='Users Page')


# ================= REGISTER =================
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.users'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 🔍 check username
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!', 'warning')
            return redirect(url_for('users.register'))

        # 🔍 check email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', 'warning')
            return redirect(url_for('users.register'))

        # 🔐 check password match
        if password != confirm_password:
            flash('Your passwords do not match!', 'warning')
            return redirect(url_for('users.register'))

        # 🔒 hash password
        pwd_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # 💾 save user
        new_user = User(username=username, email=email, password=pwd_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Register successful!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register Page')


# ================= LOGIN =================
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.users'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)

            flash('Login successful!', 'success')
            return redirect(url_for('users.users'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template('users/login.html', title='Login Page')


# ================= LOGOUT =================
@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('users.login'))


# ================= PROFILE =================
@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.firstname = request.form.get('firstname')
        current_user.lastname = request.form.get('lastname')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('users.profile'))

    return render_template('users/profile.html', title='Profile Page')


# ================= CHANGE PASSWORD =================
@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # ✅ เช็ครหัสเดิม
        if not bcrypt.check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect!', 'danger')
            return redirect(url_for('users.change_password'))

        # ✅ เช็ครหัสใหม่ตรงกัน
        if new_password != confirm_password:
            flash('New passwords do not match!', 'warning')
            return redirect(url_for('users.change_password'))

        # ✅ hash รหัสใหม่
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()

        flash('Password updated successfully!', 'success')
        return redirect(url_for('users.profile'))

    return render_template('users/change_password.html', title='Change Password')