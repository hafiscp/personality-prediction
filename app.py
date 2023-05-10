import json,requests
from flask import Flask,request, session, render_template,make_response
from pymongo import MongoClient
import uuid

from  lib import convertor

mongo_url = "mongodb://127.0.0.1:27017/"

client = MongoClient(mongo_url)
db = client["sulaiman"]
collection = db["users"]

app = Flask(__name__)

app.secret_key = "thisisasecretkey"





@app.route("/")
def index():
    # Example: Retrieve documents from the collection
    documents = collection.find()
    for doc in documents:
        print(doc)

    return "Hello, MongoDB!"

# Additional routes and application logic...


@app.route("/signin")
def signin():
    return "Hello, World!"

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        data = request.form.to_dict()
        username = data["username"]
        password = data["password"]
        email = data["email"]
        number = data["number"]
        collection.insert_one({"username":username,"password":password,"email":email,"number":number})
        return "<h1>Thanks for signing up!</h1>"

@app.route("/index", methods=["GET"])
def index1():
    return render_template("index.html")


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        data = request.form.to_dict()
        username = data["username"]
        password = data["password"]
        user = collection.find_one({"username":username,"password":password})
    if user:
        # session[username] = str(uuid.uuid4())
        response = make_response('Setting a cookie')
        response.set_cookie(username, str(uuid.uuid4()))
        return response 
        
        # return "<h1>Logged in!</h1>"

@app.route("/personality-test", methods=["GET"])
def personality_test():
    with open('questions.json') as json_file:
        data = json.load(json_file)
        return render_template("personality-test.html",data=data)

@app.route("/test", methods=["POST"])
def test():
    results = convertor(request.form.to_dict())
    print(results)
    return render_template("result.html",results=results)

if __name__ == "__main__":
    app.run(debug=True,port=5080)
