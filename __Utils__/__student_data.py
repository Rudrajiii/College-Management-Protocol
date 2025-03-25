def prepare_student_data(form_data):
    """
    Prepare the student data dictionary for database update.

    Args:
        form_data (ImmutableMultiDict): The form data submitted by the user.
        profile_pic_path (str): The path to the updated profile picture.

    Returns:
        dict: A dictionary containing the staff data.
    """
    return {
            'enrollment': form_data.get('enrollment'),
            'username': form_data.get('username'),
            'password': form_data.get('password'),
            'email': form_data.get('email'),
            'branch': form_data.get('branch'),
            'year': form_data.get('year'),
            'gender': form_data.get('gender'),
            'phone': form_data.get('phone'),
            'dob': form_data.get('dob'),
            'parent_name': form_data.get('parent_name'),
            'parent_no': form_data.get('parent_no'),
            'address': form_data.get('address')
        }

