from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

profiles = [
    {"id": 1, "name": "Coupon Queen USA", "status": "Available", "user": "", "lastUpdated": ""},
    {"id": 2, "name": "FOX 2", "status": "Available", "user": "", "lastUpdated": ""},
    {"id": 3, "name": "Kevin", "status": "Available", "user": "", "lastUpdated": ""},
    {"id": 4, "name": "Sindhu Patil", "status": "Available", "user": "", "lastUpdated": ""},
    {"id": 5, "name": "Soffik Hossain", "status": "Available", "user": "", "lastUpdated": ""},
    {"id": 6, "name": "Prasad Kharad", "status": "Available", "user": "", "lastUpdated": ""},
    {"id": 7, "name": "Nazmin SS", "status": "Available", "user": "", "lastUpdated": ""},
    {"id": 8, "name": "WEZA ROGERIO", "status": "Available", "user": "", "lastUpdated": ""}
]

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/profiles', methods=['GET'])
def get_profiles():
    return jsonify(profiles)

@socketio.on('connect')
def handle_connect():
    print("A client connected")
    socketio.emit('update_profiles', profiles, to=None)  # Send data to all clients

@socketio.on('use_profile')
def use_profile(data):
    for profile in profiles:
        if profile["id"] == data["id"] and profile["status"] == "Available":
            profile["status"] = "In Use"
            profile["user"] = data["user"]
            profile["lastUpdated"] = get_current_time()
            break
    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True

@socketio.on('release_profile')
def release_profile(data):
    for profile in profiles:
        if profile["id"] == data["id"] and profile["status"] == "In Use":
            profile["status"] = "Available"
            profile["user"] = ""
            profile["lastUpdated"] = get_current_time()
            break
    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True

@socketio.on('add_profile')
def add_profile(data):
    new_profile = {
        "id": len(profiles) + 1,
        "name": data["name"],
        "status": "Available",
        "user": "",
        "lastUpdated": get_current_time()
    }
    profiles.append(new_profile)
    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True

@socketio.on('delete_profile')
def delete_profile(data):
    global profiles
    profiles = [p for p in profiles if p["id"] != data["id"]]
    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
