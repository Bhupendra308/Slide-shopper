# Slide Shopper

## Overview
Slide Shopper is a user-friendly web platform designed for seamless booking and purchasing of PowerPoint presentations (PPTs). It provides smooth order management and a hassle-free experience for both users and administrators.

## Features
- **PPT Booking System:** Users can book PowerPoint presentations as per their requirements.
- **SQL Database Integration:** Stores user bookings and order details in a MySQL database.
- **Admin Management:** Admins can manage bookings and contact users for finalizing purchases.
- **Flask Backend:** The project is powered by Flask for backend processing.

## Technologies Used
- **Frontend:** HTML, CSS
- **Backend:** Flask (Python)
- **Database:** MySQL
- **Other Libraries:** Requests, re (regular expressions), MySQL-connector-python

## Installation Guide

1. **Clone the Repository:**
   ```sh
   git clone <repository-url>
   cd slide-shopper
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   - Ensure MySQL is installed and running.
   - Create a database and import necessary tables.

4. **Run the Application:**
   ```sh
   python app.py
   ```

5. **Access the Web App:**
   Open `http://127.0.0.1:5000/` in your browser.

## Usage
- Users can visit the website and book PowerPoint slides.
- Admins will receive the booking details and handle communication manually.
- Once confirmed, the user completes the purchase process.

## Future Enhancements
- **Automated Order Processing:** Implementing automated confirmation and payment integration.
- **User Authentication:** Adding user accounts for better tracking.
- **AI Integration:** Enhancing the system with AI recommendations.

## License
This project is for educational and personal use. Modifications and enhancements are encouraged.

