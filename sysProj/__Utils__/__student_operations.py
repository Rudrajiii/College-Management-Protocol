from functions import *
from flask import *
import os

def remove_student(enrollment_no , root_file_dir):
    y = remove_student_db(enrollment_no)
    if y == 0:
        flash('⚠️ Student not found.', 'error')  
    else:
        try:
            filename = os.path.join(root_file_dir, y)
            os.remove(filename)
            flash('✅ Student removed successfully!', 'success')  
        except FileNotFoundError:
            flash('⚠️ Image file of student not found.', 'error')

def updated_image(file , filename , form_data , en , root_file_dir):
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".png" , ".jpg" , ".jpeg"]:
        flash('⚠️ student image file is not jpg , jpeg or png.' , 'error')
        return redirect(url_for('admin_dashboard'))
    profile_pic_location = en + file_extension
    #* Save the uploaded image file to the static folder
    filename = os.path.join(root_file_dir, profile_pic_location)
    file.save(filename)
    edit_student_update_db(en,form_data,profile_pic_location)
    flash('✅ Student records successfully edited!' , 'success')
    return redirect(url_for('admin_dashboard'))


