from app import db ,cache
def get_user_from_db(username):
    print("Fetching user from cache or MongoDB if not cached")
    user =  db.creators.find_one({"username": username})
    return user

@cache.memoize(timeout=300)  # Caching this function's result for 5 minutes
def get_user(username):
    return get_user_from_db(username)