from models import db, User, Airline, Airport, Flight
from extensions import bcrypt

def create_sample_data():
    # Create admin user
    hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
    admin = User(username='admin', email='admin@skywings.com', 
                password=hashed_password, is_admin=True)
    db.session.add(admin)
    
    # Create airlines
    airlines = [
        Airline(name='SkyWings Airlines', code='SW'),
        Airline(name='Global Airways', code='GA')
    ]
    db.session.add_all(airlines)
    
    # Create airports
    airports = [
        Airport(name='JFK Airport', city='New York', country='USA', code='JFK'),
        Airport(name='Heathrow', city='London', country='UK', code='LHR')
    ]
    db.session.add_all(airports)
    
    db.session.commit()
    
    # Create flights
    flights = [
        Flight(
            airline_id=1,
            flight_number='SW123',
            origin_airport_id=1,
            destination_airport_id=2,
            departure_time='2023-12-15 08:00:00',
            arrival_time='2023-12-15 16:00:00',
            duration_minutes=480,
            economy_price=399.99,
            seats_available=150
        )
    ]
    db.session.add_all(flights)
    db.session.commit()