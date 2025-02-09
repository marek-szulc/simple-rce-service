from flask import Flask, request, render_template_string, jsonify
import os

app = Flask(__name__)
flag = os.getenv("FLAG", "No flag found")
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "supersecure"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Login failed. Please try again."
    return render_template_string("""
        <form method='POST'>
            <input type='text' name='username' placeholder='Username' required>
            <input type='password' name='password' placeholder='Password' required>
            <button type='submit'>Login</button>
        </form>
    """)

@app.route("/admin", methods=["GET"])
def admin():
    auth = request.authorization
    if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 401
    cmd = request.args.get("cmd", "")
    if cmd:
        try:
            result = os.popen(cmd).read()
            return f"Command output: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Admin panel: Use ?cmd=<command>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
