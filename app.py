from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DB_NAME = 'medicine.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            phone TEXT NOT NULL,
            expiry_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = get_db_connection()
    medicines = conn.execute('SELECT * FROM medicines').fetchall()
    conn.close()
    total = len(medicines)
    return render_template('home.html', medicines=medicines, total=total)

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        name = request.form['name'].strip()
        city = request.form['city'].strip()
        phone = request.form['phone'].strip()
        expiry_date = request.form['expiry_date']

        # Basic validation
        if not name or not city or not phone or not expiry_date:
            flash('Please fill all fields.', 'error')
            return redirect(url_for('donate'))

        try:
            exp_date_obj = datetime.strptime(expiry_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('donate'))

        conn = get_db_connection()
        conn.execute('INSERT INTO medicines (name, city, phone, expiry_date) VALUES (?, ?, ?, ?)',
                     (name, city, phone, expiry_date))
        conn.commit()
        conn.close()

        flash('Medicine donated successfully! Thank you 🙏', 'success')
        return redirect(url_for('donate'))
    return render_template('donate.html')

@app.route('/view')
def view():
    conn = get_db_connection()
    medicines = conn.execute('SELECT * FROM medicines').fetchall()
    conn.close()
    total = len(medicines)
    return render_template('view.html', medicines=medicines, total=total)

# API for live search and city filter
@app.route('/api/medicines')
def api_medicines():
    search = request.args.get('search', '').lower()
    city_filter = request.args.get('city', '').lower()

    conn = get_db_connection()
    medicines = conn.execute('SELECT * FROM medicines').fetchall()
    conn.close()

    filtered = []
    for med in medicines:
        if (search in med['name'].lower() or search in med['city'].lower()) and (city_filter == '' or city_filter == med['city'].lower()):
            filtered.append(dict(med))

    return jsonify(filtered)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
