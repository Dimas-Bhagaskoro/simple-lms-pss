from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)

db = client["simple_lms"]

activity_logs = db["activity_logs"]

learning_analytics = db["learning_analytics"]