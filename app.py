import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory store for tasks
tasks = []

# Configuration
HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
PORT = int(os.environ.get("FLASK_PORT", 5000))
DEBUG = bool(os.environ.get("FLASK_DEBUG", True))

# Home route
@app.route("/")
def home():
    return "Welcome to the Task Tracker API! Use /tasks to manage tasks."

# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

# Add a new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Task description required"}), 400
    
    task = {
        "id": len(tasks) + 1,
        "task": data["task"],
        "done": False
    }
    tasks.append(task)
    return jsonify(task), 201

# Mark a task as done
@app.route("/tasks/<int:task_id>/done", methods=["PUT"])
def mark_done(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": f"Task {task_id} deleted"}), 200

# Run the app
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
