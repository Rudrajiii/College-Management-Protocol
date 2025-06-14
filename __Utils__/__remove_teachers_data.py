import os
from flask import *
def remove_teacher(app, collection, user_id):
    try:
        user_details = collection.find_one({"_id": user_id})
        print("User details:", user_details)
        result = collection.delete_one({"_id": user_id})
        print("Delete result:", result.deleted_count)

        if result.deleted_count == 1:
            # Delete user profile pic
            if user_details and 'profile_pic' in user_details:
                profile_pic_path = user_details['profile_pic']
                print("Profile picture path:", profile_pic_path)
                if profile_pic_path:
                    full_path = os.path.join(app.root_path, profile_pic_path[1:])
                    print("Full path:", full_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": "Internal server error"}), 500
