from pymongo import MongoClient
from django.conf import settings

def get_mongo_connection():
    """Returns a MongoDB database connection"""
    client = MongoClient(
        host=settings.MONGO_DB['HOST'],
        port=settings.MONGO_DB['PORT'],
        username=settings.MONGO_DB['USER'],
        password=settings.MONGO_DB['PASSWORD'],
        authSource=settings.MONGO_DB['AUTH_SOURCE']
    )
    return client[settings.MONGO_DB['NAME']]

def initialize_collections():
    """Ensure required collections exist"""
    db = get_mongo_connection()
    required_collections = ['skills', 'skill_categories']
    for collection in required_collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)