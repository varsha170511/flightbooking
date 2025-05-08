from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
from datetime import datetime, timedelta
import random
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database configuration - Changed to SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flight_booking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Flask-Login configuration  
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # <-- Increased length for bcrypt hashes
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return str(self.id)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(50))
    flight_number = db.Column(db.String(10))
    origin = db.Column(db.String(100))
    origin_code = db.Column(db.String(3))
    destination = db.Column(db.String(100))
    destination_code = db.Column(db.String(3))
    departure_time = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)
    duration = db.Column(db.String(20))
    price = db.Column(db.Float)
    seats_available = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    booking_reference = db.Column(db.String(20), unique=True)
    travelers = db.Column(db.JSON)  # Stores traveler details as JSON
    total_price = db.Column(db.Float)
    status = db.Column(db.String(20), default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit = SubmitField('Login')
class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    agree_terms = BooleanField('I agree to terms and conditions', validators=[DataRequired()])
    submit = SubmitField('Register')
class SearchForm(FlaskForm):
    origin = SelectField('From', choices=[
        ('NYC', 'New York (JFK)'),
        ('LON', 'London (Heathrow)'),
        ('DEL', 'Delhi (IGI)'),
        ('TOK', 'Tokyo (Narita)')
    ])
    destination = SelectField('To', choices=[
        ('NYC', 'New York (JFK)'),
        ('LON', 'London (Heathrow)'),
        ('DEL', 'Delhi (IGI)'),
        ('TOK', 'Tokyo (Narita)')
    ])
    departure = DateField('Departure Date', format='%Y-%m-%d')
    passengers = SelectField('Passengers', 
                           choices=[(i, str(i)) for i in range(1, 10)],
                           coerce=int,
                           default=1)
    submit = SubmitField('Search Flights')



# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.args if request.method == 'GET' else None)
    
    if form.validate_on_submit() or request.method == 'GET':
        # Get the actual searched values
        origin_code = form.origin.data or request.args.get('origin', 'NYC')
        destination_code = form.destination.data or request.args.get('destination', 'LON')
        
        # Map codes to full city names
        city_map = {
            'NYC': 'New York (JFK)',
            'LON': 'London (Heathrow)',
            'DEL': 'Delhi (IGI)',
            'TOK': 'Tokyo (Narita)'
        }
        
        origin = city_map.get(origin_code, 'New York')
        destination = city_map.get(destination_code, 'London')
        
        # Rest of your parameters...
        departure_date = form.departure.data.strftime('%Y-%m-%d') if form.departure.data else request.args.get('departure_date')
        return_date = request.args.get('return_date', '')
        passengers = form.passengers.data or int(request.args.get('passengers', 1))
        flight_class = request.args.get('flight_class', 'economy')

        # Generate flights with ACTUAL searched routes
        flights = []
        airlines = ['SkyWings Airlines', 'Global Airways']
        
        for i in range(10):
            flights.append({
                'id': i + 1,
                'airline': random.choice(airlines),
                'airline_logo': f"{random.choice(airlines).lower().replace(' ', '-')}.png",
                'flight_number': f"{random.choice(['SW', 'GA'])}{random.randint(100, 999)}",
                'origin': origin,
                'origin_code': origin_code,
                'destination': destination,
                'destination_code': destination_code,
                # Rest of your flight data generation...
                'departure_time': f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}",
                'arrival_time': f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}",
                'duration': f"{random.randint(1, 12)}h {random.randint(0, 59)}m",
                'price': random.randint(200, 800),
                'flight_class': flight_class,
                'stops': random.choice([0, 0, 0, 1]),
                'seats_left': random.randint(5, 30)
            })
        
        return render_template('search.html', 
                            flights=flights,
                            origin=origin,
                            destination=destination,
                            departure_date=departure_date,
                            return_date=return_date,
                            passengers=passengers,
                            flight_class=flight_class,
                            form=form)
    
    return render_template('search.html', form=form)

@app.route('/flight/<int:flight_id>')
def flight_details(flight_id):
    # Get search parameters from request
    origin_code = request.args.get('origin', 'NYC')
    destination_code = request.args.get('destination', 'LON')
    passengers = request.args.get('passengers', 1, type=int)
    flight_class = request.args.get('flight_class', 'economy')
    return_date = request.args.get('return_date', None)
    
    # Map airport codes to city names
    city_names = {
        'NYC': 'New York',
        'LON': 'London',
        'DEL': 'Delhi',
        'TOK': 'Tokyo'
    }
    
    # Flight data - now dynamic based on search parameters
    flight = {
        'id': flight_id,
        'airline': 'SkyWings Airlines',
        'airline_logo': 'skywings-airlines.png',
        'flight_number': f"SW{random.randint(100, 999)}",
        'origin': city_names.get(origin_code, 'New York'),
        'origin_code': origin_code,
        'destination': city_names.get(destination_code, 'London'),
        'destination_code': destination_code,
        'departure_time': f"{random.randint(6, 23):02d}:{random.choice(['00', '15', '30', '45'])}",
        'arrival_time': f"{random.randint(6, 23):02d}:{random.choice(['00', '15', '30', '45'])}",
        'departure_date': datetime.today().strftime('%Y-%m-%d'),
        'duration': f"{random.randint(1, 12)}h {random.randint(0, 59)}m",
        'price': random.randint(200, 800),
        'base_price': random.randint(150, 600),
        'taxes': random.randint(30, 100),
        'service_fee': 15,
        'stops': random.choice([0, 0, 0, 1]),
        'seats_left': random.randint(5, 30),
        'flight_class': flight_class,
        'checked_baggage': 1,
        'passengers': passengers
    }
    
    # If round trip, add return flight
    if return_date:
        flight['return_flight'] = {
            'id': flight_id + 100,
            'airline': 'SkyWings Airlines',
            'airline_logo': 'skywings-airlines.png',
            'flight_number': f"SW{random.randint(100, 999)}",
            'origin': city_names.get(destination_code, 'London'),
            'origin_code': destination_code,
            'destination': city_names.get(origin_code, 'New York'),
            'destination_code': origin_code,
            'departure_time': f"{random.randint(6, 23):02d}:{random.choice(['00', '15', '30', '45'])}",
            'arrival_time': f"{random.randint(6, 23):02d}:{random.choice(['00', '15', '30', '45'])}",
            'departure_date': return_date,
            'duration': f"{random.randint(1, 12)}h {random.randint(0, 59)}m",
            'price': random.randint(200, 800),
            'base_price': random.randint(150, 600),
            'taxes': random.randint(30, 100),
            'service_fee': 15,
            'stops': random.choice([0, 0, 0, 1]),
            'seats_left': random.randint(5, 30),
            'flight_class': flight_class,
            'checked_baggage': 1
        }
        flight['price'] += flight['return_flight']['price']
    
    return render_template('flight-details.html', flight=flight)

@app.route('/booking/<int:flight_id>', methods=['GET', 'POST'])
@login_required
def booking(flight_id):
    # In a real app, this would come from the database
    flight = {
        'id': flight_id,
        'airline': 'SkyWings Airlines',
        'origin': 'New York',
        'origin_code': 'NYC',
        'destination': 'London',
        'destination_code': 'LON',
        'departure_time': '09:30',
        'arrival_time': '21:15',
        'departure_date': 'December 15, 2023',
        'duration': '7h 45m',
        'price': 399,
        'base_price': 299,
        'taxes': 85,
        'service_fee': 15,
        'flight_class': 'economy'
    }
    
    passengers = int(request.args.get('passengers', 1))
    
    if request.method == 'POST':
        # Process form data and create booking
        # In a real app, this would save to the database
        booking_reference = f"SW{random.randint(100000, 999999)}"
        
        # Get traveler data from form
        travelers = []
        for i in range(passengers):
            travelers.append({
                'first_name': request.form.get(f'firstName{i}'),
                'last_name': request.form.get(f'lastName{i}'),
                'title': request.form.get(f'title{i}'),
                'dob': request.form.get(f'dob{i}'),
                'nationality': request.form.get(f'nationality{i}'),
                'passport_number': request.form.get(f'passport{i}'),
                'passport_expiry': request.form.get(f'passportExpiry{i}'),
                'frequent_flyer_number': request.form.get(f'frequentFlyer{i}') or None
            })
        
        # Redirect to payment page
        return redirect(url_for('payment', flight_id=flight_id, booking_reference=booking_reference))
    
    return render_template('booking.html', flight=flight, passengers=passengers)

@app.route('/payment/<int:flight_id>')
@login_required
def payment(flight_id):
    booking_reference = request.args.get('booking_reference', f"SW{random.randint(100000, 999999)}")
    
    # Create a booking object with all required information
    booking = {
        'id': random.randint(1000, 9999),  # Temporary ID for demo
        'booking_reference': booking_reference,
        'total_price': 399,  # This should come from the actual flight price
        'status': 'pending',
        'travelers': [
            {
                'first_name': 'John',
                'last_name': 'Doe'
            }
            # Add more travelers based on the actual booking data
        ]
    }

    # Get flight data
    flight = {
        'id': flight_id,
        'airline': 'SkyWings Airlines',
        'origin': 'New York',
        'origin_code': 'NYC',
        'destination': 'London',
        'destination_code': 'LON',
        'departure_time': '09:30',
        'arrival_time': '21:15',
        'departure_date': 'December 15, 2023',
        'duration': '7h 45m',
        'price': 399,
        'base_price': 299,
        'taxes': 85,
        'service_fee': 15,
        'flight_class': 'economy'
    }
    
    passengers = int(request.args.get('passengers', 1))
    travelers = []
    for i in range(passengers):
        travelers.append({
            'first_name': f'Traveler {i+1}',
            'last_name': 'Smith',
            'title': 'Mr.',
            'seat': f'{random.randint(10, 30)}{random.choice(["A", "B", "C", "D", "E", "F"])}'
        })
    
    return render_template('payment.html', 
                         flight=flight, 
                         travelers=travelers,
                         booking=booking,  # Add the booking object
                         booking_reference=booking_reference,
                         passengers=passengers)

@app.route('/process-payment', methods=['POST'])
@login_required
def process_payment():
    try:
        booking_reference = request.form.get('booking_reference', f"SW{random.randint(100000, 999999)}")
        flight_id = int(request.form.get('flight_id'))
        
        # Get the flight from database or create one if it doesn't exist (for demo)
        flight = Flight.query.get(flight_id)
        if not flight:
            flight = Flight(
                id=flight_id,
                airline='SkyWings Airlines',
                flight_number=f"SW{random.randint(100, 999)}",
                origin='New York',
                origin_code='NYC',
                destination='London',
                destination_code='LON',
                departure_time=datetime.strptime('2023-12-15 09:30:00', '%Y-%m-%d %H:%M:%S'),
                arrival_time=datetime.strptime('2023-12-15 21:15:00', '%Y-%m-%d %H:%M:%S'),
                duration='7h 45m',
                price=399.0,
                seats_available=150
            )
            db.session.add(flight)
        
        # Create the booking
        booking = Booking(
            user_id=current_user.id,
            flight_id=flight_id,
            booking_reference=booking_reference,
            travelers=[{
                'first_name': request.form.get('firstName0'),
                'last_name': request.form.get('lastName0'),
                'title': request.form.get('title0', 'Mr.'),
            }],  # For simplicity, just storing the first traveler
            total_price=float(request.form.get('total_price', 399.0)),
            status='confirmed'
        )
        
        # Update flight seats
        flight.seats_available = max(0, flight.seats_available - 1)
        
        # Save to database
        db.session.add(booking)
        db.session.commit()
        
        flash('Payment processed successfully!', 'success')
        return redirect(url_for('confirmation', booking_reference=booking_reference))
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Payment processing error: {str(e)}")
        flash('An error occurred while processing payment. Please try again.', 'danger')
        return redirect(url_for('payment', flight_id=flight_id))

@app.route('/confirmation')
@login_required
def confirmation():
    booking_reference = request.args.get('booking_reference', f"SW{random.randint(100000, 999999)}")
    
    # Updated flight data with all required attributes
    flight = {
        'id': random.randint(1, 100),
        'airline': 'SkyWings Airlines',
        'airline_logo': 'skywings-airlines.png',  # Added this line
        'origin': 'New York',
        'origin_code': 'NYC',
        'destination': 'London',
        'destination_code': 'LON',
        'departure_time': '09:30',
        'arrival_time': '21:15',
        'departure_date': 'December 15, 2023',
        'duration': '7h 45m',
        'price': 399,
        'base_price': 299,
        'taxes': 85,
        'service_fee': 15,
        'flight_class': 'economy',
        'flight_number': 'SW123',
        'stops': 0  # Added this line
    }
    
    # Mock travelers data
    travelers = [
        {
            'title': 'Mr.',
            'first_name': 'John',
            'last_name': 'Smith',
            'passport_number': '123456789',
            'frequent_flyer_number': 'SW123456',
            'seat': '15A'
        },
        {
            'title': 'Mrs.',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'passport_number': '987654321',
            'frequent_flyer_number': None,
            'seat': '15B'
        }
    ]
    
    payment_method = "Visa ending in 1234"
    billing_address = "123 Main St, New York, NY 10001, USA"
    
    return render_template('confirmation.html',
                        flight=flight,
                        travelers=travelers,
                        booking_reference=booking_reference,
                        email=current_user.email,
                        payment_method=payment_method,
                        billing_address=billing_address)
@app.route('/my-trips')
@login_required
def my_trips():
    # In a real app, this would come from the database
    upcoming_trips = [
        {
            'id': 1,
            'origin': 'New York',
            'destination': 'London',
            'origin_code': 'NYC',
            'destination_code': 'LON',
            'departure_time': '09:30',
            'arrival_time': '21:15',
            'departure_date': 'December 15, 2023',
            'duration': '7h 45m',
            'airline': 'SkyWings Airlines',
            'flight_number': 'SW123',
            'booking_reference': 'SW123456',
            'travelers': ['John Smith', 'Jane Smith'],
            'status': 'confirmed',
            'status_color': 'success'
        },
        {
            'id': 2,
            'origin': 'Paris',
            'destination': 'Tokyo',
            'origin_code': 'PAR',
            'destination_code': 'TYO',
            'departure_time': '14:20',
            'arrival_time': '08:30',
            'departure_date': 'March 5, 2024',
            'duration': '12h 10m',
            'airline': 'Global Airways',
            'flight_number': 'GA456',
            'booking_reference': 'GA789012',
            'travelers': ['John Smith'],
            'status': 'confirmed',
            'status_color': 'success'
        }
    ]
    
    return render_template('my-trips.html', upcoming_trips=upcoming_trips)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my_trips'))
        
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            
            user = User.query.filter_by(email=email).first()
            
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=remember)
                # Get the next page from args or default to my_trips
                next_page = request.args.get('next')
                flash('Successfully logged in!', 'success')
                return redirect(next_page or url_for('my_trips'))
            else:
                flash('Invalid email or password.', 'danger')
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                email=form.email.data,
                name=f"{form.first_name.data} {form.last_name.data}",
                password=password_hash,
                phone=form.phone.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful!', 'success')
            return redirect(url_for('my_trips'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            app.logger.error(f"Registration error: {str(e)}")
            
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # In a real app, you would send a password reset email here
            flash('If an account exists with this email, we have sent a password reset link', 'info')
        return redirect(url_for('login'))
    return render_template('auth/forgot_password.html')
@app.route('/trip/<int:trip_id>')
def trip_details(trip_id):
    # Your view logic here
    return render_template('my-trips.html', trip_id=trip_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)