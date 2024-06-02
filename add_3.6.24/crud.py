from flask import render_template , jsonify , abort
from data import get_data , Enrollment_logs
from resizeimage import resizeimage
from pymongo import MongoClient
from flask_caching import Cache
from datetime import  datetime
from flask import request
from PIL import Image
from functions import *
# Temporary function import , later changed by Rudra
from function import add_student_db,remove_student_db
from flask import *
import sqlite3
import random
import time 
import glob
import csv
import os
from bson import ObjectId  # Import ObjectId from bson module


app = Flask(__name__)
csv_file_path = 'data/modified_student_data.csv'
app.config['UPLOAD_DIR'] = 'static/Uploads'
root_dir = 'static/Uploads'
app.secret_key = 'opejfjfjjsjkseiiwiei45884&&&*())*$#@@$'
MONGO_URI = "mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/project"
client = MongoClient(MONGO_URI)
db = client['project']
creators = db.creators

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)


def get_user_from_db(username):
    print("Fetching user from cache or MongoDB if not cached")
    user =  db.creators.find_one({"username": username})
    return user

@cache.memoize(timeout=300)  # Cache this function's result for 5 minutes
def get_user(username):
    return get_user_from_db(username)


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

#?Route fuction of admin login

@app.route('/admin_login', methods = ['POST', 'GET'])
def admin_login():
    print("Admin login function called") 
    if(request.method == 'POST'):
        start_time = time.time()  # Record the start time

        enrollment_no = request.form.get('enrollment')
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if admin's info is in the cache and not expired
        user_profile = cache.get(username)

        if user_profile is None:
            # Fetch admin's info from MongoDB if not found in cache or expired
            user_profile = get_user(username)
            # Cache the admin's info
            cache.set(username, user_profile, timeout=300)
            print(f"Admin's info fetched from MongoDB: {user_profile}")
        else:
            # Debug message: Data fetched from cache
            print(f"Admin's info fetched from cache: {user_profile}")

        var1 =  admin_login_db(enrollment_no,username,password)
        # user_profile = get_user(username)
        # user_profile = test(username)
        if user_profile is None:
                flash('Invalid username. Please try again.', 'error')
                return redirect(url_for('admin_login'))

        # print(test(username))
        print(count_students())
        print(count_teachers())
        check = user_profile['profilepic']
        print("Profile pic value:", check)
        session['username'] = user_profile['username']
        session['password'] = user_profile['password']
        session['enrollment_no'] = user_profile['enrollment_no']
        session['profilepic'] = user_profile['profilepic']
        if check != 'None' :
            session['profilepic'] = user_profile['profilepic']
        else:
            session['profilepic'] = 'https://github.com/Rudrajiii/Recipe-App/blob/main/public/images/uploads/default.jpg?raw=true'


        if var1:
            session['username'] = username
            session['role'] = 'admin'

            loading_time = time.time() - start_time
            delay = max(0, loading_time) 
            print(delay)
            session['delay'] = delay
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username, enrollment number, or password. Please try again.', 'error')
            return redirect(url_for('admin_login'))    #if the username or password does not matches 
        
    return render_template("admin_login.html" , delay=session.get('delay', 0))


@app.route('/view_cache')
def view_cache():
    cached_items = []
    for key in cache.cache._cache.keys():
        value = cache.get(key)
        # Convert ObjectId to string if present
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, ObjectId):
                    value[k] = str(v)
        cached_items.append({
            'key': key,
            'value': value
        })
        print(f"Cache item - Key: {key}, Value: {value}")
    return jsonify(cached_items)

#? Route function of teacher login

@app.route('/teacher_login', methods = ['POST', 'GET'])
def teacher_login():
    if(request.method == 'POST'):
        enrollment_no = request.form.get('enrollment')
        username = request.form.get('username')
        password = request.form.get('password')

        var1 = teacher_login_db(enrollment_no,username,password)

        if var1:
            session['username'] = username
            session['role'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid username, enrollment number, or password. Please try again.', 'error')
            return redirect(url_for('teacher_login'))    #if the username or password does not matches 

    return render_template("teacher_login.html")


#?Route fuction of student login

@app.route('/student_login', methods = ['POST', 'GET'])
def student_login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        enrollment_no = request.form.get('enrollment')

        var1 = student_login_db(enrollment_no,username,password)
        if var1:
            session['username'] = username
            session['role'] = 'student'
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username, enrollment number, or password. Please try again.', 'error')
            return redirect(url_for('student_login'))
    return render_template("student_login.html")

@app.route('/admin_dashboard')
def admin_dashboard():
    admin_profile_image = session['profilepic']

    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    total_student_count = count_students()
    total_teacher_count = count_teachers()
    return render_template('admin_dashboard.html', 
            username=session['username'] ,
            total_student_count=total_student_count,
            total_teacher_count=total_teacher_count,
            admin_profile_image=admin_profile_image
                        )

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'username' not in session or session['role'] != 'teacher':
        return redirect(url_for('teacher_login'))
    return render_template('teacher_dashboard.html', username=session['username'])

@app.route('/student_dashboard')
def student_dashboard():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))
    return render_template('student_dashboard.html', username=session['username'])

@app.route('/admin_profile')
def admin_profile():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    admin_username = session['username']
    admin_password = session['password']
    admin_enrollment = session['enrollment_no']
    admin_profile_image = session['profilepic']
    return render_template('admin_profile.html',
                        admin_username=admin_username,
                        admin_password=admin_password,
                        admin_enrollment=admin_enrollment,
                        admin_profile_image=admin_profile_image
                        )

# Edited start by satyadeep at 3/6/24
# Add student details route

@app.route('/add_student', methods=['POST' , 'GET'])
def add_student():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if(request.method == 'POST'):
        enrollment_no = request.form.get('enrollment')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        branch = request.form.get('branch')
        year = request.form.get('year')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        parent_name = request.form.get('parent_name')
        parent_no = request.form.get('parent_no')
        address = request.form.get('address')
        file = request.files['profile_pic']
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".png" , ".jpg" , ".jpeg"]:
            return f'''<h1>Selected file is not a jpg or png or jpeg file please go back and upload correct file format</h1>''' 
        profile_pic_location = enrollment_no + file_extension
        print(profile_pic_location)
        # Save the uploaded image file to the static folder
        filename = os.path.join(app.config['UPLOAD_DIR'], profile_pic_location)
        file.save(filename)
        x = add_student_db(enrollment_no,username,password,email,branch,year,gender,phone,dob,parent_name,parent_no,address,profile_pic_location)
        if x == 1:
            return f'''<h1>student Record Successfully added!!</h1>'''
        else:
            return f'''<h1>Enrollment No. is already present in database!!</h1>'''
    return render_template('add_student.html')


# Manage Student and Remove student details route

@app.route('/manage_student', methods=['POST' , 'GET'])
def manage_student():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if(request.method == 'POST'):
        enrollment_no = request.form.get('enrollment')
        val = request.form.get('button')
        if val == "remove":
            # y contains 0 if no student found with that no. or if found it contains profile_pic name
            y = remove_student_db(enrollment_no)
            if y == 0:
                return f'''<h1>Student not found to be removed Removed</h1>'''
            else:
                # Specify the path to the image file
                filename = os.path.join(app.config['UPLOAD_DIR'], y)

                # Remove the file
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    return f'''<h1>Image File of student not found</h1>'''
                return f'''<h1>Student removed successfully</h1>'''
        if val == "edit":
            return f'''<h1>Student Succesfully Edited</h1>'''
    return render_template('manage_student.html')

# Edited end by satyadeep at 3/6/24


@app.route('/student_profile')
def student_profile():
    ...


@app.route('/teacher_profile')
def teacher_profile():
    ...


@app.route('/staff_informations')
def staff_informations(): 
    return render_template('manage_teachers.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))


#!No to need to present in this file
#todo Here is a problem have to fix it later!!!
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'password':
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

#!No to need to present in this file
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

#!No to need to present in this file
@app.route("/access_data")
def access_data():
    student_data = read_csv(csv_file_path)
    return jsonify(student_data)

@app.route("/add")
def add():   
    return render_template("add.html")

#!No to need to present in this file
@app.route("/logic")
def log():
    return Enrollment_logs()

#!No to need to present in this file
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
    return render_template("delete_user.html")
    
#!No to need to present in this file
@app.route('/secret')
def secret():
    return get_data()


if __name__ == "__main__":
    app.run(debug = True)
    modified_csv_data()
    test('Rudra')  
