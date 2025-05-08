# ✈️ SkyWings Flight Booking System

**SkyWings** is a full-featured, web-based flight booking platform that enables users to search for flights, make reservations, and manage their travel plans. Designed with a clean, responsive UI and robust backend, it's built using **Flask**, **SQLAlchemy**, and **Bootstrap**.

---

## 🔧 Features

- 🔍 **Flight Search**: Search for flights by origin, destination, and travel dates.  
- 🎟️ **Booking System**: Securely book flights with traveler details and payment options.  
- 🔐 **User Authentication**: Register, login, and manage user accounts securely.  
- 🧳 **Trip Management**: View upcoming, completed, or canceled trips in the *My Trips* section.  
- 🛠️ **Admin Panel**: Admins can manage flights, users, and bookings.  
- 📱 **Responsive UI**: Mobile-first design with Bootstrap ensures seamless experience across devices.

---

## 💻 Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF  
- **Frontend**: HTML, CSS (Bootstrap), JavaScript  
- **Database**: SQLite (default), MySQL (optional)  
- **Authentication & Security**: Flask-Login, Flask-Bcrypt

---

## 🚀 Installation Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/skywings.git
   cd skywings
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. **(Optional) Add Sample Data**
   ```bash
   python database.py
   ```

6. **Run the Application**
   ```bash
   flask run
   ```

7. **Access the App**
   Open your browser and go to:  
   `http://127.0.0.1:5000`

---

## 📁 Project Structure

```
flightbooking/
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates
├── app.py                  # Main application entry point
├── models.py               # SQLAlchemy database models
├── forms.py                # WTForms for form handling
├── extensions.py           # Flask extensions (DB, login, etc.)
├── routes.py               # All application routes
├── database.py             # Sample data population script
├── requirements.txt        # List of Python dependencies
└── README.md               # Project documentation
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///flight_booking.db
```

---

## 🖼️ Screenshots

### 🏠 Home Page
![Home Page](static/images/screenshots/home.png)

### 🔍 Flight Search
![Flight Search](static/images/screenshots/search.png)

### ✈️ Booking
![Booking](static/images/screenshots/booking.png)

### 💳 Payment
![Payment](static/images/screenshots/payment.png)

### ✅ Confirmation
![Confirmation](static/images/screenshots/confirmation.png)

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.

---

## 🤝 Contributing

We welcome contributions! Fork the repo, create a branch, and submit a pull request.

---

## 📬 Contact

For questions or support, feel free to contact us at:  
📧 [support@skywings.com](mailto:support@skywings.com)
