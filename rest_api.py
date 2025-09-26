from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage
users = {}  # Format: {user_id: {"name": ..., "email": ...}}

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user}), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user_id = data.get("id")
    if user_id in users:
        return jsonify({"error": "User already exists"}), 400
    users[user_id] = {"name": data.get("name"), "email": data.get("email")}
    return jsonify({"message": "User created", "user": {user_id: users[user_id]}}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    users[user_id].update({"name": data.get("name"), "email": data.get("email")})
    return jsonify({"message": "User updated", "user": {user_id: users[user_id]}}), 200

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    deleted = users.pop(user_id)
    return jsonify({"message": "User deleted", "user": {user_id: deleted}}), 200

if __name__ == "__main__":
    app.run(debug=True)
