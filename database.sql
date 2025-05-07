-- Create database
CREATE DATABASE IF NOT EXISTS flight_booking;
USE flight_booking;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Airlines table
CREATE TABLE IF NOT EXISTS airlines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    code VARCHAR(3) NOT NULL UNIQUE,
    logo VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Airports table
CREATE TABLE IF NOT EXISTS airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    code VARCHAR(3) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Flights table
CREATE TABLE IF NOT EXISTS flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline_id INT NOT NULL,
    flight_number VARCHAR(10) NOT NULL,
    origin_airport_id INT NOT NULL,
    destination_airport_id INT NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    duration_minutes INT NOT NULL,
    economy_price DECIMAL(10, 2) NOT NULL,
    premium_economy_price DECIMAL(10, 2),
    business_price DECIMAL(10, 2),
    first_class_price DECIMAL(10, 2),
    seats_available INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (airline_id) REFERENCES airlines(id),
    FOREIGN KEY (origin_airport_id) REFERENCES airports(id),
    FOREIGN KEY (destination_airport_id) REFERENCES airports(id)
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    booking_reference VARCHAR(20) NOT NULL UNIQUE,
    total_price DECIMAL(10, 2) NOT NULL,
    status ENUM('confirmed', 'cancelled', 'completed') DEFAULT 'confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Booking flights (for round trips)
CREATE TABLE IF NOT EXISTS booking_flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    flight_id INT NOT NULL,
    flight_class ENUM('economy', 'premium', 'business', 'first') NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);

-- Travelers table
CREATE TABLE IF NOT EXISTS travelers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    passport_number VARCHAR(50),
    passport_expiry DATE,
    frequent_flyer_number VARCHAR(50),
    seat_number VARCHAR(10),
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('credit_card', 'paypal', 'bank_transfer') NOT NULL,
    transaction_id VARCHAR(100),
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- Insert sample data
INSERT INTO airlines (name, code) VALUES 
('SkyWings Airlines', 'SW'),
('Global Airways', 'GA'),
('Oceanic Airlines', 'OA'),
('Continental', 'CA');

INSERT INTO airports (name, city, country, code) VALUES
('John F. Kennedy International Airport', 'New York', 'United States', 'JFK'),
('Heathrow Airport', 'London', 'United Kingdom', 'LHR'),
('Charles de Gaulle Airport', 'Paris', 'France', 'CDG'),
('Narita International Airport', 'Tokyo', 'Japan', 'NRT'),
('Sydney Airport', 'Sydney', 'Australia', 'SYD'),
('Dubai International Airport', 'Dubai', 'United Arab Emirates', 'DXB');