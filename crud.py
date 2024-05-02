from flask import render_template , jsonify , abort
from data import get_data , Enrollment_logs
from resizeimage import resizeimage
from datetime import  datetime
from flask import request
from PIL import Image
from flask import *
import sqlite3
import random
import glob
import csv
import os
app = Flask(__name__)
csv_file_path = 'data/modified_student_data.csv'
app.config['UPLOAD_DIR'] = 'static/Uploads'
root_dir = 'static/Uploads'

def get_post(id):
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    user = con.execute('SELECT * FROM users WHERE id = ?',(id,)).fetchone()
    con.close()
    if user is None:
        abort(404)
    return user

@app.route("/")
def index():
    return render_template("index.html")

#!Here is a problem have to fix it later!!!
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'password':
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route("/student_dashBoard")
def student():
    student_data = read_csv(csv_file_path)
    return render_template("student_dash_board.html" , data=student_data)

def read_csv(your_csv_file):
    with open(your_csv_file, "r") as csv_reader:
        csv_file = csv.DictReader(csv_reader)
        data = [row for row in csv_file]
    return data
def modified_csv_data():
    # Given departments array
    departments_array = ['CSE', 'CSE(ai)', 'CSE(ai & Ml)', 'ECE', 'EE', 'ME', 'IOT', 'CSBS', 'IT']

    # Read the CSV file and store the data
    data = []
    with open('data/student_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    # print(data)
# Count the number of rows and calculate the desired number of CSE entries
    total_rows = len(data)
    cse_min_count = total_rows * 0.4
    cse_max_count = total_rows * 0.6

    # Initialize counters
    cse_count = 0
    new_data = []

    # Modify department values according to the given array
    for row in data:
        if row['department'] == 'CSE':
            if cse_count < cse_min_count:
                row['department'] = 'CSE'
                cse_count += 1
            elif cse_count >= cse_min_count and cse_count < cse_max_count:
                row['department'] = random.choice(['CSE', 'CSE(ai)', 'CSE(ai & Ml)'])
                cse_count += 1
            else:
                row['department'] = random.choice(departments_array)
        else:
            row['department'] = random.choice(departments_array)
        new_data.append(row)

# Write the modified data to a new CSV file
    with open('data/modified_student_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['Full_name', 'gender', 'department']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_data:
            writer.writerow(row)

@app.route("/access_data")
def access_data():
    student_data = read_csv(csv_file_path)
    return jsonify(student_data)
@app.route("/stuff_dashBoard")
def stuff():
    return "<h1>hello from stuff dashboard</h1>"

@app.route("/add")
def add():   
    return render_template("add.html")

@app.route("/logic")
def log():
    return Enrollment_logs()

@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            gender = request.form["gender"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            Enrollment_no = request.form["Enrollment_no"]
            file = request.files["profile_pic"]
            file.save(os.path.join(app.config['UPLOAD_DIR'],file.filename))
            with sqlite3.connect("users.db") as con:
                cur = con.cursor()   
                cur.execute("INSERT into users(name, email, gender, contact, dob, Enrollment_no, profile_pic) values (?,?,?,?,?,?,?)",(name,email,gender,contact,dob,Enrollment_no,file.filename))
                con.commit()
                msg = "User successfully Added"   
        except:
            con.rollback()
            msg = "We can not add User to the list"
        finally:
            con.close()
            return render_template("success.html",msg = msg)

@app.route("/view")
def view():    
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users")   
    rows = cur.fetchall()
    return render_template("view.html",rows = rows,)

@app.route("/<int:id>/view_user", methods=("GET", "POST"))
def view_user(id):
    row = get_post(id)
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        filename_or = row["profile_pic"]
        packages =  con.execute('Select date(dob) FROM users WHERE id = ?', (id,)).fetchone()
        for dob in packages:
            dob = datetime.strptime(dob, '%Y-%m-%d')
            age = (datetime.today() - dob).days/365
            age = round(age, 1)
    return render_template("view_user.html",row = row, now_date = age,)

@app.route("/<int:id>/resize_user", methods=("GET", "POST"))
def resize_user(id):
    row = get_post(id)
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        filename_or = row["profile_pic"]
        with open('static/Uploads/' + filename_or, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image, [200, 200])
                cover.save('static/Uploads/' + filename_or, image.format)      
    return render_template("index.html")

@app.route("/<int:id>/edit_user", methods=("GET", "POST"))
def edit_user(id):
    user = get_post(id)

    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        gender = request.form["gender"]
        contact = request.form["contact"]
        dob = request.form["dob"]
        Enrollment_no = request.form["Enrollment_no"]
        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            query = '''
                UPDATE users
                SET name = ?, email = ?, gender = ?, contact = ?, dob = ? , Enrollment_no = ? where id = ?
            '''
            cur.execute(query,(name,email,gender,contact,dob,Enrollment_no,id))
            con.commit()
            msg = "Updated Successfully!!"
            return render_template("success.html" , msg = msg)
    return render_template('edit_user.html', user = user)

@app.route('/<int:id>/delete_user', methods=("GET", "POST"))
def delete_user(id):
    user = get_post(id)
    with sqlite3.connect("users.db") as con:
        cur = con.cursor() 
        con.execute('DELETE FROM users WHERE id = ?', (id,))
        con.commit()
        return redirect(url_for('delete_user'))
    
@app.route('/secret')
def secret():
    return get_data()

if __name__ == "__main__":
    app.run(debug = True)
    modified_csv_data()  
