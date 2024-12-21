# __ADMIN__/__admin_funcs.py
import os
from time import time
from flask import url_for
from flask import session
from bson import ObjectId
from caching import user_cache
from functions import *

class AdminFuncs:
    def __init__(self, cache , db_collection):
        self.cache = cache
        self.collection = db_collection

    def get_image_name(self, enrollment_no, extension, updated=False):
        if updated:
            return f'{enrollment_no}(updated){extension}'
        else:
            return f'{enrollment_no}{extension}'

    def get_user_profile(self, username):
        """Fetch the admin's profile, either from cache or MongoDB."""
        user_profile = self.cache.get(username)
        if user_profile is None:
            #* Fetch admin's info from MongoDB if not found in cache or expired
            user_profile = user_cache.get_user(username)
            #* Cache the admin's info
            self.cache.set(username, user_profile, timeout=300)
            print(f"Admin's info fetched from MongoDB: {user_profile}")
        else:
            #* Data fetched from cache
            print(f"Admin's info fetched from cache: {user_profile}")
        return user_profile

    def login_admin(self, username, password, enrollment_no):
        """Handle admin login logic."""
        user_profile = self.get_user_profile(username)
        
        if user_profile is None:
            return None

        #* Check the credentials
        if admin_login_db(enrollment_no, username, password):
            #* Return user profile with additional session data
            return user_profile
        return None

    def set_session_data(self, user_profile):
        """Set the session data for the logged-in admin."""
        session['username'] = user_profile['username']
        session['password'] = user_profile['password']
        session['enrollment_no'] = user_profile['enrollment_no']
        session['profilepic'] = user_profile.get('profilepic', 'https://github.com/Rudrajiii/Recipe-App/blob/main/public/images/uploads/default.jpg?raw=true')
        session['role'] = 'admin'

    def get_loading_time(self, start_time):
        """Calculate the time taken for the login process."""
        loading_time = time() - start_time
        return max(0, loading_time)

    def fetch_dashboard_data(self):
        """Fetch and return dashboard-related data."""
        return count_students(), count_teachers()
    
    def get_teachers_data(self):
        """Fetch and process teacher data."""
        teachers = self.collection.find({})
        teacher_list = []
        for teacher in teachers:
            teacher['_id'] = str(teacher['_id'])  # Convert ObjectId to string
            teacher_list.append(teacher)
        return teacher_list

    def save_profile_pic_of_teachers(self, profile_pic, enrollment_no, upload_folder):
        """Save the uploaded profile picture and return its relative path."""
        if profile_pic:
            extension = os.path.splitext(profile_pic.filename)[1]
            new_image_name = self.get_image_name(enrollment_no, extension)
            profile_pic_path = os.path.join(upload_folder, new_image_name)
            profile_pic.save(profile_pic_path)
            # Create a relative path for use in HTML
            return url_for('static', filename=f'Uploads/teachers/{new_image_name}')
        return None
    
    def create_teacher_record(self, form_data, profile_pic_path):
        """Generate the teacher record from form data and insert it into the database."""
        teacher = {
            "enrollment_no": form_data.get('Enrollment_no'),
            "password": form_data.get('password'),
            "username": form_data.get('name'),
            "email": form_data.get('email'),
            "gender": form_data.get('gender'),
            "phone_no": form_data.get('contact'),
            "dob": form_data.get('dob'),
            "profile_pic": profile_pic_path,
            "current_address": form_data.get('current_address'),
            "teaching_subjects": {"subjects": ["English", "History"]},
            "alloted_sections": {"sections": ["C", "D"]},
            "bio": form_data.get('bio'),
            "description": form_data.get('description'),
            "rating": int(form_data.get('rating')) if form_data.get('rating') else 0,
            "reviews": int(form_data.get('reviews')) if form_data.get('reviews') else 0,
            "teaches_total_students": int(form_data.get('teaches_total_students')) if form_data.get('teaches_total_students') else 0
        }
        res = self.collection.insert_one(teacher)
        return res
    
    def get_teacher_by_id(self, staff_id):
        """Fetch a teacher record by ID."""
        return self.collection.find_one({"_id": ObjectId(staff_id)})

    def update_teacher_record(self, staff_id, staff_data):
        """Update a teacher's record in the database."""
        result = self.collection.update_one({"_id": ObjectId(staff_id)}, {"$set": staff_data})
        return result.matched_count > 0

    def save_updated_profile_picture(self, profile_pic, enrollment_no, upload_folder, current_pic_path):
        """Save a new profile picture and delete the old one if it exists."""
        if profile_pic and profile_pic.filename:
            # Delete the old profile picture
            if current_pic_path:
                old_profile_pic_path = os.path.join(upload_folder, current_pic_path.split('/')[-1])
                if os.path.exists(old_profile_pic_path):
                    os.remove(old_profile_pic_path)

            # Save the new profile picture
            extension = os.path.splitext(profile_pic.filename)[1]
            new_image_name = self.get_image_name(enrollment_no, extension, updated=True)
            profile_pic_path = os.path.join(upload_folder, new_image_name)
            profile_pic.save(profile_pic_path)
            return url_for('static', filename=f'Uploads/teachers/{new_image_name}')
        return current_pic_path

    def add_student(self, form_data, file, upload_folder):
        """Handle adding a new student record."""
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".png", ".jpg", ".jpeg"]:
            return None, "Invalid file format. Only .png, .jpg, and .jpeg are allowed."
        
        profile_pic_location = form_data.get('enrollment') + file_extension
        filename = os.path.join(upload_folder, profile_pic_location)
        file.save(filename)
        
        # Call to the database function to add student
        status = add_student_db(
            form_data.get('enrollment'), form_data.get('username'), form_data.get('password'),
            form_data.get('email'), form_data.get('branch'), form_data.get('year'),
            form_data.get('gender'), form_data.get('phone'), form_data.get('dob'),
            form_data.get('parent_name'), form_data.get('parent_no'), form_data.get('address'),
            profile_pic_location
        )
        
        if status == 1:
            return {"status": "success", "message": "✅ Student record successfully added!"}
        else:
            return {"status": "error", "message": "⚠️ Enrollment No. is already present in the database."}