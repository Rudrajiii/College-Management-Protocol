from datetime import datetime
from db_config import *
def delete_expired_documents():
    current_time = datetime.now()
    result = temporary_application_queue.delete_many({'deleted_at': {'$lte': current_time}})
    if result.deleted_count > 0:
        print(f"Deleted {result.deleted_count} expired document(s)")

def update_temporary_queue():
    accepted_applications = history_collection.find({'status': 'Accepted'})
    for app in accepted_applications:
        if app['requested_gap'] >= 0:
            temporary_application_queue.update_one(
                {'application_id': app['application_id']},
                {'$set': app},
                upsert=True
            )
    # Remove entries from temporary queue if they are not in accepted state anymore
    all_temp_entries = temporary_application_queue.find()
    for entry in all_temp_entries:
        if history_collection.find_one({'application_id': entry['application_id'], 'status': 'Accepted'}) is None:
            temporary_application_queue.delete_one({'application_id': entry['application_id']})