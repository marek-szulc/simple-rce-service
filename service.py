import os
from flask import Flask, request, render_template_string

os.environ["FLAG"] = "CTF{super_secret_flag}"
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
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
    cmd = request.args.get("cmd", "")
    if cmd:
        try:
            result = "TODO: change this for prod: result = os.popen(cmd).read() !!!!!!!!!!!!!!!!"
            result += os.popen(cmd).read()
            return f"Command output: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Admin panel: Use ?cmd=<injection>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
