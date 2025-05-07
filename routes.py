from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt
from models import User, Flight, Booking
from forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/flights')
def flights():
    flights = Flight.query.all()
    return render_template('flights.html', flights=flights)

@main_bp.route('/book/<int:flight_id>', methods=['POST'])
@login_required
def book(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    if flight.seats_available <= 0:
        flash('No seats available', 'danger')
        return redirect(url_for('main.flights'))
    
    booking = Booking(user_id=current_user.id, flight_id=flight.id)
    flight.seats_available -= 1
    db.session.add(booking)
    db.session.commit()
    flash('Flight booked successfully!', 'success')
    return redirect(url_for('main.my_bookings'))

@main_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', bookings=bookings)