def prepare_staff_data(form_data, profile_pic_path):
    """
    Prepare the staff data dictionary for database update.

    Args:
        form_data (ImmutableMultiDict): The form data submitted by the user.
        profile_pic_path (str): The path to the updated profile picture.

    Returns:
        dict: A dictionary containing the staff data.
    """
    return {
        "username": form_data.get('username'),
        "email": form_data.get('email'),
        "password": form_data.get('password'),
        "gender": form_data.get('gender'),
        "phone_no": form_data.get('phone_no'),
        "enrollment_no": form_data.get('enrollment_no'),
        "current_address": form_data.get('current_address'),
        "bio": form_data.get('bio'),
        "description": form_data.get('description'),
        "rating": int(form_data.get('rating')) if form_data.get('rating') else 0,
        "reviews": int(form_data.get('reviews')) if form_data.get('reviews') else 0,
        "teaches_total_students": int(form_data.get('teaches_total_students')) if form_data.get('teaches_total_students') else 0,
        "dob": form_data.get('dob'),
        "profile_pic": profile_pic_path,
    }
