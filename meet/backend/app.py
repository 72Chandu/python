from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.security import generate_password_hash, check_password_hash
from model.user import User
from mongoengine import connect
import eventlet
from collections import defaultdict
room_users = defaultdict(set) # Dictionary to store users in each room

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

@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    if not room:
        return

    user_info = connected_users.get(request.sid, {'name': 'Stranger'})
    join_room(room)
    room_users[room].add(request.sid)

    users_in_room = [
        {'userId': sid, 'name': connected_users.get(sid, {}).get('name', 'Stranger')}
        for sid in room_users[room] if sid != request.sid
    ]

    # Send existing users only to the new joiner
    emit('existing-users', {'users': users_in_room})

    # Notify others in room about new user
    emit('user-joined', {
        'userId': request.sid,
        'name': user_info['name']
    }, room=room, include_self=False)

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


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    user_info = connected_users.pop(sid, {'name': 'Stranger'})

    # Delay removal and emit
    def delayed_removal():
        import time
        time.sleep(5)  # Wait 5 seconds to see if the user reconnects
        # If still disconnected
        still_connected = any(user['id'] == user_info.get('id') for user in connected_users.values())
        if not still_connected:
            for room, users in room_users.items():
                if sid in users:
                    users.remove(sid)
                    emit('user-left', {'userId': sid}, room=room)
            print(f"{user_info['name']} permanently disconnected.")

    eventlet.spawn(delayed_removal)

@socketio.on('leave-room')
def handle_leave_room(data):
    room = data.get('room')
    sid = request.sid

    if room in room_users and sid in room_users[room]: # Remove user from room
        room_users[room].remove(sid)

    emit('user-left', {'userId': sid}, room=room, include_self=False) # Notify others
    leave_room(room) # Leave the room
    print(f"{connected_users.get(sid, {}).get('name', 'Unknown')} left room {room}")

if __name__ == '__main__':
    socketio.run(app, debug=True)





