from __STUDENT__.__data_util import format_student_dashboard_data
from flask import session, flash, redirect, url_for
from caching import user_cache
from functions import *
from db_config import *
from support_funcs import *


class StudentFuncs:
    def __init__(self , cache , db_collection):
        self.cache = cache
        self.db_collection = db_collection

    def login(self, enrollment_no, username, password):
        var1 = student_login_db(enrollment_no, username, password)
        if var1:
            session['username'] = username
            session['role'] = 'student'
            session['enrollment_no'] = enrollment_no
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username, enrollment number, or password. Please try again.🤡', 'error')
            return redirect(url_for('student_login'))
        
    def get_student_dashboard_data(self, enrollment_no):
        """Fetch all necessary data for the student dashboard."""
        delete_expired_documents()

        # Fetch student details
        student_details = self.db_collection.find_one({"enrollment_no": enrollment_no})
        if not student_details:
            return None

        # Fetch history
        docs = list(make_history())

        # Fetch teacher information
        teacher_infos = get_teacher_image()
        teacher_info_map = {teacher['enrollment_no']: teacher for teacher in teacher_infos}

        # Process leave entries
        leave_entries = list(temporary_application_queue.find())
        #todo Just to debug bruh ..
        print("\n\n_______________________________")
        print(leave_entries)
        print(student_details)
        print("_______________________________\n\n")

        for doc in leave_entries:
            if doc['status'] == "Accepted":
                teacher_enrollment_no = doc['enrollment_number']
                if teacher_enrollment_no in teacher_info_map:
                    doc['image_url'] = teacher_info_map[teacher_enrollment_no]['profile_pic']

        # Fetch announcements
        academic_year = student_details['academic_year']
        announcement = student_announcement_db(academic_year)

        # Return all data to the route
        return format_student_dashboard_data(student_details, announcement, leave_entries)

