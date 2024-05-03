import sqlite3
from flask import *
from flask import  jsonify , abort , request
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'
def requires_admin_auth(func):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == ADMIN_USERNAME and auth.password == ADMIN_PASSWORD):
            return jsonify({'error': 'Unauthorized access'}), 401  # Unauthorized
        return func(*args, **kwargs)
    return wrapper
# @requires_admin_auth
def get_data():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        data = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in rows]
        conn.close()
        return jsonify(data)
    except sqlite3.Error as e:

        return jsonify({'error': str(e)})
    
# @requires_admin_auth
def Enrollment_logs():
    enroll_array = []
    with sqlite3.connect("users.db") as connection:
        cur = connection.cursor()
        cur.execute("SELECT Enrollment_no FROM users;")
        rows = cur.fetchall()
        for row in rows:
            enroll_array.append(row[0])
    return jsonify(enroll_array)

if __name__ == '__main__':
    get_data()