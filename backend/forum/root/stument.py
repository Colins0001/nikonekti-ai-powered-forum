from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

# getting env from flask
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME")
MONGODB_COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME")
MONGODB_STUDENTS_COLLECTION_NAME = os.environ.get("MONGODB_STUDENTS_COLLECTION_NAME")
MONGODB_MENTORS_COLLECTION_NAME = os.environ.get("MONGODB_MENTORS_COLLECTION_NAME")
MONGODB_MESSAGES_COLLECTION_NAME = os.environ.get("MONGODB_MESSAGES_COLLECTION_NAME")
MONGODB_CONNECTIONS_COLLECTION_NAME = os.environ.get(
    "MONGODB_CONNECTION_COLLECTION_NAME"
)
MONGODB_CHAT_ROOM_COLLECTION_NAME = os.environ.get("MONGODB_CHAT_ROOM_COLLECTION_NAME")


class StudentMentorForum:
    def __init__(
        self,
        db_name=MONGODB_DB_NAME,
        connections_collection=MONGODB_CONNECTIONS_COLLECTION_NAME,
        messages_collection=MONGODB_MESSAGES_COLLECTION_NAME,
        chat_rooms_collection=MONGODB_CHAT_ROOM_COLLECTION_NAME
    ):
        # Connect to MongoDB server
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[db_name]
        self.connections_collection = self.db[connections_collection]
        self.messages_collection = self.db[messages_collection]
        self.chat_rooms_collection = self.db[chat_rooms_collection]

    def add_student(self, student_name, student_email):
        # connecting to the collection
        self.collection = self.db[MONGODB_STUDENTS_COLLECTION_NAME]
        student = {
            "type": "student",
            "name": student_name,
            "email": student_email,
            "created_at": datetime.datetime.now(),
        }
        result = self.collection.insert_one(student)
        return result.inserted_id

    def add_mentor(self, mentor_name, mentor_email, expertise):
        # connecting to the collection
        self.collection = self.db[MONGODB_MENTORS_COLLECTION_NAME]
        mentor = {
            "type": "mentor",
            "name": mentor_name,
            "email": mentor_email,
            "expertise": expertise,
            "created_at": datetime.datetime.now(),
        }
        result = self.collection.insert_one(mentor)
        return result.inserted_id

    ############################################################################################################
    # Message Board
    ############################################################################################################
    
    def post_message(self, room_id, sender_email, message):
        # connecting to the collection
        self.collection = self.db[MONGODB_MESSAGES_COLLECTION_NAME]
        msg = {
            'room_id': room_id,
            'sender_email': sender_email,
            'message': message,
            'timestamp': datetime.datetime.now()
        }
        result = self.collection.insert_one(msg)
        return result.inserted_id
    
    def get_messages_by_room(self, room_id):
        return list(self.messages_collection.find({'room_id': room_id}))
    
    ###############################################################################################################
    # Student Email and Mentor Email
    ###############################################################################################################

    # Find a student by email or a mentor by email
    def find_student_by_email(self, email):
        self.collection = self.db[MONGODB_STUDENTS_COLLECTION_NAME]
        return self.collection.find_one({"email": email})

    def find_mentor_by_email(self, email):
        self.collection = self.db[MONGODB_MENTORS_COLLECTION_NAME]
        return self.collection.find_one({"email": email})

    # Update a student by ID or a mentor by ID
    def update_student_by_id(self, student_id, updates):
        self.collection = self.db[MONGODB_STUDENTS_COLLECTION_NAME]
        result = self.collection.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": {"name": updates["name"], "email": updates["email"]}},
        )

        return result.modified_count

    def update_mentor_by_id(self, mentor_id, updates):
        self.collection = self.db[MONGODB_MENTORS_COLLECTION_NAME]
        result = self.collection.update_one(
            {"_id": ObjectId(mentor_id)},
            {
                "$set": {
                    "name": updates["name"],
                    "email": updates["email"],
                    "expertise": updates["expertise"],
                }
            },
        )
        return result.modified_count

    # Delete a student by ID or a mentor by ID
    def delete_student(self, user_id):
        self.collection = self.db[MONGODB_STUDENTS_COLLECTION_NAME]
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count

    def delete_mentor(self, user_id):
        self.collection = self.db[MONGODB_MENTORS_COLLECTION_NAME]
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count

    # Search mentors by expertise
    def search_mentors(self, expertise=None):
        query = {"type": "mentor"}
        if expertise:
            query["expertise"] = expertise
        return list(self.collection.find(query))

    # Creating connection between student and mentor
    def connect_student_to_mentor(self, student_email, mentor_email):
        connection = {
            "student_email": student_email,
            "mentor_email": mentor_email,
            "connected_at": datetime.datetime.now(),
        }
        result = self.connections_collection.insert_one(connection)
        return result.inserted_id
    
    # finding  the connection between student and mentor
    def find_connection_by_student_email(self, student_email):
        self.collection = self.db[MONGODB_CONNECTIONS_COLLECTION_NAME]
        return self.connections_collection.find({"student_email": student_email})
    
    # finding the connection between student and mentor
    def find_connection_by_mentor_email(self, mentor_email):
        self.collection = self.db[MONGODB_CONNECTIONS_COLLECTION_NAME]
        return self.connections_collection.find({"mentor_email": mentor_email})

    # finding the connection using ID
    def find_connection_by_id(self, connection_id):
        self.collection = self.db[MONGODB_CONNECTIONS_COLLECTION_NAME]
        return self.connections_collection.find_one({"_id": ObjectId(connection_id)})
    
    # delete the connection between student and mentor
    def delete_connection(self, connection_id):
        self.collection = self.db[MONGODB_CONNECTIONS_COLLECTION_NAME]
        result = self.collection.delete_one({"_id": ObjectId(connection_id)})
        return result.deleted_count
    
    
    ############################################################################################################
    # Creatin rooms for the chat
    ############################################################################################################
    
    def create_room(self, room_name, participants):
        chat_room = {
            'room_name': room_name,
            'created_at': datetime.datetime.now(),
            'participants': participants
        }
        result = self.chat_rooms_collection.insert_one(chat_room)
        return result.inserted_id

    def get_rooms(self):
        return list(self.chat_rooms_collection.find())

    def get_room_by_id(self, room_id):
        return self.chat_rooms_collection.find_one({'_id': ObjectId(room_id)})
    
    def find_room_by_participants(self, participants: list):
        return self.chat_rooms_collection.find_one({'participants': participants})
    
    def join_room(self, room_id, participant_email):
        self.chat_rooms_collection.update_one(
            {'_id': ObjectId(room_id)},
            {'$addToSet': {'participants': participant_email}}
        )
    
    def leave_room(self, room_id, participant_email):
        self.chat_rooms_collection.update_one(
            {'_id': ObjectId(room_id)},
            {'$pull': {'participants': participant_email}}
        )
    
    def delete_room(self, room_id):
        result = self.chat_rooms_collection.delete_one({'_id': ObjectId(room_id)})
        return result.deleted_count