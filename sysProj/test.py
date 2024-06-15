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


def add_student_function():
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        db = client['project']
        collection = db['students']
        # Validation rules for students collection
        # Validation rules for students collection
        # Drop the unique index on password if it exists
        existing_indexes = collection.index_information()
        if 'password_1' in existing_indexes:
            collection.drop_index('password_1')
            print("Dropped unique index on password.")
        student_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["enrollment_no", "username", "password", "phone_no", "email", "branch", "academic_year", "gender", "dob", "parent_name", "parent_no", "current_address", "profile_pic"],
                "properties": {
                    "_id": {},
                    "enrollment_no": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "username": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "password": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "phone_no": {
                        "bsonType": "string",
                        "pattern": "^[0-9]{10}$",
                        "description": "must be a string of 10 digits and is required"
                    },
                    "email": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "branch": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "academic_year": {
                        "bsonType": "int",
                        "minimum": 1,
                        "maximum": 4,
                        "description": "must be an integer and is required"
                    },
                    "gender": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "dob": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "parent_name": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "parent_no": {
                        "bsonType": "string",
                        "pattern": "^[0-9]{10}$",
                        "description": "must be a string of 10 digits and is required"
                    },
                    "current_address": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "profile_pic": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    }
                },
                "additionalProperties": False  # Set to False to disallow any other fields
            }
        }
         # Apply the schema validation to the existing collection
        db.command({
            "collMod": "students",
            "validator": student_validator,
            "validationLevel": "strict"
        })
        
        # Create a unique index on enrollment_no
        db.students.create_index("enrollment_no", unique=True)
        # db.students.create_index("password", unique=False)
        
        print("Schema validation applied to the students collection.")
    
        # result = collection.insert_many(students)
        # print(result)
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


def add_student_db_test(enrollment_no, username, password, email, branch, year, gender, phone, dob, parent_name, parent_no, address, profile_pic_location):
    try:
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        db = client['project']
        collection = db.students
        
        student_info = {
            "enrollment_no": enrollment_no,
            "username": username,
            "password": password,
            "email": email,
            "branch": branch,
            "academic_year": int(year),
            "gender": gender,
            "phone_no": phone,
            "dob": dob,
            "parent_name": parent_name,
            "parent_no": parent_no,
            "current_address": address,
            "profile_pic": profile_pic_location
        }

        collection.insert_one(student_info)
        return 1
    except pymongo.errors.DuplicateKeyError as e:
        print("Error: Duplicate key error - enrollment number or password must be unique.")
        return 0
    except pymongo.errors.WriteError as we:
        print(f"Write Error: {we}")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0

# Example usage
# result = add_student_db_test(
#     "55509", "lol", "lol", "john@example.com", 
#     "CS", "2", "Male", "1230000000", "2000-01-01", 
#     "John Doe Sr.", "0987654321", "123 Main St", "/path/to/profile_pic"
# )
# print("Insertion result:", result)

class TeacherApplication:
    def __init__(self, enrollment_number, name, reason, start_time,end_time, status, response):
        self.enrollment_number = enrollment_number
        self.name = name
        self.reason = reason
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.response = response

def create_teacherApplication_collections(application):
    try:
        # Connect to MongoDB (replace with your MongoDB connection string)
        client = pymongo.MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
        
        # Access or create the database
        db = client['project']
        
        # Access or create the collection 'teacherApplications'
        collection = db['teacherApplications']
        
        # Create a document from the application object
        document = {
            "enrollment_number": application.enrollment_number,
            "name": application.name,
            "reason": application.reason,
            "start_time": application.start_time,
            "end_time": application.end_time,
            "status": application.status,
            "response": application.response
        }
        
        # Insert the document into the collection
        collection.insert_one(document)
        
        print("New Teacher application record created successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the MongoDB connection (optional, but recommended)
        client.close()

# Example usage
if __name__ == "__main__":
    # Create an instance of TeacherApplication
    application1 = TeacherApplication(enrollment_number="ENR2024002", name="alice_smith", reason="__", start_time="2024-06-13T17:31",end_time="2024-06-27T17:31", status="pending", response="accepted")
    #! Don't Run this Functions
    # create_teacherApplication_collections(application1)
    # update_admin_info() 
    # add_admin_function()
    # update_teacher_info()
    # add_student_function()
    # delete_info_func()
    # delete_teacher_info()