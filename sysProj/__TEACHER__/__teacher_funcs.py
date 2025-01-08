from flask import session, flash, redirect, url_for
from caching import user_cache
from functions import *
from db_config import *

class TeacherFuncs:
    def __init__(self , cache , db_collection):
        self.cache = cache
        self.db_collection = db_collection
    def login(self, enrollment_no, username, password):
        var1 = teacher_login_db(enrollment_no, username, password)
        if var1:
            session['username'] = username
            session['role'] = 'teacher'
            session['enrollment_no'] = enrollment_no
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid username, enrollment number, or password. Please try again.', 'error')
            return redirect(url_for('teacher_login'))
        
    def get_teacher_dashboard_info(self, enrollment_no):
        # Fetch teacher details from database
        teacher_details = self.db_collection.find_one({'enrollment_no': enrollment_no})
        # teacher_details = collection.find_one({'enrollment_no': enrollment_no})
        
        # Fetch teacher application details
        teacher_application = application.find_one({'enrollment_number': enrollment_no})
        status = teacher_application.get('status', 'None') if teacher_application else 'None'

        # Fetch leave application history
        history_records = list(history_collection.find({"enrollment_number": enrollment_no}).sort("timestamp", -1))

        return teacher_details, status, history_records