'''from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from config import get_connection
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pritha",
    database="blood_bank"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE authentication_id = %s AND password = %s", (user_id, password))
    user = cursor.fetchone()

    if user:
        session['user'] = user
        return redirect(url_for('home'))
    else:
        flash("Invalid login")
        return redirect('/')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('home.html', user=session['user'])


@app.route('/add-donor', methods=['GET', 'POST'])
def add_donor():

    if request.method == 'POST':
        donor_id = request.form.get('donor_id') or None
        name = request.form['name']
        age = request.form['age']
        contact = request.form['contact']
        blood_group = request.form['blood_group']
        last_donation = request.form['last_donation'] or None

        try:
            if donor_id:
                cursor.execute("""
                    INSERT INTO donors (donor_id, name, age, contact, blood_group, last_donation)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (donor_id, name, age, contact, blood_group, last_donation))
            else:
                cursor.execute("""
                    INSERT INTO donors (name, age, contact, blood_group, last_donation)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, age, contact, blood_group, last_donation))

            db.commit()
            flash("Donor added successfully!", "success")
            return redirect('/add-donor')

        except Exception as e:
            print(e)
            db.rollback()
            flash("Error adding donor.", "error")
    cursor.execute("SELECT blood_group FROM inventory")
    blood_groups = [row[0] for row in cursor.fetchall()]
    return render_template("add_donor.html", blood_groups=blood_groups)

if __name__ == '__main__':

    app.run(debug=True)
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime,timedelta

# Flask Setup
app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pritha",
    database="blood_bank"
)
cursor = db.cursor(dictionary=True)

# ======================= Routes ============================

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE authentication_id = %s AND password = %s", (user_id, password))
    user = cursor.fetchone()

    if user:
        session['user'] = user
        return redirect(url_for('home'))
    else:
        flash("Invalid login", "error")
        return redirect('/')


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('home.html', user=session['user'])

# ================== Add Donor =============================

@app.route('/add-donor', methods=['GET', 'POST'])
def add_donor():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact = request.form['contact']
        blood_group = request.form['blood_group']
        last_donation = request.form['last_donation'] or None

        try:
            cursor.execute("""
                    INSERT INTO donors ( name, age, contact, blood_group, last_donation)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, age, contact, blood_group, last_donation))

            db.commit()
            flash("Donor added successfully!", "success")
            return redirect('/home')

        except Exception as e:
            print(e)
            db.rollback()
            flash("Error adding donor.", "error")
            return redirect('/add-donor')

    cursor.execute("SELECT blood_group FROM inventory")
    blood_groups = [row['blood_group'] for row in cursor.fetchall()]
    return render_template("add_donor.html", blood_groups=blood_groups)

# ================= View Donors ============================

@app.route('/view-donors')
def view_donors():
    if 'user' not in session:
        return redirect('/')
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    return render_template("view_donors.html", donors=donors)

# ============== Record Donation ===========================
'''@app.route('/record-donation', methods=['GET', 'POST'])
def record_donation():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        # Process form data
        donation_id = None
        donor_id = request.form['donor_id']
        whole = float(request.form.get('whole_blood_units') or 0)
        rbc = float(request.form.get('rbc_units') or 0)
        plasma = float(request.form.get('plasma_units') or 0)
        platelet = float(request.form.get('platelet_units') or 0)
        print(f"Whole blood: {whole}, RBC: {rbc}, Plasma: {plasma}, Platelet: {platelet}")
        try:
            cursor.execute("""Select blood_group from donors where donor_id=%s""",donor_id)
            blood_group=cursor.fetchone()
            blood_group = blood_group['blood_group']
            cursor.execute("""
                INSERT INTO donation_details (donation_id, donor_id, blood_group, whole_blood_units,
                rbc_units, plasma_units, platelet_units, donation_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """, (donation_id, donor_id, blood_group, whole, rbc, plasma, platelet))
            db.commit()
            flash("Donation recorded!", "success")
            return redirect('/home')

        except Exception as e:
            print(e)
            db.rollback()
            flash("Failed to record donation", "error")

    # Fetch blood groups from the database
    cursor.execute("SELECT DISTINCT blood_group FROM donors")
    blood_groups = [row['blood_group'] for row in cursor.fetchall()]

    return render_template("record_donation.html", blood_groups=blood_groups)'''
'''
@app.route('/record-donation', methods=['GET', 'POST'])
def record_donation():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        # Process form data
        donor_id = request.form['donor_id']
        whole = float(request.form.get('whole_blood_units') or 0)
        rbc = float(request.form.get('rbc_units') or 0)
        plasma = float(request.form.get('plasma_units') or 0)
        platelet = float(request.form.get('platelet_units') or 0)
        print(f"Whole blood: {whole}, RBC: {rbc}, Plasma: {plasma}, Platelet: {platelet}")

        try:
            # Fetch blood group based on donor_id
            cursor.execute("""SELECT blood_group FROM donors WHERE donor_id = %s""", (donor_id,))
            blood_group = cursor.fetchone()

            # If no blood group found, handle the error (optional)
            if blood_group is None:
                flash("No blood group found for the given donor.", "error")
                return redirect('/record-donation')

            blood_group = blood_group['blood_group']

            # Insert donation details into the database
            cursor.execute("""
                INSERT INTO donation_details (donor_id, blood_group, whole_blood_units,
                rbc_units, plasma_units, platelet_units, donation_date)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (donor_id, blood_group, whole, rbc, plasma, platelet))

            db.commit()
            flash("Donation recorded!", "success")
            return redirect('/home')

        except Exception as e:
            print(e)
            db.rollback()
            flash("Failed to record donation", "error")

    # Fetch blood groups from the database for the form dropdown
    cursor.execute("SELECT DISTINCT blood_group FROM donors")
    blood_groups = [row['blood_group'] for row in cursor.fetchall()]
    cursor.execute("Select donor_id, name from donors")
    donors=cursor.fetchall()

    return render_template("record_donation.html",donors=donors)
'''


@app.route('/record-donation', methods=['GET', 'POST'])
def record_donation():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        donor_id = request.form['donor_id']
        whole = float(request.form.get('whole_blood_units') or 0)
        rbc = float(request.form.get('rbc_units') or 0)
        plasma = float(request.form.get('plasma_units') or 0)
        platelet = float(request.form.get('platelet_units') or 0)

        print(f"Whole blood: {whole}, RBC: {rbc}, Plasma: {plasma}, Platelet: {platelet}")

        try:
            # Ensure only 1 unit is entered per component
            if any(unit > 1 for unit in [whole, rbc, platelet]):
                flash("Only 1 unit can be donated at a time for Whole Blood, RBC, or Platelets.", "error")
                return redirect('/record-donation')

            # Ensure only one donation type is chosen at a time
            if (whole > 0 and (rbc > 0 or platelet > 0)):
                flash("You can donate either Whole Blood OR RBC/Platelets, not both at the same time.", "error")
                return redirect('/record-donation')

            # Get last donation date
            cursor.execute("""
                SELECT donation_date, whole_blood_units, rbc_units, platelet_units
                FROM donation_details
                WHERE donor_id = %s
                ORDER BY donation_date DESC
                LIMIT 1
            """, (donor_id,))
            last_donation = cursor.fetchone()

            today = datetime.today()

            if last_donation:
                last_date = last_donation['donation_date']

                if whole > 0 and last_donation['whole_blood_units'] > 0:
                    if today - last_date < timedelta(days=90):
                        flash("Whole blood donations must be at least 3 months apart.", "error")
                        return redirect('/record-donation')

                if rbc > 0 and last_donation['rbc_units'] > 0:
                    if today - last_date < timedelta(days=90):
                        flash("RBC donations must be at least 3 months apart.", "error")
                        return redirect('/record-donation')

                if platelet > 0 and last_donation['platelet_units'] > 0:
                    if today - last_date < timedelta(days=7):
                        flash("Platelet donations must be at least 7 days apart.", "error")
                        return redirect('/record-donation')

            # Fetch blood group
            cursor.execute("SELECT blood_group FROM donors WHERE donor_id = %s", (donor_id,))
            result = cursor.fetchone()

            if not result:
                flash("No blood group found for the given donor.", "error")
                return redirect('/record-donation')

            blood_group = result['blood_group']

            # Insert donation record
            cursor.execute("""
                INSERT INTO donation_details (donor_id, blood_group, whole_blood_units,
                rbc_units, plasma_units, platelet_units, donation_date)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (donor_id, blood_group, whole, rbc, plasma, platelet))

            db.commit()
            flash("Donation recorded successfully!", "success")
            return redirect('/home')

        except Exception as e:
            print("Error:", e)
            db.rollback()
            flash("Failed to record donation.", "error")

    # Fetch donors for form
    cursor.execute("SELECT donor_id, name FROM donors")
    donors = cursor.fetchall()

    return render_template("record_donation.html", donors=donors)


# ================= Blood Requests =========================
@app.route('/blood-requests', methods=['GET', 'POST'])
def blood_requests():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        request_by = request.form['request_by']
        blood_group = request.form['blood_group']
        whole = float(request.form.get('whole_blood') or 0)
        rbc = float(request.form.get('rbc_units') or 0)
        plasma = float(request.form.get('plasma_units') or 0)
        platelet = float(request.form.get('platelet_units') or 0)

        try:
            cursor.execute("""
                INSERT INTO blood_requests (request_by, blood_group,
                whole_blood_units, rbc_units, plasma_units, platelet_units, status, request_date)
                VALUES (%s, %s, %s, %s, %s, %s, 'Pending', NOW())
            """, (request_by, blood_group, whole, rbc, plasma, platelet))
            db.commit()
            flash("Request submitted!", "success")
            return redirect('/home')

        except Exception as e:
            print(e)
            db.rollback()
            flash("Error submitting request", "error")

    cursor.execute("SELECT DISTINCT blood_group FROM donors")
    blood_groups = [row['blood_group'] for row in cursor.fetchall()]
    return render_template("requests.html",  blood_groups=blood_groups)

@app.route('/view-donations')
def view_donations():
    if 'user' not in session:
        return redirect('/')

    # Fetch donation details from database
    cursor.execute("""
        SELECT d.donor_id, d.name, dd.donation_id, dd.donation_date, 
               dd.whole_blood_units, dd.rbc_units, dd.plasma_units, dd.platelet_units
        FROM donors d
        JOIN donation_details dd ON d.donor_id = dd.donor_id
    """)
    donation_details = cursor.fetchall()

    return render_template('view_donations.html', donations=donation_details)

@app.route('/view-inventory')
def view_inventory():
    if 'user' not in session:
        return redirect('/')

    # Fetch inventory details from the database
    cursor.execute("SELECT * FROM inventory")
    inventory_details = cursor.fetchall()

    return render_template('view_inventory.html', inventory=inventory_details)
    
@app.route('/delete-donor/<int:donor_id>', methods=['POST'])
def delete_donor(donor_id):
    if 'user' not in session:
        return redirect('/')

    try:
        cursor.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
        db.commit()
        flash("Donor and associated donations deleted successfully!", "success")
    except Exception as e:
        print(e)
        db.rollback()
        flash("Failed to delete donor.", "error")

    return redirect('/view-donors')  # or wherever your donor list is

@app.route('/view-requests', methods=['GET', 'POST'])
def view_requests():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        request_id = request.form['request_id']
        action = request.form['action']

        try:
            if action == 'approve':
                cursor.execute("UPDATE blood_requests SET status='Approved' WHERE request_id=%s", (request_id,))
            elif action == 'reject':
                cursor.execute("UPDATE blood_requests SET status='Rejected' WHERE request_id=%s", (request_id,))
            db.commit()
            flash(f"Request {action}d successfully!", "success")
        except Exception as e:
            db.rollback()
            print(e)
            flash("An error occurred while updating the request.", "error")

    cursor.execute("SELECT * FROM blood_requests ORDER BY request_date DESC")
    requests = cursor.fetchall()
    return render_template('view_requests.html', requests=requests)

# ================= Logout =========================

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# =================== Run App ======================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

