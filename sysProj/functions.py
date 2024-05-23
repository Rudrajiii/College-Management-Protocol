# 17/5/24 edit start by satyadeep

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


# 17/5/24 edit end by satyadeep