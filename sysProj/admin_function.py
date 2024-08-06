def get_image_name(enrollment_no, extension, updated=False):
    if updated:
        return f'{enrollment_no}(updated){extension}'
    else:
        return f'{enrollment_no}{extension}'