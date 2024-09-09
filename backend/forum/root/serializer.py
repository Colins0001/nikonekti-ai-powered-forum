from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields

ma = Marshmallow()


# students
class StudentSchema(ma.Schema):
    _id = fields.String()
    type = fields.String()
    name = fields.String()
    email = fields.String()
    created_at = fields.DateTime()


# mentors
class MentorSchema(ma.Schema):
    _id = fields.Str()
    type = fields.Str()
    name = fields.Str()
    email = fields.Str()
    expertise = fields.Str()
    created_at = fields.DateTime()


# connections
class ConnectionSchema(ma.Schema):
    _id = fields.Str()
    student_email = fields.Str()
    mentor_email = fields.Str()
    connected_at = fields.DateTime()


# chatroom
class ChatRoomSchema(ma.Schema):
    _id = fields.Str()
    room_name = fields.Str()
    created_at = fields.DateTime()
    participants = fields.List(fields.Str())


# messages
class MessageSchema(ma.Schema):
    _id = fields.Str()
    room_id = fields.Str()
    sender_email = fields.Str()
    message = fields.Str()
    timestamp = fields.DateTime()