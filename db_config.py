from pymongo import MongoClient # type: ignore
MONGO_URI = "your_mongo_uri_here" 
client = MongoClient(MONGO_URI)
db = client['project']
creators = db.creators
collection = db['teachers']
students = db['students']
application = db['teacherApplications']
history_collection = db['history']
temporary_application_queue = db['temporary_application_queue']
payments = db["payments"]