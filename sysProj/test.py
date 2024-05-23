import pymongo
from admin_data import first_admin
def add_admin_function():
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']
    collection = db['creators']
    result = collection.insert_one(first_admin)
    return result

def admin_login_db(enrollment_no,username,password):
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    # Acessing project Database
    db = client['project']
    # Acessing creators/admins Collection
    collection = db.creators
    admins = collection.find_one({"username": username , "enrollment_no": enrollment_no , "password": password})
    print(admins)
    if admins == None:
        return 0
    else:
        return 1
admin_login_db('xxxx' , "Rudra" , '1234')
# add_admin_function()




