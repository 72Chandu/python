const socket = io();
const peers = {};
let localStream;
let audioEnabled = true;
let videoEnabled = true;
let roomId = "";
let mySocketId = null;
const participants = new Map();
let hostId = null; // <-- NEW: Track host ID
const savedUsername = localStorage.getItem('username') || 'You';


socket.on('connect', () => {
  mySocketId = socket.id;
  console.log("My socket ID:", mySocketId);
  participants.set(mySocketId, savedUsername); // Add self
  updateParticipantList();
});

// Host created a room
socket.on('room-created', ({ room, hostId: id }) => {
  hostId = id;
  console.log("Room created:", room, "Host ID:", hostId);
  participants.set(hostId, savedUsername + ' (Host)');
  updateParticipantList();
});

socket.on('host-info', ({ hostId: id }) => {
  hostId = id;
  console.log("Current Host ID:", hostId);
  updateParticipantList();
});

const servers = {
  iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('join-room')?.addEventListener('click', joinRoom);
  document.getElementById('generate-room')?.addEventListener('click', generateRoom);
  document.getElementById('share-screen')?.addEventListener('click', shareScreen);
  document.getElementById('toggle-audio')?.addEventListener('click', toggleAudio);
  document.getElementById('toggle-video')?.addEventListener('click', toggleVideo);
  document.getElementById('leave-room')?.addEventListener('click', leaveRoom);
  document.getElementById('show-participants')?.addEventListener('click', toggleParticipants);
  document.getElementById('show-messages')?.addEventListener('click', toggleMessages);
  document.getElementById('send-message')?.addEventListener('click', sendMessage);
  
  // Auto-rejoin if data is available
  const savedRoom = localStorage.getItem('roomId');
  const savedName = localStorage.getItem('username');
  
  if (savedRoom && savedName) {
    document.getElementById('room-input').value = savedRoom;
    window.username = savedName;
    joinRoom(); // Trigger auto join
  }
});


async function joinRoom() {
  const room = document.getElementById('room-input').value;
  roomId = room;
  // Save to localStorage
  localStorage.setItem('roomId', roomId);
  localStorage.setItem('username', username);
  socket.emit('join', { room, user: username });
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    localStream = stream;
    const audioTracks = stream.getAudioTracks();
    audioTracks.forEach(track => {
      track.enabled = true;
      console.log("Enabling audio track:", track.label);
    });

    // console.log("Local stream tracks:", stream.getTracks());
    // console.log("Audio tracks:", audioTracks);

    const localVideo=document.getElementById('localVideo');
    localVideo.srcObject = stream;
    localVideo.muted = true; // Mute local video to prevent feedback
    localVideo.className = 'w-full h-auto max-h-48 object-cover rounded-lg border-2 border-gray-300';
    socket.emit('existing-users', { room, user: username });
  } catch (err) {
    console.error('Error accessing media devices.', err);
  }
}

socket.on('existing-users', ({ users }) => {  
  if (!localStream)  return;
  
  // Clear any existing participants except yourself
  participants.clear();
  participants.set(mySocketId, savedUsername);
  users.forEach(({ userId , name}) => { 
    participants.set(userId, name || 'Stranger'); // Store in participants map
    const pc = createPeerConnection(userId); 
    peers[userId] = pc; 
    localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
    
    pc.createOffer().then(offer =>{ 
      return pc.setLocalDescription(offer); 
    }).then(() => {
        socket.emit('signal', {
          type: 'offer',              // Signaling type
          offer: pc.localDescription, // The actual WebRTC offer
          to: userId,                 // Target user to send the offer to
          room: roomId                // Room ID to help the server route the message
        });
      });
  });
  updateParticipantList(); // Update the participant list UI
});

socket.on('user-joined', ({ userId , name}) => {
  if (!peers[userId]) {
  const pc = createPeerConnection(userId);
  peers[userId] = pc;
  localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
  
  pc.createOffer().then(offer => {
    return pc.setLocalDescription(offer);
  }).then(() => {
    socket.emit('signal', {
      type: 'offer',
      offer: pc.localDescription,
      to: userId,
      room: roomId
    });
  });
}
  // Add to participant list
  participants.set(userId, name || 'Stranger');  
  updateParticipantList();
});

socket.on('user-left', ({ userId }) => {
  const videoEl = document.getElementById(`video-${userId}`);
  if (videoEl && videoEl?.parentNode) videoEl.parentNode.remove();
  if (peers[userId]) {
    peers[userId].close();
    delete peers[userId];
  }
  // Remove from participant list
  participants.delete(userId);
  updateParticipantList();
});

socket.on('signal', async ({ from, type, offer, answer, candidate }) => {
  // If stream not ready, wait
  if (!localStream) {
    try {
      localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      document.getElementById('localVideo').srcObject = localStream;
    } catch (err) {
      console.error('Stream init error:', err);
      return;
    }
  }

  let pc = peers[from];
  if (!pc) {
    pc = createPeerConnection(from);
    peers[from] = pc;
    localStream.getTracks().forEach(track => {
      
      console.log("Track kind:", track.kind);
      
      pc.addTrack(track, localStream);
    });
  }
  try {
    if (type === 'offer') {
      await pc.setRemoteDescription(new RTCSessionDescription(offer));
      const answerDesc = await pc.createAnswer();
      await pc.setLocalDescription(answerDesc);
      socket.emit('signal', { type: 'answer', answer: pc.localDescription, to: from, room: roomId });
    } else if (type === 'answer') {
      await pc.setRemoteDescription(new RTCSessionDescription(answer));
    } else if (type === 'candidate' && candidate) {
      if (pc.remoteDescription && pc.remoteDescription.type) {
        await pc.addIceCandidate(new RTCIceCandidate(candidate));
      } else {
        console.warn('Remote description not set; skipping ICE candidate');
      }
    }
  } catch (e) {
    console.error('Signal handling error:', e);
  }
});

function createPeerConnection(userId) {
  const pc = new RTCPeerConnection(servers);
  pc.onicecandidate = event => {
    if (event.candidate) {
      socket.emit('signal', { 
        type: 'candidate',
        candidate: event.candidate,
        to: userId,
        room: roomId
      });
    }
  };

   pc.ontrack = event => {
    const remoteContainer = document.getElementById('remoteVideos');
    if (!remoteContainer) {
      console.error('remoteVideos container not found in DOM.');
      return;
    }
    const existing = document.getElementById(`video-${userId}`);
    if (!existing) {
      const remoteVideo = document.createElement('video');
      remoteVideo.srcObject = event.streams[0];
      remoteVideo.id = `video-${userId}`;
      remoteVideo.autoplay = true;
      remoteVideo.playsInline = true;
      remoteVideo.controls = false;
      remoteVideo.muted = false;
      remoteVideo.className = 'w-full h-auto object-cover rounded-lg border-2 border-gray-300';
      remoteContainer.appendChild(remoteVideo);
    }
  };

  return pc;
}


function updateParticipantList() {
  const list = document.getElementById('participants');
  if (!list) return;
  list.innerHTML = ''; // Clear previous list
  participants.forEach((name, id) => {
    let displayName = name;
    if(id=== hostId) displayName += ' (Host)';
    if(id === mySocketId) displayName += ' (You)';

    const li = document.createElement('li');
    li.textContent = displayName;
    li.className = 'text-white px-2 py-1 border-b border-gray-700';
    list.appendChild(li);
  });
}

function generateRoom() {
  const room = Math.random().toString(36).substring(2, 8);
  roomId = room;
  let username=localStorage.getItem('username') || 'You';
  localStorage.setItem('roomId', roomId);
  localStorage.setItem('username', username);
  socket.emit('create-room', { room, user: username });
  const link = `${location.origin}/?room=${room}`;
  document.getElementById('room-link').textContent = link;
  document.getElementById('room-input').value = room;
}

function sendMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  console.log("Sending message:", message);
  if (!message) return
  socket.emit('message', { room: roomId, message });
  input.value = '';
}

socket.on('message', ({ user, message,from }) => {
  //  console.log("My socket ID:", mySocketId, "| Message from:", from);
   const isSelf=from===mySocketId;
   const formatted = isSelf ? `You: ${message}` : `${user || 'Stranger'}: ${message}`;
  //  console.log("Received message:", formatted, "from:", from);
   appendMessage(formatted, isSelf);
});

function appendMessage(msg,isSelf=false) {
  const messages = document.getElementById('messages');
  if(!messages) return;

  const div = document.createElement('div');
  div.textContent = msg;
  div.className=isSelf ? 'text-right text-blue-600 font-bold' : 'text-left text-blue-600';
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function shareScreen() {
  try {
    const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
    const screenTrack = screenStream.getVideoTracks()[0];
    Object.values(peers).forEach(pc => {
      const sender = pc.getSenders().find(s => s.track.kind === 'video');
      if (sender) sender.replaceTrack(screenTrack);
    });
    document.getElementById('localVideo').srcObject = screenStream;
    screenTrack.onended = async () => {
      const camStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      document.getElementById('localVideo').srcObject = camStream;
      localStream = camStream;
      const videoTrack = camStream.getVideoTracks()[0];
      Object.values(peers).forEach(pc => {
        const sender = pc.getSenders().find(s => s.track.kind === 'video');
        if (sender) sender.replaceTrack(videoTrack);
      });
    };
  } catch (err) {
    console.error("Error sharing screen:", err);
  }
}

function toggleAudio() {
  if (!localStream) return;
  audioEnabled = !audioEnabled;
  localStream.getAudioTracks().forEach(track => track.enabled = audioEnabled);
  const button = document.getElementById('toggle-audio');
  button.textContent = audioEnabled ? '🔊' : '🔇';
  console.log("Audio Enabled:", audioEnabled);
  console.log("Track.enabled:", localStream.getAudioTracks()[0].enabled); 
}

function toggleVideo() {
  if (!localStream) return;
  videoEnabled = !videoEnabled;
  localStream.getVideoTracks().forEach(track => track.enabled = videoEnabled);
  const button = document.getElementById('toggle-video');
  button.textContent = videoEnabled ? '📷' : '🎥';
}

function leaveRoom() {
  if(!roomId) return;
  socket.emit('leave', { room: roomId, user: username });

  Object.values(peers).forEach(pc => pc.close());
  for (let id in peers) delete peers[id];
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop());
    localStream = null;
  }
  document.getElementById('localVideo').srcObject = null;
  document.getElementById('remoteVideos').innerHTML = '';

  // Clear participants
  participants.clear();
  updateParticipantList();

  // Clear storage
  localStorage.removeItem('roomId');
  localStorage.removeItem('username');

  roomId = null;
  username = null;
  // alert("You have left the room.");
  window.location.href = "/login"; // Redirect to login page
  // window.close(); // Try to close the tab
  // setTimeout(() => {  // If tab is not allowed to close, redirect to a safe page
  //   window.location.href = "/login";
  // }, 1000);
}

function toggleParticipants() {
  document.getElementById('participants-container').classList.toggle('hidden');
  document.getElementById('messages-container').classList.add('hidden');
}

function toggleMessages() {
  document.getElementById('messages-container').classList.toggle('hidden');
  document.getElementById('participants-container').classList.add('hidden');
}

function cleanupStreams() {
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop());
    localStream = null;
  }

  if (originalStream) {
    originalStream.getTracks().forEach(track => track.stop());
    originalStream = null;
  }

  remoteStream = null;
}