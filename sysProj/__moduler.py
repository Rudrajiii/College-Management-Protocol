
#? All Required Packages  
from packages import *

#? Local Module's
from db_config import *
from caching import user_cache
from graphical_analysis import *
from support_funcs import *

#? Core Module's
from __ADMIN__ import AdminFuncs
from __TEACHER__ import  TeacherFuncs
from __STUDENT__ import StudentFuncs
from __Utils__ import prepare_staff_data , prepare_student_data , remove_student , updated_image , __remove_teacher

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


#?email sending configuration
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


#? Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)

#* initialization of the AdminFuncs class
admin_funcs = AdminFuncs(cache , collection)
#* initialization of the TeacherFuncs class
teacher_funcs = TeacherFuncs(cache , collection)
#* initialization of the StudentFuncs class
student_funcs = StudentFuncs(cache , students)


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

#? Our Main Entry Gate Way
@app.route("/")
def index():
    return render_template("index.html")

# -------------------------------------------------------
#* Route fuction of admin login
#* all admin route's are listed down here
# -------------------------------------------------------

#? Test Trial For Modular Structure [✅CHECK ROUTE'S]

#? Modular Structure [✅ ROUTE 1 CHECKED]
#? admin login route
@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    print("Admin login function called")
    if request.method == 'POST':
        start_time = time()

        enrollment_no = request.form.get('enrollment')
        username = request.form.get('username')
        password = request.form.get('password')

        #* Use the AdminFuncs class to log the admin in and get the user profile
        user_profile = admin_funcs.login_admin(username, password, enrollment_no)

        if user_profile is None:
            flash('Invalid username, enrollment number, or password. Please try again. __moduler', 'error')
            return redirect(url_for('admin_login'))

        #* Set session data for the logged-in user
        admin_funcs.set_session_data(user_profile)

        #* Fetch dashboard data (e.g., student and teacher count)
        student_count, teacher_count = admin_funcs.fetch_dashboard_data()
        
        #* Calculate loading time
        delay = admin_funcs.get_loading_time(start_time)
        session['delay'] = delay
        
        print(f"Students: {student_count}, Teachers: {teacher_count}")
        
        #* Redirect to admin dashboard after successful login
        return redirect(url_for('admin_dashboard'))
    
    return render_template("admin_login.html", delay=session.get('delay', 0))

#? Modular Structure [✅ ROUTE 2 CHECKED]
#? admin dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session['role'] != 'admin' or 'profilepic' not in session:
        return redirect(url_for('admin_login'))

    #* Fetch dashboard data using AdminFuncs
    student_count, teacher_count = admin_funcs.fetch_dashboard_data()

    #* Retrieve admin profile image from session
    admin_profile_image = session.get('profilepic', 'https://default-profile-image-url')
    
    #* Example count from some application logic (replace as needed)
    count = application.count_documents({})

    print("working...1")
    print(admin_profile_image)
    
    return render_template('admin_dashboard.html', 
            username=session['username'],
            total_student_count=student_count,
            total_teacher_count=teacher_count,
            admin_profile_image=admin_profile_image,
            count=count
    )

#? Modular Structure [✅ ROUTE 3 CHECKED]
#? admin profile route
@app.route('/admin_profile')
def admin_profile():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    #* Get admin session data
    admin_username = session.get('username')
    admin_password = session.get('password')
    admin_enrollment = session.get('enrollment_no')
    admin_profile_image = session.get('profilepic', 'https://default-profile-image-url')

    print("working...2")
    
    return render_template('admin_profile.html',
                        admin_username=admin_username,
                        admin_password=admin_password,
                        admin_enrollment=admin_enrollment,
                        admin_profile_image=admin_profile_image
    )

# --------------------------------------------------
#todo all admin activites
# --------------------------------------------------
#* All Routes for a stuff controlled by the admin
#? Modular Structure [✅ ROUTE 4 CHECKED]
#? Teacher Data Retrival
#! This Route is For Developer's of this software.
@app.route('/teachers_data', methods=['GET'])
def get_creators():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    #* Use the AdminFuncs class to get teacher data
    teacher_list = admin_funcs.get_teachers_data()
    return jsonify(teacher_list)

#? Retreving Teacher information from out DB
#? Modular Structure [✅ ROUTE 5 CHECKED]
@app.route('/staff_informations')
def staff_informations():
    """
    it retrieves the stuff data from teacher
    collection to show their information in this
    route
    """
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    teachers = list(collection.find({})) 
    return render_template('manage_teachers.html' , teachers = teachers)

#? Register a new teacher in the main DB
#? Modular Structure [✅ ROUTE 6 CHECKED]
@app.route('/register_a_staff', methods=['GET', 'POST'])
def register_a_staff():
    """
    Here admin is registering the teachers who has joined
    recently!! all the informations will be stored from there
    to a personal Teacher Information DB
    
    """
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        profile_pic = request.files['profile_pic']
        profile_pic_path = admin_funcs.save_profile_pic_of_teachers(profile_pic, request.form.get('Enrollment_no'), app.config['UPLOAD_FOLDER'])
        admin_funcs.create_teacher_record(request.form, profile_pic_path)
        flash('✅ Teacher records added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('register_a_staff.html')



#? Route function to update the information of registered teacher
#? Modular Structure [✅ ROUTE 7 CHECKED]
@app.route('/update_a_staff', methods=['GET', 'POST'])
def update_a_staff():
    """
    Admin can update an existing teacher's information.
    """
    # Clear previous flash messages
    get_flashed_messages()

    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))

    staff_id = request.args.get('id')
    if not staff_id:
        flash('Staff ID is required.', 'error')
        return redirect(url_for('staff_informations'))

    teacher = admin_funcs.get_teacher_by_id(staff_id)
    if not teacher:
        flash('Staff not found.', 'error')
        return redirect(url_for('staff_informations'))

    if request.method == 'POST':
        form_data = request.form
        profile_pic = request.files['profile_pic']
        #* Save the profile picture and get the updated path
        profile_pic_path = admin_funcs.save_updated_profile_picture(
            profile_pic,
            form_data.get('enrollment_no'),
            app.config['UPLOAD_FOLDER'],
            teacher.get('profile_pic')
        )

        #* Use utility function to prepare the staff data
        staff_data = prepare_staff_data(form_data, profile_pic_path)

        if admin_funcs.update_teacher_record(staff_id, staff_data):
            flash('✅ Staff information updated1 successfully!', 'success')
        else:
            flash('❌ Failed to update staff information.', 'error')

        return redirect(url_for('admin_dashboard'))

    return render_template('update_a_staff.html', staff_id=staff_id, teacher=teacher)


#* All Routes for all student controlled by the admin
#? Route to register a new student in 
#? Modular Structure [✅ ROUTE 8 CHECKED]
@app.route('/add_student', methods=['POST' , 'GET'])
def add_student():
    try:
        if 'username' not in session or session['role'] != 'admin':
            return redirect(url_for('admin_login'))
        
        if request.method == 'POST':
            form_data = prepare_student_data(request.form)
            #* making form data dictionary from the request
            file = request.files['profile_pic']

            #* initing the class
            #* give actual instances for cache and db_collection
            admin_functions = AdminFuncs(cache, collection)  
            
            result = admin_functions.add_student(form_data, file, app.config['UPLOAD_DIR'])
            
            return jsonify(result)

        return render_template('add_student.html')
    except Exception as e:
        print("ERROR : ",e)

#? Route to put all details about students for admins
#? Modular Structure [✅ ROUTE 9 CHECKED]
@app.route('/manage_student', methods=['POST', 'GET'])
def manage_student():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        enrollment_no = request.form.get('enrollment')
        val = request.form.get('button')
        
        if val == "remove":
            remove_student(enrollment_no , app.config['UPLOAD_DIR'])

        if val == "edit":
            y = edit_student_get_db(enrollment_no)
            if y == 0:
                flash('⚠️ Student not found to edit.', 'error')  
            else:
                global student_record
                student_record = y
                return redirect(url_for('edit_student', enrollment=enrollment_no))
            return redirect(url_for('manage_student'))  

    return render_template('manage_student.html')


#? Route to edit any existing informations of a student
#? Modular Structure [✅ ROUTE 10 CHECKED]
@app.route('/edit_student', methods=['POST' , 'GET'])
def edit_student():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if(request.method == 'POST'):
        form_data = prepare_student_data(request.form)
        file = request.files['profile_pic']
        if file.filename == '':
            profile_pic_location = student_record['profile_pic']
            edit_student_update_db(student_record['enrollment_no'],form_data,profile_pic_location)
            flash('✅ Student records successfully edited!' , 'success')                #success on edit student record
            return redirect(url_for('admin_dashboard'))
        else:
            #* Specify the path to the image file
            filename = os.path.join(app.config['UPLOAD_DIR'], student_record['profile_pic'])
            en = student_record['enrollment_no']
            #* Remove the file
            try:
                os.remove(filename)
            except FileNotFoundError:
                flash('⚠️ Image file of student not found.' , 'error')
                return redirect(url_for('admin_dashboard'))
            updated_image(file , filename , form_data , en , app.config['UPLOAD_DIR'])
    return render_template('edit_student.html' , student_record = student_record)


#? All the internal announcements will be endergoes from admin panel
#? Modular Structure [✅ ROUTE 11 CHECKED]
@app.route('/announcement', methods = ['POST', 'GET'])
def announcement():
    """
    if admin wants to notify something either for students
    or stuffs will be operated by this function.
    """
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    if(request.method == 'POST'):
        recipient = request.form.get('recipient')
        message = request.form.get('message')
        set_time = request.form.get('set_time')
        student_year = request.form.get('academic_year[]')  #only if student it enables or for teachers its set to all
        recipient = recipient + " " + student_year
        print(recipient)
        if message == "" or set_time == "" or student_year == "":
            flash('⚠️ input fields are empty.' , 'error')
        else:
            announcement_db(recipient,message,set_time)
            flash('✅ Message recorded successfully!' , 'success')
        return redirect(url_for('admin_dashboard'))
    
# --------------------------------------------------
#* Route function of teacher login
#* all teacher login route is listed down here
# --------------------------------------------------

#? teacher login route
#? Modular Structure [✅ ROUTE 12 CHECKED]
@app.route('/teacher_login', methods = ['POST', 'GET'])
def teacher_login():
    if(request.method == 'POST'):
        enrollment_no = request.form.get('enrollment')
        username = request.form.get('username')
        password = request.form.get('password')
        return teacher_funcs.login(enrollment_no , username , password)    #if the username or password does not matches 
    return render_template("teacher_login.html")

#? teacher dashboard route
#? Modular Structure [✅ ROUTE 13 CHECKED]
@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'username' not in session or session['role'] != 'teacher':
        return redirect(url_for('teacher_login'))
    enrollment_no = session['enrollment_no']

    # Get teacher details, application status, and leave history
    teacher_details, status, history_records = teacher_funcs.get_teacher_dashboard_info(enrollment_no)

    # Pass the data to the template
    return render_template('teacher_dashboard.html', username=session['username'], teacher_details=teacher_details, status=status, history=history_records)

#? Teacher Profile route
#? Modular Structure [✅ ROUTE 14 CHECKED]
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

# -------------------------------------------------------
#* Route fuction of student login
#* All student routes are listed down here 
# -------------------------------------------------------
#? Student login route
#? Modular Structure [✅ ROUTE 15 CHECKED]
@app.route('/student_login', methods = ['POST', 'GET'])
def student_login():
    if request.method == 'POST':
        return student_funcs.login(
            request.form.get('enrollment'),
            request.form.get('username'),
            request.form.get('password')
        )
    return render_template("student_login.html")

#? student dashboard route
#? Modular Structure [✅ ROUTE 16 CHECKED]
@app.route('/student_dashboard')
def student_dashboard():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))

    student_data = student_funcs.get_student_dashboard_data(session['enrollment_no'])

    if not student_data:
        return redirect(url_for('student_login'))

    return render_template('student_dashboard.html', **student_data)

#? student profile route
#! Modular Structure [✅ ROUTE 17 INCOMPLETE]
@app.route('/student_profile')
def student_profile():
    ...


#? Route to check if Teacher exists or not
# todo : It's a route for developers 
@app.route('/get_staff/<staff_id>', methods=['GET'])
def get_staff(staff_id):
    staff = collection.find_one({"_id": ObjectId(staff_id)})
    if staff:
        staff['_id'] = str(staff['_id'])
        return jsonify(staff)
    else:
        return jsonify({"error": "Staff not found"}), 404

#? work as delete data func to remove someone from DB
#? Modular Structure [✅ ROUTE 18 CHECKED]
@app.route('/delete_user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    It ensures that it will also remove the images from
    actual root directory in where they were stored!!
    """
    if 'username' not in session or session['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        user_id = ObjectId(user_id)
    except Exception as e:
        return jsonify({"error": "Invalid user ID"}), 400
    return __remove_teacher(app , collection , user_id)

#? func to logout from respective dashboard's
#? Modular Structure [✅ ROUTE 19 CHECKED]
@app.route('/logout')
def logout():
    """
    internally removes the metadata
    stored in a session stack.
    
    """
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

#? still in development process
#? making api endpoint for all statistical analysis
# todo : temporary route for supplying data in charts
@app.route("/access_data")
def access_data():
    """
    rightnow only making data with
    dummy data set , will be replaced with
    realone soon.
    
    """
    student_data = read_csv(csv_file_path)
    return jsonify(student_data)

#* -----------------------------------------------------------------
# todo Notification Section Where admin will able too see the all.
# todo necessary notifications releated to teacher applications.  
#* -----------------------------------------------------------------

@app.route("/view_all_notifications" , methods=["GET", "POST"])
def view_all_notifications():

    """
    section where we store all the upcoming leave
    applications send by the teachers.Now admin has options
    >>Accept Application
    >>Reject Application
    >>In Each Case Email will be send to the teacher it self
    
    each and every response performed by the admin will be
    stored in the history section also.
    """

    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    teacher_applications = list(application.find({}))
    
    # Calculate the requested gap in days
    fetch_all_history = make_history()
    # print(list(fetch_all_history))
    docs = list(fetch_all_history)
    print(docs)
    # for doc in docs:
    #     print(doc)
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
    return render_template("all_notifications.html" ,teacher_applications = teacher_applications , all_history = docs)

# todo route to remove notification's
@app.route("/delete_notification/<application_id>", methods=["DELETE"])
def delete_notification(application_id):

    """
    after giving the response in that applications
    admin can delete the notification as it already stored
    for history section

    """
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


#? Till done!!
#? Start Now
@app.route("/update_status/<application_id>", methods=["PUT"])
def update_status(application_id):
    """
    when a teacher apply for a leave application
    then the first status that is shown in teacher dashboard is
    "pending".
    but as soon as admin give the response in that 
    application either in form of accept or reject
    status get changed in that way.
    and this route is performing this operation.
    
    """
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    new_status = request.json.get('status')
    
    if new_status not in ['Accepted', 'Rejected']:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    
    application_data = application.find_one({'_id': ObjectId(application_id)})
    if not application_data:
        return jsonify({'success': False, 'error': 'Application not found'}), 404
    
    start_time = application_data.get('start_time', '')
    end_time = application_data.get('end_time', '')
    requested_gap = None
    
    if start_time and end_time:
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            requested_gap = (end_dt - start_dt).days
        except ValueError:
            requested_gap = 'Invalid date format'
    else:
        requested_gap = 'Missing date'
    
    message = application_data.get('reason', 'No message provided')
    today = datetime.today().date()
    formatted_time = today.strftime('%d-%m-%Y')

    history_data = history_collection.find_one({'application_id': ObjectId(application_id)})

    if history_data:
        result = history_collection.update_one(
            {'application_id': ObjectId(application_id)},
            {'$set': {'status': new_status, 'timestamp': formatted_time, 'requested_gap': requested_gap}}
        )
    else:
        history_data = {
            'application_id': ObjectId(application_id),
            'enrollment_number': application_data['enrollment_number'],
            'name': application_data['name'],
            'status': new_status,
            'timestamp': formatted_time,
            'email': application_data['email'],
            'message': message,
            'requested_gap': requested_gap,
            'deleted_at': application_data['deleted_at']
        }
        temporary_application_queue.insert_one(history_data)
        result = history_collection.insert_one(history_data)
    # Call the function to update the temporary queue
    update_temporary_queue()

    result = application.update_one(
        {'_id': ObjectId(application_id)},
        {'$set': {'status': new_status}}
    )

    if result.modified_count == 1:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to update status'}), 500


#* EMAIL FEATURE
@app.route("/send_email/<application_id>", methods=["POST"])
def send_email(application_id):
    """
    made for sending emails to teachers and students

    """

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
    """
    made for the leave application submissions
    for teachers.

    """
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



        # Calculate deleted_at timestamp
        dt = datetime.strptime(data['end_time'], "%Y-%m-%dT%H:%M")
        deleted_at = dt.replace(tzinfo=timezone.utc)
        

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
            'email': data['email'],
            'deleted_at': deleted_at
        })

        # Emit an alert to all connected clients in the admin_dashboard namespace
        socketio.emit('alert', {'message': f'New application from {session["username"]} ({session["enrollment_no"]})'}, namespace='/admin_dashboard')


        return jsonify({'message': 'Application submitted successfully'}), 200

    except Exception as e:
        print(e)
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