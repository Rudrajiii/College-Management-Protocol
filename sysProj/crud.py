from flask import render_template , jsonify , abort
from data import get_data , Enrollment_logs
from resizeimage import resizeimage  # type: ignore
from pymongo import MongoClient
from flask_caching import Cache # type: ignore
from datetime import  datetime
from flask import request
from PIL import Image
from functions import *
from flask_cors import CORS # type: ignore
from flask import *
import sqlite3
import random
import time 
import glob
from datetime import datetime 
import timeago # type: ignore
from time import time
import csv
import os
import re
from bson import ObjectId
from flask_mail import Mail ,  Message # type: ignore
import smtplib
from flask_socketio import SocketIO, emit , send , Namespace #type: ignore

class DataStore():
    a = None
    b = None
    c = None

data = DataStore()


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app , cors_allowed_origins="*")
csv_file_path = 'data/modified_student_data.csv'
app.config['UPLOAD_DIR'] = 'static/Uploads'
root_dir = 'static/Uploads'
app.secret_key = 'opejfjfjjsjkseiiwiei45884&&&*())*$#@@$'
MONGO_URI = "mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/project"
client = MongoClient(MONGO_URI)
db = client['project']
creators = db.creators
collection = db['teachers']
students = db['students']
application = db['teacherApplications']
history_collection = db['history']

#email sending configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  #smtp.gmail.com
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'university0690@gmail.com'
app.config['MAIL_PASSWORD'] = 'APNI_PASSWORD_DAL_LE_CHOMU'

mail = Mail(app)

UPLOAD_FOLDER = 'static/Uploads/teachers'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)


def get_image_name(enrollment_no, extension, updated=False):
    if updated:
        return f'{enrollment_no}(updated){extension}'
    else:
        return f'{enrollment_no}{extension}'

@app.route('/teachers_data', methods=['GET'])
def get_creators():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    teachers = collection.find({}) 
    teacher_list = []
    for teacher in teachers:
        teacher['_id'] = str(teacher['_id'])  #string pr convert kr raha
        teacher_list.append(teacher)
    return jsonify(teacher_list)



def get_user_from_db(username):
    print("Fetching user from cache or MongoDB if not cached")
    user =  db.creators.find_one({"username": username})
    return user

@cache.memoize(timeout=300)  # Caching this function's result for 5 minutes
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
        start_time = time()  # Record the start time

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

            loading_time = time() - start_time
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
            session['enrollment_no'] = enrollment_no
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
            session['enrollment_no'] = enrollment_no
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username, enrollment number, or password. Please try again.', 'error')
            return redirect(url_for('student_login'))
    return render_template("student_login.html")

@app.route('/admin_dashboard')
def admin_dashboard():

    if 'username' not in session or session['role'] != 'admin' or 'profilepic' not in session:
        return redirect(url_for('admin_login'))
    total_student_count = count_students()
    total_teacher_count = count_teachers()
    admin_profile_image = session['profilepic']
    application = db['teacherApplications']
    count = application.count_documents({})
    print(admin_profile_image)
    return render_template('admin_dashboard.html', 
            username=session['username'] ,
            total_student_count=total_student_count,
            total_teacher_count=total_teacher_count,
            admin_profile_image=admin_profile_image,
            count=count
                        )

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'username' not in session or session['role'] != 'teacher':
        return redirect(url_for('teacher_login'))
    enrollment_no = session['enrollment_no']
    teacher_details = collection.find_one({'enrollment_no':enrollment_no})
    # print(teacher_details) #? -> Teacher Details
    teacher_application = application.find_one({'enrollment_number': session['enrollment_no']})
    if teacher_application:
        status = teacher_application.get('status', 'None')
    else:
        status = 'None'  # Default if no application found
    
     # Fetch leave application history
    history_records = list(history_collection.find({"enrollment_number": enrollment_no}).sort("timestamp", -1))

    return render_template('teacher_dashboard.html', username=session['username'] , teacher_details=teacher_details , status=status , history=history_records)

@app.route('/student_dashboard')
def student_dashboard():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))
    student_enrollment = session['enrollment_no']
    print("ENROLLMENT_NO "+student_enrollment)
    setudent_details = students.find_one({"enrollment_no":student_enrollment})
    print(setudent_details)
    # Getting the data for annoucement for student from database
    announcement = student_announcement_db()
    return render_template('student_dashboard.html', username=session['username'] ,
                            ENROLLMENT_NO=setudent_details['enrollment_no'],
                            PASSWORD = setudent_details['password'],
                            DOB = setudent_details['dob'],
                            CONTACT = setudent_details['phone_no'],
                            BRANCH = setudent_details['branch'],
                            EMAIL_ID = setudent_details['email'],
                            ADDRESS = setudent_details['current_address'],
                            ACADEMIC_YEAR = setudent_details['academic_year'],
                            announcement = announcement)

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


@app.route('/student_profile')
def student_profile():
    ...


@app.route('/teacher_profile/<string:id>', methods=['GET'])
def teacher_profile(id):
    # Ensure the user is an admin
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    try:
        teacher_id = ObjectId(id)
    except Exception as e:
        abort(404, description="Invalid teacher ID")

    # Fetching teacher details using the provided id
    teacher = collection.find_one({"_id": teacher_id})
    if teacher is None:
        abort(404, description="Teacher not found")

    return render_template('teacher_profile.html', teacher=teacher)


@app.route('/staff_informations')
def staff_informations():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    teachers = list(collection.find({})) 
    return render_template('manage_teachers.html' , teachers = teachers)



@app.route('/register_a_staff', methods=['GET', 'POST'])
def register_a_staff():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        contact = request.form.get('contact')
        enrollment_no = request.form.get('Enrollment_no')
        current_address = request.form.get('current_address')
        bio = request.form.get('bio')
        description = request.form.get('description')
        rating = request.form.get('rating')
        reviews = request.form.get('reviews')
        teaches_total_students = request.form.get('teaches_total_students')
        dob = request.form.get('dob')
        profile_pic = request.files['profile_pic']


        profile_pic_path = None
        if profile_pic:
            extension = os.path.splitext(profile_pic.filename)[1]
            new_image_name = get_image_name(enrollment_no, extension)
            profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], new_image_name)
            profile_pic.save(profile_pic_path)
            profile_pic_path = url_for('static', filename=f'Uploads/teachers/{new_image_name}')  # To create a relative path for HTML
    

        teacher = {
            "enrollment_no": enrollment_no,
            "password": password,
            "username": name,
            "email": email,
            "gender": gender,
            "phone_no": contact,
            "dob": dob,
            "profile_pic": profile_pic_path,
            "current_address": current_address,
            "teaching_subjects": {"subjects": ["English", "History"]},
            "alloted_sections": {"sections": ["C", "D"]},  
            "bio": bio,
            "description": description,
            "rating": int(rating) if rating else 0,
            "reviews": int(reviews) if reviews else 0,
            "teaches_total_students": int(teaches_total_students) if teaches_total_students else 0
        }
        res = collection.insert_one(teacher)
        print(res)
        return 'Success'

    return render_template('register_a_staff.html')


@app.route('/update_a_staff', methods=['GET','POST'])
def update_a_staff():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    staff_id = request.args.get('id')
    # print(type(staff_id))
    print(staff_id)
    # teachers = collection.find_one({"_id": ObjectId(staff_id)})
    # print(teachers['profile_pic'])
    # print(type(teachers['profile_pic']))
    if not staff_id:
        flash('Staff ID is required.', 'error')
        return redirect(url_for('staff_informations'))

    teacher = collection.find_one({"_id": ObjectId(staff_id)})
    if not teacher:
        flash('Staff not found.', 'error')
        return redirect(url_for('staff_informations'))

    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        if not staff_id:
            flash('Staff ID not provided.', 'error')
            return redirect(url_for('update_a_staff', id=staff_id))
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        contact = request.form.get('phone_no')
        Enrollment_no = request.form.get('enrollment_no')
        current_address = request.form.get('current_address')
        bio = request.form.get('bio')
        description = request.form.get('description')
        rating = request.form.get('rating')
        reviews = request.form.get('reviews')
        teaches_total_students = request.form.get('teaches_total_students')
        dob = request.form.get('dob')
        profile_pic = request.files['profile_pic']

        # files = os.listdir(app.config['UPLOAD_FOLDER'])

        profile_pic_path = teacher['profile_pic']  # Default to the current profile pic path

        if profile_pic and profile_pic.filename:
            # Delete the old profile picture
            if teacher['profile_pic']:
                old_profile_pic_path = os.path.join(app.root_path, teacher['profile_pic'][1:])  # Remove leading '/' from URL
                if os.path.exists(old_profile_pic_path):
                    os.remove(old_profile_pic_path)

            # Save the new profile picture
            extension = os.path.splitext(profile_pic.filename)[1]
            new_image_name = get_image_name(Enrollment_no, extension, updated=True)
            profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], new_image_name)
            profile_pic.save(profile_pic_path)
            profile_pic_path = url_for('static', filename=f'Uploads/teachers/{new_image_name}')

        staff_data = {
            "username": name,
            "email": email,
            "password": password,
            "gender": gender,
            "phone_no": contact,
            "enrollment_no": Enrollment_no,
            "current_address": current_address,
            "bio": bio,
            "description": description,
            "rating": rating,
            "reviews": reviews,
            "teaches_total_students": teaches_total_students,
            "dob": dob,
            "profile_pic": profile_pic_path
        }

        if staff_id:
            result = collection.update_one(
                {"_id": ObjectId(staff_id)},
                {"$set": staff_data}
            )
            # print(result)
            # print('Updated name: ' + result.username)
            if result.matched_count > 0:
                flash('Staff information updated successfully!', 'success')
            else:
                flash('Staff not found.', 'error')
        else:
            
            flash('Staff ID not provided.', 'error')

        return 'updated'  # Redirect to an appropriate route

    return render_template('update_a_staff.html' , staff_id=staff_id , teacher = teacher)

@app.route('/get_staff/<staff_id>', methods=['GET'])
def get_staff(staff_id):
    staff = collection.find_one({"_id": ObjectId(staff_id)})
    if staff:
        staff['_id'] = str(staff['_id'])
        return jsonify(staff)
    else:
        return jsonify({"error": "Staff not found"}), 404


@app.route('/delete_user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if 'username' not in session or session['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        user_id = ObjectId(user_id)
    except Exception as e:
        return jsonify({"error": "Invalid user ID"}), 400
        # Fetch user details before deleting
    user_details = collection.find_one({"_id": user_id})
    result = collection.delete_one({"_id": user_id})
    print(result)
    # if details['profile_pic']:
    #             user_profile_pic_path = os.path.join(app.root_path, details['profile_pic'][1:])  # Remove leading '/' from URL
    #             if os.path.exists(user_profile_pic_path):
    #                 os.remove(user_profile_pic_path)

    if result.deleted_count == 1:
        # Delete user profile pic if it exists
        if user_details and 'profile_pic' in user_details:
            profile_pic_path = user_details['profile_pic']
            if profile_pic_path:
                full_path = os.path.join(app.root_path, profile_pic_path[1:])  # Remove leading '/' from URL
                if os.path.exists(full_path):
                    os.remove(full_path)
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404



#*inserted code from satyadeep
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
                return f'''<h1>Student not found to be Removed</h1>'''
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
            # y contains 0 if no student found with that enroll no. else it contains the record of student
            y = edit_student_get_db(enrollment_no)
            if y == 0:
                return f'''<h1>Student not found to be edited</h1>'''
            else:
                # student_record variable is considered as global to use it in edit route functions
                global student_record
                student_record = y
                return redirect(url_for('edit_student'))
    return render_template('manage_student.html')

# *Edit student route
# !New Route created bu Satyadeep
@app.route('/edit_student', methods=['POST' , 'GET'])
def edit_student():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if(request.method == 'POST'):
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
        if file.filename == '':
            profile_pic_location = student_record['profile_pic']
            edit_student_update_db(student_record['enrollment_no'],username,password,email,branch,year,gender,phone,dob,parent_name,parent_no,address,profile_pic_location)
            return f'''<h1>Student record Successfully edited</h1>'''
        else:
            # Specify the path to the image file
            filename = os.path.join(app.config['UPLOAD_DIR'], student_record['profile_pic'])

            # Remove the file
            try:
                os.remove(filename)
            except FileNotFoundError:
                return f'''<h1>Image File of student not found</h1>'''
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in [".png" , ".jpg" , ".jpeg"]:
                return f'''<h1>Selected file is not a jpg or png or jpeg file please go back and upload correct file format</h1>''' 
            profile_pic_location = student_record['enrollment_no'] + file_extension
            # Save the uploaded image file to the static folder
            filename = os.path.join(app.config['UPLOAD_DIR'], profile_pic_location)
            file.save(filename)
            edit_student_update_db(student_record['enrollment_no'],username,password,email,branch,year,gender,phone,dob,parent_name,parent_no,address,profile_pic_location)
            return f'''<h1>Student record updated with Updated pic</h1>'''
    return render_template('edit_student.html' , student_record = student_record)

# Edited end by satyadeep at 4/6/24

# Edit start by Satyadeep on 20/6/24

@app.route('/announcement', methods = ['POST', 'GET'])
def announcement():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    if(request.method == 'POST'):
        recipient = request.form.get('recipient')
        message = request.form.get('message')
        announcement_db(recipient,message)
    return f'''<h1>Message recorded sucessfully</h1>'''
    

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

#** Important function for chart data generation

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


@app.route("/view_all_notifications" , methods=["GET", "POST"])
def view_all_notifications():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    teacher_applications = list(application.find({}))
    
    # Calculate the requested gap in days
    for app in teacher_applications:
        start_time = app.get('start_time', '')
        end_time = app.get('end_time', '')
        
        if start_time and end_time:
            try:
                start_dt = datetime.fromisoformat(start_time)
                end_dt = datetime.fromisoformat(end_time)
                app['requested_gap'] = (end_dt - start_dt).days
            except ValueError:
                app['requested_gap'] = 'Invalid date format'
        else:
            app['requested_gap'] = 'Missing date'

    # print(teacher_applications)
    return render_template("all_notifications.html" ,teacher_applications = teacher_applications )


@app.route("/delete_notification/<application_id>", methods=["DELETE"])
def delete_notification(application_id):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    application_data = application.find_one({'_id': ObjectId(application_id)})
    if not application_data:
        return jsonify({'success': False, 'error': 'Application not found'}), 404
    
    result = application.delete_one({'_id': ObjectId(application_id)})
    
    if result.deleted_count == 1:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to delete notification'}), 500

@app.route("/update_status/<application_id>", methods=["PUT"])
def update_status(application_id):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    new_status = request.json.get('status')
    
    if new_status not in ['Accepted', 'Rejected']:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    
    application_data = application.find_one({'_id': ObjectId(application_id)})
    print(application_data)
    if not application_data:
        return jsonify({'success': False, 'error': 'Application not found'}), 404
    
    
    # Check if a history entry already exists for this application
    history_data = history_collection.find_one({'application_id': ObjectId(application_id)});

    # Prepare the message to be saved in history
    message = application_data.get('reason', 'No message provided');

    today = datetime.today().date()
    formatted_time = today.strftime('%d-%m-%Y')

    if history_data:
        # Update existing history entry
        result = history_collection.update_one(
            {'application_id': ObjectId(application_id)},
            {'$set': {'status': new_status, 'timestamp':formatted_time}}
        )
    else:
        # Prepare new history data
        history_data = {
            'application_id': ObjectId(application_id),
            'enrollment_number': application_data['enrollment_number'],
            'name': application_data['name'],
            'status': new_status,  # Save the new status
            'timestamp': formatted_time,
            'email': application_data['email'],
            'message': message
        }
        result = history_collection.insert_one(history_data)

    result = application.update_one(
        {'_id': ObjectId(application_id)},
        {'$set': {'status': new_status}}
    )
    
    if result.modified_count == 1:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to update status'}), 500


#EMAIL FEATURE
@app.route("/send_email/<application_id>", methods=["POST"])
def send_email(application_id):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))

    teacher_application = application.find_one({'_id': ObjectId(application_id)})
    teacher_email = teacher_application.get('email')
    application_status = teacher_application.get('status')

    if not teacher_email:
        return jsonify({'success': False, 'error': 'Email address not found for this application'}), 400

    subject = "Your leave application update"
    body = f"Dear {teacher_application['name']},\n\nThis is a notification regarding your leave application\n\nSo Your application got {application_status}.\n\nBest regards,\nAdmin"
    msg = Message(subject, sender='university0690@gmail.com', recipients=[teacher_email])
    msg.body = body

    try:
        mail.send(msg)
        return jsonify({'success': True}), 200
    except smtplib.SMTPException as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/submit_application' , methods=['POST'])
def submit_application():
    if 'username' not in session or session['role'] != 'teacher':
        return redirect(url_for('teacher_login'))
    try:
        # Check if there is an existing application with status "Pending"
        existing_application = application.find_one({
            'enrollment_number': session['enrollment_no'],
            'status': 'Pending'
        })

        if existing_application:
            return jsonify({'error': 'You already have a pending application'}), 400
        # Get data from request
        data = request.json
        print(data)

        # Insert into MongoDB collection
        application.insert_one({
            'enrollment_number': data['enrollment_number'],
            'name': session['username'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'reason': data['reason'],
            'status': data['status'],
            'response':data['Response'],
            'submitted_at': datetime.now(),
            'email': data['email']
        })

        # Emit an alert to all connected clients in the admin_dashboard namespace
        socketio.emit('alert', {'message': f'New application from {session["username"]} ({session["enrollment_no"]})'}, namespace='/admin_dashboard')


        return jsonify({'message': 'Application submitted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#* Error handling
@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('error_page.html' , error = e), 404

@app.errorhandler(500)
def internal_server_error(e):
    return f"internal_server_error{e}", 500

#* Let's link up the student dashboard with our main gateway.
@app.route("/timetable" , methods = ["GET", "POST"])
def timetable():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))
    return render_template("timetable.html",ENROLLMENT_NO = session['enrollment_no'])


@app.route("/exam" , methods=["GET", "POST"])
def exam():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))
    return render_template("exam.html" , ENROLLMENT_NO = session['enrollment_no'])

@app.route("/update_password/<ENROLLMENT_NO>" , methods=["GET","POST"])
def update_password(ENROLLMENT_NO):
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))
    if request.method == 'POST':
        current_password = request.form.get('currentpass')
        new_password = request.form.get('newpass')
        confirm_password = request.form.get('confirmpass')
        if new_password != confirm_password:
            return f'''<h1>Confirm password and new password does not match</h1>'''
        else:
            x = change_student_pass_db(ENROLLMENT_NO,current_password,confirm_password)
            print(x)
            # If x = 0 , means currentpassword is wrongly put else change password is success
            if x == 0:
                return f'''<h1>Please input correct old password</h1>'''
            else:
                return f'''<h1>Password Successfully changed</h1>'''
    return render_template("password.html" , ENROLLMENT_NO = session['enrollment_no'])


class AdminNamespace(Namespace):
    def on_connect(self):
        print('Admin connected.')

    def on_disconnect(self):
        print('Admin disconnected.')

class TeacherNamespace(Namespace):
    def on_connect(self):
        print('Teacher connected.')

    def on_apply(self, data):
        print('Apply button clicked:', data)
        # Emit an alert to all connected clients in the admin_dashboard namespace
        # socketio.emit('alert', {'message': 'An apply button was clicked!'}, namespace='/admin_dashboard')

    def on_disconnect(self):
        print('Teacher disconnected.')

socketio.on_namespace(AdminNamespace('/admin_dashboard'))
socketio.on_namespace(TeacherNamespace('/teacher_dashboard'))

if __name__ == "__main__":
    socketio.run(app , debug = True)
    modified_csv_data()
    test('Rudra')

