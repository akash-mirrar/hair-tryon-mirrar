from functools import wraps
from flask import request, session, jsonify
import pymongo, jwt, os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))
MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
collection_name = "hair_tryon"

# Create a MongoDB client
# ca = certifi.where()

client = pymongo.MongoClient(MONGO_URI)

# Access your database and collection
db = client["hair_tryon"]
user_collection = db["user"]

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify(message="Invalid Token"), 401

        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        current_user = user_collection.find_one({"phone_no": data["phone_no"]})

        return f(current_user, **kwargs)
    return decorator
