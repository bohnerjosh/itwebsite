from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort
import hashlib
import os 
import re
from pathlib import Path
from datetime import datetime

email_regex = re.compile(r"^(.+)@(.+)\.(.{3})")
app = Flask(__name__)
app.secret_key = b'ABCDEFG#(*JXKNCW:Q"vwads6it7y'

MESSAGE_DIR = Path(__name__).parent / "messages"

@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/services/', methods=['GET'])
def services():
    return render_template("services.html")

@app.route('/contact/', methods=['GET'])
def contact():
    return render_template("contact.html")

@app.route('/contact/', methods=["POST"])
def post_contact():
    message = ""

    email = request.form["email"]
    name = request.form["name"]
    inquiry = request.form["message"]

    if not re.fullmatch(email_regex, email):
        message = "Invalid email address"
    elif name == "":
        message = "Name cannot be blank"
    elif inquiry == "":
        message = "Message cannot be blank"

    if message == "":
        # save the message
        fileName = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"
        with open(str(MESSAGE_DIR / fileName), "w+") as f:
            f.write(email + "\n" + name + "\n" + inquiry + "\n")
        return render_template("sent.html")
    else:
        return render_template("contact.html", message=message)

@app.route('/sent/', methods=['GET'])
def sent():
    return render_template("sent.html")

@app.route('/store/', methods=['GET'])
def store():
    return render_template("store.html")
