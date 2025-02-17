from flask import session

def format_student_dashboard_data(student_details, announcement, leave_entries):
    """Format the data structure for the student dashboard."""
    return {
        "username": session['username'],
        "ENROLLMENT_NO": student_details['enrollment_no'],
        "PASSWORD": student_details['password'],
        "DOB": student_details['dob'],
        "CONTACT": student_details['phone_no'],
        "BRANCH": student_details['branch'],
        "EMAIL_ID": student_details['email'],
        "ADDRESS": student_details['current_address'],
        "ACADEMIC_YEAR": student_details['academic_year'],
        "announcement": announcement,
        "docs": leave_entries,
        "ID": str(student_details['_id'])
    }
