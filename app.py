from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO
import datetime
import json
from plyer import notification

app = Flask(__name__,template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*")
def create_lst(file):
    with open(file, "r") as file:
        profiles = json.loads(f"[{file.read().strip()}]")  # Wrap in list format
    file.close()
    return profiles
#profiles = create_lst("user_data.txt") 
def add_user_data(file, new_profile):
    with open(file, "a") as file:  # Open file in append mode
        file.write(",\n")
        json.dump(new_profile, file)
        print(new_profile)
    file.close()    
    print(f"Profile '{new_profile['name']}' added successfully!")

def rmv_user_data(file, new_profile):
    profiles = create_lst(file)  # Load profiles from file

    # Filter out the profile with matching name and status 'Available'
    updated_profiles = [p for p in profiles if not (p["name"] == new_profile and p["status"] == "Available")]

    # Write the updated profiles back to the file
    with open(file, "w") as f:
        f.write(",\n".join(json.dumps(profile) for profile in updated_profiles)) 
    f.close() 
    #print(f"Profile '{new_profile}' removed successfully!")

#profiles = create_lst("user_data.txt")


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
def logger():
    pass


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/profiles', methods=['GET'])
def get_profiles():
    return jsonify(profiles)

@app.route('/admin')
def admin():
    return render_template("admin.html")  # Serves the admin page


@socketio.on('connect')
def handle_connect():
    profiles= create_lst("user_data.txt")
    print("A client connected")
    socketio.emit('update_profiles', profiles, to=None)  # Send data to all clients

@socketio.on('use_profile')
def use_profile(data):
    profiles = create_lst("user_data.txt")  # Load profiles from file

    for profile in profiles:
        if profile["id"] == data["id"] and profile["status"] == "Available":
            profile["status"] = "In Use"
            profile["user"] = data["user"]
            profile["lastUpdated"] = get_current_time()
            
            break  

    with open("user_data.txt", "w") as f:
        f.write(",\n".join(json.dumps(profile) for profile in profiles))
    socketio.emit('notify', {
        "title": "Profile In Use",
        "message": f"Profile '{profile['name']}' is now in used by {profile['user']}"
    })
    socketio.emit('update_profiles', profiles)  

@socketio.on('release_profile')
def release_profile(data):
    profiles = create_lst("user_data.txt")  

    for profile in profiles:
        if profile["id"] == data["id"] and profile["status"] == "In Use":
            profile["status"] = "Available"
            profile["user"] = ""
            profile["lastUpdated"] = get_current_time()
            break  
    with open("user_data.txt", "w") as f:
        f.write(",\n".join(json.dumps(profile) for profile in profiles))
    socketio.emit('notify', {
        "title": "Profile free",
        "message": f"Profile '{profile['name']}' is now free."
    })
    socketio.emit('update_profiles', profiles)  

"""@socketio.on('use_profile')
def use_profile(data):
    profiles= create_lst("user_data.txt")
    for profile in profiles:
        if profile["id"] == data["id"] and profile["status"] == "Available":
            profile["status"] = "In Use"
            profile["user"] = data["user"]
            profile["lastUpdated"] = get_current_time()
            break
    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True"""

"""@socketio.on('release_profile')
def release_profile(data):
    profiles= create_lst("user_data.txt")
    for profile in profiles:
        if profile["id"] == data["id"] and profile["status"] == "In Use":
            profile["status"] = "Available"
            profile["user"] = ""
            profile["lastUpdated"] = get_current_time()
            break
    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True
"""
#@socketio.on('add_profile')
#def add_profile(data):
#    new_profile = {
#        "id": len(profiles) + 1,
#        "name": data["name"],
#        "status": "Available",
#        "user": "",
#        "lastUpdated": get_current_time()
#    }
#    profiles.append(new_profile)
#    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True

#@socketio.on('delete_profile')
#def delete_profile(data):
#    global profiles
#    profiles = [p for p in profiles if p["id"] != data["id"]]
#    socketio.emit('update_profiles', profiles, to=None)  # Fix: Replaces broadcast=True

@app.route('/add_prfl', methods=['POST'])
def add_prfl():
    profiles= create_lst("user_data.txt")
    data = request.json
    name=data.get("profileName")
    if name!="":
        new_profile = {
            "id": len(profiles) + 1,
            "name": name,
            "status": "Available",
            "user": "",
            "lastUpdated": get_current_time()
        }
    else:
        return jsonify({"message": "Profile name cannot be empty!", "profiles": profiles,"success": False })
    if name.lower() in [i['name'].lower() for i in profiles]:
        return jsonify({"message": f"'{name}' Profile already exists!", "profiles": profiles,"success": False })
   # print(new_profile)
    else:
        add_user_data("user_data.txt", new_profile)
        
    #return redirect(url_for('admin'))
        return jsonify({"message": f"'{name}' Profile added successfully!", "profiles": profiles,"success": True })
    
@app.route('/rmv_prfl', methods=['POST'])
def rmv_prfl():
    profiles = create_lst("user_data.txt")
    data = request.json
    name=data.get("profileName")
   #print(name)
    #print("p",profiles,"pend")
    for i in profiles:
        #print("n",name,"nend")       
        if i['name']==name and i['status']=="Available":
            
            rmv_user_data("user_data.txt", name)
            print(f"Profile removed successfully!{name}")
            
            return jsonify({"message": "Profile removed successfully!", "profiles": profiles,"success": True })
        #print(i)
        
    return jsonify({"message": "Profile is in use or profile doesn't exist", "profiles": profiles,"success": False })
        
        

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)
