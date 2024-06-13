from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta

# Connect to MongoDB Atlas (replace with your connection string)
client = MongoClient("mongodb+srv://sambhranta1123:SbGgIK3dZBn9uc2r@cluster0.jjcc5or.mongodb.net/")
db = client["project"]
collection = db["notifications"]

# Calculate deletion times
current_time = datetime.utcnow()  # Use UTC time
deletion_time = current_time + timedelta(minutes=1)
deletion_time1 = current_time + timedelta(minutes=1, seconds=10)
deletion_time2 = current_time + timedelta(minutes=2, seconds=20)


documents =[
    {
        "FOR": "teacher",
        "message": "Medical Leave",
        #"deleteAt": deletion_time          #remove the hash when using it during projct implementation
    },
    {
        "FOR": "teacher",
        "message": "Family Emergency",
        #"deleteAt": deletion_time1
    },
    {
        "FOR": "teacher",
        "message": "Personal Leave",
        #"deleteAt": deletion_time2
    },
    {
        "FOR": "teacher",
        "message": "Professional Development",
        #"deleteAt": deletion_time
    },
    {
        "FOR": "student",
        "message": "Maternity/Paternity Leave",
        #"deleteAt": deletion_time1
    },
    {
        "FOR": "student",
        "message": "Vacation",
        #"deleteAt": deletion_time2
    },
    
    {
        "FOR": "student",
        "message": "Unexpected Travel",
        #"deleteAt": deletion_time
    }
]


collection.insert_many(documents)
print("Documents inserted with deleteAt field.")


collection.create_index(
    [("deleteAt", ASCENDING)],
    expireAfterSeconds=0
)
print("TTL index created on deleteAt field.")
