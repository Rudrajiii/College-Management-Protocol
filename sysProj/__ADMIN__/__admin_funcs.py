# __ADMIN__/__admin_funcs.py
from time import time
from flask import session
from caching import user_cache
from functions import admin_login_db, count_students, count_teachers

class AdminFuncs:
    def __init__(self, cache):
        self.cache = cache

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
