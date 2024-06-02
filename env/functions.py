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
