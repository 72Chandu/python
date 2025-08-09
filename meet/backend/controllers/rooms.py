from flask import Blueprint, request, jsonify, render_template, redirect
from model.room import Room  # Assuming Room is defined in models/room.py
import uuid

room_bp = Blueprint('room_bp', __name__)

# Create a room
@room_bp.route('/create-room', methods=['POST'])
def create_room():
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        room_id = str(uuid.uuid4())

        room = Room(admin=email, name=name, roomID=room_id)
        room.save()

        return jsonify(success=True, room=room.to_json()), 201
    except Exception as e:
        print(e)
        return jsonify(success=False), 500

# Get a room by roomID
@room_bp.route('/get-room', methods=['POST'])
def get_room():
    try:
        data = request.get_json()
        room_id = data.get('room')
        room = Room.objects(roomID=room_id).first()
        if room:
            return jsonify(success=True, room=room.to_json()), 200
        else:
            return jsonify(success=False, message='Room not found'), 404
    except Exception as e:
        print(e)
        return jsonify(success=False, message='Room not found'), 404

# Get all rooms created by a specific user
@room_bp.route('/get-room-by-user', methods=['POST'])
def get_room_by_user():
    try:
        data = request.get_json()
        email = data.get('email')

        rooms = Room.objects(admin=email)

        if not rooms:
            return jsonify(success=False, message='Room not found'), 404
        else:
            return jsonify(success=True, rooms=[room.to_json() for room in rooms]), 200
    except Exception as e:
        print(e)
        return jsonify(success=False, message='Something went wrong'), 500

# Middleware-like endpoint for chat room
@room_bp.route('/chat/<room>')
def chat_room_mw(room):
    try:
        room_obj = Room.objects(roomID=room).first()
        if room_obj:
            return render_template('chatroom.html', roomId=room)
    except Exception as e:
        print(e)
    return redirect('/home')

# Middleware-like endpoint for video room
@room_bp.route('/room/<room>')
def room_mw(room):
    try:
        room_obj = Room.objects(roomID=room).first()
        if room_obj:
            return render_template('room.html', roomId=room)
    except Exception as e:
        print(e)
    return redirect('/home')
