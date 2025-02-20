from datetime import datetime , timedelta
import pymongo


# Admin Login database connection
def admin_login_db(enrollment_no,username,password):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing creators/admins Collection
    collection = db.creators
    admins = collection.find_one({"username": username , "enrollment_no": enrollment_no , "password": password})
    if admins == None:
        return 0
    else:
        return 1
    

# Teacher Login database connection
def teacher_login_db(enrollment_no,username,password):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing creators/admins Collection
    collection = db.teachers
    teachers = collection.find_one({"username": username , "enrollment_no": enrollment_no , "password": password})
    if teachers == None:
        return 0
    else:
        return 1
    
# Student Login database connection
def student_login_db(enrollment_no,username,password):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing creators/admins Collection
    collection = db.students
    students = collection.find_one({"username": username , "enrollment_no": enrollment_no , "password": password})
    if students == None:
        return 0
    else:
        return 1

def test(username):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']  
    users_collection = db['creators']
    admin_details = users_collection.find_one({'username': username})
    return admin_details

def count_students():
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']  
    students_collection = db['students']
    total_student_count = students_collection.count_documents({})
    return total_student_count

def count_teachers():
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']  
    teachers_collection = db['teachers']
    total_teachers_count = teachers_collection.count_documents({})
    return total_teachers_count


# Edited start by satyadeep at 3/6/24

# Add student database connection
def add_student_db(enrollment_no,username,password,email,branch,year,gender,phone,dob,parent_name,parent_no,address,profile_pic_location):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing students Collection
    collection = db.students
    #Checking if enrollment no. is already present in DB
    students = collection.find_one({"enrollment_no": enrollment_no})
    
    if students == None:
        # Adding students record
        student_info = {
            "enrollment_no" : enrollment_no ,
            "password" : password ,
            "username" : username ,
            "email" : email ,
            "branch" : branch ,
            "academic_year" : int(year) ,
            "gender" : gender ,
            "phone_no" : phone ,
            "dob" : dob ,
            "parent_name" : parent_name ,
            "parent_no" : parent_no ,
            "current_address" : address ,
            "profile_pic" : profile_pic_location
        }
        student_id = collection.insert_one(student_info).inserted_id
        return 1
    else:
        return 0


# Remove Student from database connection
def remove_student_db(enrollment_no):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing students Collection
    collection = db.students
    students = collection.find_one({"enrollment_no": enrollment_no})
    if students == None:
        return 0
    else:
        x = students.get('profile_pic')
        r = collection.delete_one({"enrollment_no": enrollment_no})
        return x

# Edited end by satyadeep at 3/6/24

# Edit Student get data from database connection
def edit_student_get_db(enrollment_no):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing students Collection
    collection = db.students
    students = collection.find_one({"enrollment_no": enrollment_no})
    if students == None:
        return 0
    else:
        return students
    
# Edit Student update data from database connection
def edit_student_update_db(enrollment_no,form_data,profile_pic_location):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing students Collection
    collection = db.students
    # Student record in one dictionary
    year = form_data['year']
    student_info = {
        "password" : form_data['password'] ,
        "username" : form_data['username'] ,
        "email" : form_data['email'] ,
        "branch" : form_data['branch'] ,
        "academic_year" : int(year) ,                                                 
        "gender" : form_data['gender'] ,
        "phone_no" : form_data['phone'] ,
        "dob" : form_data['dob'] ,
        "parent_name" : form_data['parent_name'] ,
        "parent_no" : form_data['parent_no'] ,
        "current_address" : form_data['address'] ,
        "profile_pic" : profile_pic_location
        }
    collection.update_one({"enrollment_no": enrollment_no} , {"$set": student_info})


# Change Students password from students dashboard database connection
def change_student_pass_db(ENROLLMENT_NO,current_password,confirm_password):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing students Collection
    collection = db.students
    students = collection.find_one({"enrollment_no": ENROLLMENT_NO})
    if current_password != students['password']:
        return 0
    else:
        collection.update_one({"enrollment_no": ENROLLMENT_NO} , {"$set": {'password': confirm_password}})
        return 1
    
# Edit start by Satyadeep on 20/6/24
# Announcement DB connection through admin dashboard

def announcement_db(recipient,message,set_time):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing notifications Collection
    collection = db.notifications
    # Adding The data for notification database
    current_time = datetime.utcnow()                                             # Using UTC time
    # converting str type of set_time to datetime variable 
    deletion_time = datetime.strptime(set_time, "%Y-%m-%dT%H:%M") - timedelta(hours = 5 , minutes = 30)
    announcement_info ={
            "for": recipient ,
            "message": message,
            "timestamp": current_time,
            "deleteAt": deletion_time          
        }
    collection.insert_one(announcement_info).inserted_id
    collection.create_index(
        [("deleteAt", pymongo.ASCENDING)],
        expireAfterSeconds=0
        )
    
# Announcement DB connection for student dashboard , we are sorting the data for both and students
def student_announcement_db(ACADEMIC_YEAR):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing notifications Collection
    collection = db.notifications
    info_list = []
    current_time = datetime.utcnow()                            # Use UTC time
    info1 = collection.find({"for":"Both all"})                     # For collecting the data of announcement for both(student , teacher)
    for item in info1:                                          
        message = item['message']
        timestamp = item['timestamp']
        time_difference = current_time - timestamp
        days = time_difference.days
        seconds = time_difference.seconds
        hours, remainder = divmod(seconds, 3600)    
        minutes, seconds = divmod(remainder, 60)
        if days != 0:
            time_past = f"{days} days ago"
        elif days == 0 and hours != 0:
            time_past = f"{hours} hours ago"
        elif days == 0 and hours == 0 and minutes != 0:
            time_past = f"{minutes} minutes ago"
        else:
            time_past = f"{seconds} seconds ago"
        temp_lst = [message,time_past]
        info_list.append(temp_lst)
    info2 = collection.find({"for":"Student all"})                     # For collecting the data of announcement foronly all year student
    for item in info2:                                          
        message = item['message']
        timestamp = item['timestamp']
        time_difference = current_time - timestamp
        days = time_difference.days
        seconds = time_difference.seconds
        hours, remainder = divmod(seconds, 3600)    
        minutes, seconds = divmod(remainder, 60)
        if days != 0:
            time_past = f"{days} days ago"
        elif days == 0 and hours != 0:
            time_past = f"{hours} hours ago"
        elif days == 0 and hours == 0 and minutes != 0:
            time_past = f"{minutes} minutes ago"
        else:
            time_past = f"{seconds} seconds ago"
        temp_lst = [message,time_past]
        info_list.append(temp_lst)
    # merging the syntax to retrive only particular year student announcement
    particular_year_info = "Student" + " " + str(ACADEMIC_YEAR)
    info3 = collection.find({"for": particular_year_info})                    # For collecting the data of announcement foronly particular year student
    for item in info3:                                          
        message = item['message']
        timestamp = item['timestamp']
        time_difference = current_time - timestamp
        days = time_difference.days
        seconds = time_difference.seconds
        hours, remainder = divmod(seconds, 3600)    
        minutes, seconds = divmod(remainder, 60)
        if days != 0:
            time_past = f"{days} days ago"
        elif days == 0 and hours != 0:
            time_past = f"{hours} hours ago"
        elif days == 0 and hours == 0 and minutes != 0:
            time_past = f"{minutes} minutes ago"
        else:
            time_past = f"{seconds} seconds ago"
        temp_lst = [message,time_past]
        info_list.append(temp_lst)
    return info_list



# Edit start by Satyadeep on 27/12/24
# Exam_scheduler DB connection through admin dashboard

def exam_scheduler_db(exam_data):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing exam Collection
    collection = db.exam
    # Setting time for deletion of exam table
    exam_table = exam_data.get('schedule')
    last_date = exam_table[-1].get('date')
    # converting str type of last_date to datetime variable 
    deletion_time = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(hours = 24)
    #inserting data to database
    data ={
            "exam_name": exam_data.get('exam_name'),
            "student_year": exam_data.get('student_year'),
            "student_branch": exam_data.get('student_branch'),
            "schedule": exam_data.get('schedule'),
            "deleteAt": deletion_time          
        }
    collection.insert_one(data).inserted_id
    collection.create_index(
        [("deleteAt", pymongo.ASCENDING)],
        expireAfterSeconds=0
        )

# Students dashboard panel exam DB for sorting specific exams
def student_exam_db(student_year , branch):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing exam Collection
    collection = db.exam
    lst = []
    exam_list = collection.find({"student_year":student_year , "student_branch":branch})
    for i in exam_list:
        lst.append(i)
    return lst


def teacher_application_record(enrollment_no , name , reason ,start_time, end_time , status , response):
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        # Acessing project Database
        db = client['project']
        # Acessing students Collection
        application = db.teacherApplications
        record = {
            "enrollment_number": enrollment_no,
            "name":name,
            "reason": reason,
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
            "response": response
        }
        save_record = application.insert_one(record)
        print("Saved record successfully")
    except Exception as e:
        print(e)


##Not useful
def save_history(enrollment_number, name, status, timestamp, email):
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        db = client['project']
        history_collection = db['history']
        history_collection.insert_one({
            "enrollment_number": enrollment_number,
            "name": name,
            "status": status,
            "timestamp": timestamp,
            "email": email
        });
        print("History Saved Successfully!!!");
    except Exception as e:
        print(e)
def make_history():
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        db = client['project']
        history_collection = db['history']
        all_history = history_collection.find()
        return all_history
    except Exception as e:
        print(e)

def get_teacher_image():
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        db = client['project']
        teachers_collection = db['teachers']
        all_info = teachers_collection.find({})
        return all_info
    except Exception as e:
        print(f"error : {e}")

# Function to add leave information to the collection
def add_leave_info(teacher_info):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']
    temporary_application_queue = db['temporary_application_queue']
    temporary_application_queue.insert_one(teacher_info)


def change_teacher_pass_db(ENROLLMENT_NO,current_password,confirm_password):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing students Collection
    collection = db.teachers
    teachers = collection.find_one({"enrollment_no": ENROLLMENT_NO})
    if current_password != teachers['password']:
        return 0
    else:
        collection.update_one({"enrollment_no": ENROLLMENT_NO} , {"$set": {'password': confirm_password}})
        return 1