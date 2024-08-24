from pymongo import MongoClient # type: ignore
MONGO_URI = "mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/project"
client = MongoClient(MONGO_URI)
db = client['project']
creators = db.creators
collection = db['teachers']
students = db['students']
application = db['teacherApplications']
history_collection = db['history']
temporary_application_queue = db['temporary_application_queue']