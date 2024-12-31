from flask import session, flash, redirect, url_for
from caching import user_cache
from functions import *

class TeacherFuncs:
    def __init__(self , cache , connection_db):
        self.cache = cache
        self.connection_db = connection_db
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