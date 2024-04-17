import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient


load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# Connect to mongodb
client = MongoClient(MONGODB_URL)
db = client['peaky-blinders']


def authenticate_user(username, password):
    try:
        collection = db['login_details']

        # Define the criteria for the username and password
        input_username = username
        input_password = password

        # Find the user by username
        user_login_document = collection.find_one({"username": input_username})

        if user_login_document:
            stored_password = user_login_document["password"]

            if username == "admin" and stored_password == password:
                return "Login admin"
            elif stored_password == password:
                return "Login Successful"
            else:
                return "Login Failed: Incorrect Password"
        else:
            return "Login Failed: User not found"
    except Exception as e:
        return "An error occurred: " + str(e)


def create_user_account(username, email, password):
    try:
        collection = db['login_details']

        # Check if the username already exists in the database
        existing_user = collection.find_one({'username': username})
        if existing_user:
            print("Username already exists. Please choose a different username.")
            return False

        # If the username doesn't exist, insert the new user
        submission = {'username': username,
                      'email': email,
                      'password': password
                      }
        collection.insert_one(submission)
        print(f"Data has been recorded")
        return True

    except Exception as e:
        return "An error occurred: " + str(e)