from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return "Welcome to login page"

if __name__ == "__main__":
    app.run(debug=False, port=8080)

