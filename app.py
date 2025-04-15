
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
        
        cursor.execute("""
            SELECT * FROM donors
            WHERE name = %s AND contact = %s AND blood_group = %s
        """, (name, contact, blood_group))
        existing_donor = cursor.fetchone()

        if existing_donor:
            flash("Donor with this name, contact, and blood group already exists.", "error")
            return redirect('/add-donor')
            
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


@app.route('/view-donors')
def view_donors():
    if 'user' not in session:
        return redirect('/')
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    return render_template("view_donors.html", donors=donors)




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
          
            if any(unit > 1 for unit in [whole, rbc, platelet]):
                flash("Only 1 unit can be donated at a time for Whole Blood, RBC, or Platelets.", "error")
                return redirect('/record-donation')

           
            if (whole > 0 and (rbc > 0 or platelet > 0)):
                flash("You can donate either Whole Blood OR RBC/Platelets, not both at the same time.", "error")
                return redirect('/record-donation')

            
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

            
            cursor.execute("SELECT blood_group FROM donors WHERE donor_id = %s", (donor_id,))
            result = cursor.fetchone()

            if not result:
                flash("No blood group found for the given donor.", "error")
                return redirect('/record-donation')

            blood_group = result['blood_group']

           
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

  
    cursor.execute("SELECT donor_id, name FROM donors")
    donors = cursor.fetchall()

    return render_template("record_donation.html", donors=donors)


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

    cursor.execute("SELECT * FROM inventory")
    inventory_details = cursor.fetchall()

    return render_template('view_inventory.html', inventory=inventory_details)
    
@app.route('/delete-donor/<int:donor_id>', methods=['POST'])
def delete_donor(donor_id):
    if 'user' not in session:
        return redirect('/')
     
    if session['user']['role'] != 'Admin':
        flash("Access denied. Only admins can delete donors.", "error")
        return redirect('/home')

    try:
        cursor.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
        db.commit()
        flash("Donor and associated donations deleted successfully!", "success")
    except Exception as e:
        print(e)
        db.rollback()
        flash("Failed to delete donor.", "error")

    return redirect('/view-donors') 

@app.route('/view-requests', methods=['GET', 'POST'])
def view_requests():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        request_id = request.form['request_id']
        action = request.form['action']

        try:
            if session['user']['role'] != 'Admin':
                flash("Access denied. Only admins can approve or reject requests.", "error")
                return redirect('/home')
            if action == 'approve':
              
                cursor.execute("SELECT * FROM blood_requests WHERE request_id = %s", (request_id,))
                request_data = cursor.fetchone()

                blood_group = request_data['blood_group']
                required_whole = request_data['whole_blood_units']
                required_rbc = request_data['rbc_units']
                required_plasma = request_data['plasma_units']
                required_platelet = request_data['platelet_units']

               
                cursor.execute("SELECT * FROM inventory WHERE blood_group = %s", (blood_group,))
                inventory = cursor.fetchone()

              
                if (inventory['whole_blood_units'] >= required_whole and
                    inventory['rbc_units'] >= required_rbc and
                    inventory['plasma_units'] >= required_plasma and
                    inventory['platelet_units'] >= required_platelet):

       
                    cursor.execute("UPDATE blood_requests SET status='Approved',action_date=NOW() WHERE request_id=%s", (request_id,))
                    db.commit()
                    flash("Request approved successfully!", "success")
                else:
                    flash("Not enough stock available to approve the request.", "error")

            elif action == 'reject':
                cursor.execute("UPDATE blood_requests SET status='Rejected' WHERE request_id=%s", (request_id,))
                db.commit()
                flash("Request rejected successfully!", "success")

        except Exception as e:
            db.rollback()
            print(e)
            flash("An error occurred while updating the request.", "error")

    cursor.execute("SELECT * FROM blood_requests ORDER BY request_date DESC")
    requests = cursor.fetchall()
    return render_template('view_requests.html', requests=requests)


@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    if 'user' not in session:
        return redirect('/')
    

    if session['user']['role'] != 'Admin':
        flash("Access denied. Only admins can create users.", "error")
        return redirect('/home')

    if request.method == 'POST':
        auth_id = request.form['auth_id']
        name = request.form['name']
        password = request.form['password']
        role = request.form['role']

        try:
          
            cursor.execute("SELECT * FROM users WHERE authentication_id = %s", (auth_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("User with this Authentication ID already exists.", "error")
            else:
                cursor.execute("""
                    INSERT INTO users (authentication_id, name, password, role)
                    VALUES (%s, %s, %s, %s)
                """, (auth_id, name, password, role))
                db.commit()
                flash("User created successfully!", "success")
                return redirect('/home')
        except Exception as e:
            db.rollback()
            print(e)
            flash("Error creating user.", "error")

    return render_template('create_user.html')




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# =================== Run App ======================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

