from model.user import User
from model.room import Room

# Create a new user (similar to Firebase signup persistence)
def create_user(data):
    try:
        user_data = {
            "uid": data.get("uid"),
            "displayName": data.get("displayName"),
            "photoURL": data.get("photoURL"),
            "email": data.get("email"),
        }
        user = User(**user_data)
        user.save()
        return {"success": True, "user": user.to_json()}, 201
    except Exception as e:
        print("Create user error:", e)
        return {"success": False, "message": str(e)}, 500


# Fetch a user and populate their previously visited rooms
def get_user(data):
    try:
        query = {}
        if data.get("uid"):
            query["uid"] = data["uid"]
        if data.get("email"):
            query["email"] = data["email"]

        user = User.objects(**query).first()
        if not user:
            return {"success": False, "message": "User not found"}, 404

        user_json = user.to_json()
        user_json["rooms"] = [room.to_json() for room in user.rooms]

        return {"success": True, "user": user_json}, 200
    except Exception as e:
        print("Get user error:", e)
        return {"success": False, "message": str(e)}, 500


# Add a room to a user's recently visited list (max 7 rooms)
def add_room(data):
    try:
        email = data.get("email")
        room_id = data.get("roomId")

        room = Room.objects(roomID=room_id).first()
        if not room:
            return {"success": False, "message": "Room not found"}, 404

        user = User.objects(email=email).first()
        if not user:
            return {"success": False, "message": "User not found"}, 404

        # Add room to the front if not already in list
        if room not in user.rooms:
            user.rooms.insert(0, room)
        else:
            user.rooms.remove(room)
            user.rooms.insert(0, room)

        # Keep only the latest 7 rooms
        if len(user.rooms) > 7:
            user.rooms = user.rooms[:7]

        user.save()

        user_json = user.to_json()
        user_json["rooms"] = [r.to_json() for r in user.rooms]

        return {"success": True, "user": user_json}, 200
    except Exception as e:
        print("Add room error:", e)
        return {"success": False, "message": str(e)}, 500