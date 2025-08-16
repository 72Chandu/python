from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.security import generate_password_hash, check_password_hash
from model.user import User
from mongoengine import connect
import eventlet
from collections import defaultdict
from model.room import Room

room_users = defaultdict(set) # Dictionary to store users in each room
room_hosts = {}  # Host SID for each room  <-- NEW
try:
    connect(
        db='meet_db',
        host='mongodb://localhost:27017/meet_db',
        alias='default'
    )
    print("Connected to MongoDB.")
except Exception as e:
    print("Failed to connect to MongoDB:", str(e))
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name= request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.objects(email=email).first():
            flash("Email already exists!")
            return redirect('/register')
        hashed_pw = generate_password_hash(password)
        User(email=email, password=hashed_pw,username=name).save()
        flash("Registered successfully! Please login.")
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.objects(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = str(user.id)
            return redirect('/')
        else:
            flash("Invalid credentials!")
            return redirect('/login')
    return render_template('login.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # or register

    user = User.objects(id=session['user_id']).first()
    return render_template('index.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- Socket.IO Events ---------------- #
connected_users = {}

@socketio.on('connect')
def handle_connect():
    user_id = session.get('user_id')
    if user_id:
        user = User.objects(id=user_id).first()
        if user:
            connected_users[request.sid] = {'id': str(user.id), 'name': user.username, 'email': user.email}
            print(f"{user.username} connected with SID {request.sid}")
    else:
        print("Anonymous connection rejected")
        return False  # Disconnect unauthenticated sockets

# --- helper to emit participant info to everyone in a room ---
@socketio.on('get_participants')
def handle_get_participants(data):
    room_id = data.get('roomId')
    room = Room.objects(roomId=room_id).first()

    # print(f"\033[94m[get_participants called with:]\033[0m {room_id}")
    # print(f"\033[94m[room:]\033[0m {room}")

    if room:
        # Fetch participant details from your User model
        participants_data = []
        for participant_id in room.participants:
            user = User.objects(id=participant_id).first()
            participants_data.append({
                "id": str(user.id),
                "name": user.username  # or whatever your field is
            })
    
        
        socketio.emit('participants_list', {
            "participants": participants_data,
            "host": str(room.host)
        }, room=room_id)


@socketio.on('create-room')
def handle_create_room(data):
    room = data.get('room')
    user_info = connected_users.get(request.sid)
    if not room:
        return

    join_room(room)
    room_hosts[room] = request.sid
    room_users[room].add(request.sid)

    # persist in DB as a new Room (if not exists)
    db_user = None
    if user_info and user_info.get('id'):
        db_user = User.objects(id=user_info['id']).first()

    room_doc = Room.objects(roomId=room).first()
    if not room_doc:
        room_doc = Room(roomId=room, host=db_user)
    # add host to participants (record who joined)
    if db_user and db_user not in room_doc.participants:
        room_doc.participants.append(db_user)
    room_doc.save()

    emit('room-created', {'room': room, 'hostId': request.sid})
    handle_get_participants(room)


@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    if not room:
        return

    user_info = connected_users.get(request.sid, {'name': 'Stranger'})
    join_room(room)
    room_users[room].add(request.sid)

    # persist to DB: add this user to room.participants (record)
    db_user = None
    if user_info and user_info.get('id'):
        db_user = User.objects(id=user_info['id']).first()

    room_doc = Room.objects(roomId=room).first()
    if not room_doc:
        # create room record if it didn't exist
        room_doc = Room(roomId=room, host=db_user)
    if db_user and db_user not in room_doc.participants:
        room_doc.participants.append(db_user)
    room_doc.save()

    # Send existing users to the newcomer (socket-level users)
    users_in_room = [
        {'userId': sid, 'name': connected_users.get(sid, {}).get('name', 'Stranger')}
        for sid in room_users[room] if sid != request.sid
    ]
    emit('existing-users', {'users': users_in_room}, to=request.sid)

    # Notify other sockets
    emit('user-joined', {'userId': request.sid, 'name': user_info['name']}, room=room, include_self=False)

    # Send a full participants list (socketId <-> DB userId <-> name)
    handle_get_participants(room)


@socketio.on('leave-room')
def handle_leave_room(data):
    room = data.get('room')
    sid = request.sid
    if room in room_users and sid in room_users[room]:
        room_users[room].remove(sid)

    emit('user-left', {'userId': sid}, room=room, include_self=False)
    handle_get_participants(room)
    leave_room(room)

    if room_hosts.get(room) == sid:
        if room_users[room]:
            new_host = next(iter(room_users[room]))
            room_hosts[room] = new_host
            emit('host-info', {'hostId': new_host}, room=room)
        else:
            room_hosts.pop(room, None)


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    user_info = connected_users.pop(sid, {'name': 'Stranger'})

    def delayed_removal():
        import time
        time.sleep(5)  # short grace period
        still_connected = any(user['id'] == user_info.get('id') for user in connected_users.values())
        if not still_connected:
            for room, users in room_users.items():
                if sid in users:
                    users.remove(sid)
                    emit('user-left', {'userId': sid}, room=room)
                    handle_get_participants(room)
            print(f"{user_info.get('name')} permanently disconnected.")

    eventlet.spawn(delayed_removal)

@socketio.on('signal')
def handle_signal(data):
    to = data.get('to')
    if to:
        emit('signal', {
            'from': request.sid,
            'type': data.get('type'),
            'offer': data.get('offer'),
            'answer': data.get('answer'),
            'candidate': data.get('candidate')
        }, to=to)


@socketio.on('message')
def handle_message(data):
    room = data.get('room')
    message = data.get('message')
    sender_info = connected_users.get(request.sid, {'name': 'Stranger'})

    emit('message', {
        'message': message,
        'user': sender_info['name'],
        'from': request.sid # Add sender socket ID
    }, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)





