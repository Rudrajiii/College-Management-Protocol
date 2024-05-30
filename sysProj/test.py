import pymongo
from admin_info import *
from student_info import students
from teacher_info import *
import os
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

def update_teacher_info():
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']
    collection = db['teachers']


    teacher_cursor = collection.find()

    for creator, url in zip(teacher_cursor, a):
        collection.update_one(
            {'_id': creator['_id']},
            {'$set': {'teaches_total_students': url}}
        )

    print('Profile pictures updated successfully.')


def delete_teacher_info():
    client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
    db = client['project']
    collection = db['teachers']

    # Define the field you want to delete
    field_to_delete = 'profilepic'

    # Update all documents to remove the specified field
    result = collection.update_many({}, {'$unset': {field_to_delete: ""}})

    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")




#! Don't Run this Functions
# update_admin_info() 
# add_admin_function()
# update_teacher_info()
# add_student_function(students)
# delete_info_func()
# delete_teacher_info()