Blood Bank Management System

A simple web-based Blood Bank Management System built with Flask and MySQL.

🔍 Overview
This project helps manage blood donors, blood inventory, and blood requests in an organised way. It includes features for:
Adding and viewing donors
Recording blood donations
Managing and approving blood requests
Tracking available blood inventory

💻 Tech Stack
Python (Flask)
MySQL
HTML/CSS (for frontend)

📂 Features
Donor registration
Blood inventory tracking
Request approval/rejection by admin
Dashboard for easy navigation

🗃️ Database
MySQL is used to store donor info, blood donation records, blood requests, and inventory data. Triggers are used to auto-update inventory when a request is approved.

⚙️ How to Run
Clone the repository

Install dependencies:
pip install -r requirements.txt

Set up your MySQL database and update the DB credentials in the code

Run the Flask app:
python app.py
Open your browser and go to http://localhost:5000

📎 Note
The app runs locally due to hosting limitations. All features are functional and can be demonstrated offline.
