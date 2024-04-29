from flask import *
from flask import render_template , jsonify
from flask import request
from PIL import Image
from datetime import  datetime
from resizeimage import resizeimage
import glob
import sqlite3
import os
import csv
app = Flask(__name__)
csv_file_path = 'student_data.csv'
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

@app.route("/student_dashBoard")
def student():
    student_data = read_csv(csv_file_path)
    return render_template("student_dash_board.html" , data=student_data)

def read_csv(your_csv_file):
    with open(your_csv_file, "r") as csv_reader:
        csv_file = csv.DictReader(csv_reader)
        data = [row for row in csv_file]
    return data

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
    enroll_array = []
    with sqlite3.connect("users.db") as connection:
        cur = connection.cursor()
        cur.execute("SELECT Enrollment_no FROM users;")
        rows = cur.fetchall()
        for row in rows:
            enroll_array.append(row[0])
    print("Enrollment Numbers:")
    for enrollment_no in enroll_array:
        print(enrollment_no == '12023052020037')
    return "<h1>Enrollment numbers fetched and printed in console.</h1>"

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
    return render_template("index.html");

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
    

if __name__ == "__main__":
    app.run(debug = True)  
