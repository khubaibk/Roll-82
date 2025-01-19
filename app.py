from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('data.db')  # Ensure the same database is used
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            rollno TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/add_entry', methods=['POST'])
def add_entry():
    data = request.get_json()
    name = data['name']
    email = data['email']
    rollno = data['rollno']

    conn = sqlite3.connect('data.db')  # Ensure the same database is used
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO entries (name, email, rollno)
        VALUES (?, ?, ?)
    ''', (name, email, rollno))
    conn.commit()
    conn.close()

    return 'Entry Added', 201

@app.route('/get_entries', methods=['GET'])
def get_entries():
    conn = sqlite3.connect('data.db')  # Ensure the same database is used
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, rollno FROM entries")  # Use 'entries' table
    entries = cursor.fetchall()
    conn.close()
    
    return jsonify([{'name': row[0], 'email': row[1], 'rollno': row[2]} for row in entries])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
