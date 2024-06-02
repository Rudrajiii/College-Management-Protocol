import pymongo
from admin_info import *
from student_info import students
def add_admin_function():
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        db = client['project']
        collection = db['creators']
        all_admins = [
            person1,
            person2,
            person3
        ]
        result = collection.insert_many(all_admins)
        print(result)
    except Exception as e:
        print(e)


def add_student_function(students):
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        db = client['project']
        collection = db['students']
        result = collection.insert_many(students)
        print(result)
    except Exception as e:
        print(e)


#!Dangerous Function
def delete_info_func():
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']
    collection = db['creators']

    # Delete all documents from the collection
    result = collection.delete_many({})

    # Print the number of deleted documents
    print("Number of documents deleted:", result.deleted_count)

def update_admin_info():
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']
    collection = db['creators']


    admin_cursor = collection.find()

    for creator, url in zip(admin_cursor, admin_image_source):
        collection.update_one(
            {'_id': creator['_id']},
            {'$set': {'profilepic': url}}
        )

    print('Profile pictures updated successfully.')

#! Don't Run this Functions
# update_admin_info() 
add_admin_function()
# add_student_function(students)
# delete_info_func()
