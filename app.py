from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user store
users = {}
next_id = 1

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

# Get a user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Name and email are required"}), 400

    user = {
        "id": next_id,
        "name": data['name'],
        "email": data['email']
    }
    users[next_id] = user
    next_id += 1

    return jsonify(user), 201

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])

    users[user_id] = user
    return jsonify(user), 200

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
