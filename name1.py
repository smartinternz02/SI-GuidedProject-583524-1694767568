from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")

def home():
    return render_template("index1.html")

@app.route("/reg.html")

def reg():
    return render_template("reg.html")

@app.route("/login")

def login():
    return "Welcome to login page"

if __name__ == "__main__":
    app.run(debug=False)