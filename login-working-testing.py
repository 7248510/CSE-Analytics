import json
import requests
import datetime
import os
from flask import Flask, render_template, url_for, request, session, redirect, Markup, flash, send_file
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
app = Flask(__name__)
crypt = Bcrypt(app)
app.config['MONGO_DBNAME'] = 'CSE'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/CSE'
mongo = PyMongo(app)
@app.route('/virustotal', methods=['POST', 'GET'])
def vt():
    app.config['SECRET_KEY'] = 'secret!'
    apikey = ''
    reportUrl = 'https://www.virustotal.com/vtapi/v2/file/report'
    scanUrl = 'https://www.virustotal.com/vtapi/v2/file/scan'
    client = MongoClient('localhost', 27017)
    db = client['CSE']
    db_name = db['users']
    while 'email' in session:
        mongusr = session['email']
        if request.method == 'POST':
            file = request.files['file']
            file.save(file.filename)
            name = file.filename;
            params = {'apikey': apikey}
            files = {'file': (name, open(name, 'rb'))}
            response = requests.post(scanUrl, files=files, params=params)
            resource = response.json()['resource']
            params = {'apikey': apikey, 'resource': resource}
            response = requests.get(reportUrl, params=params)
            output = open('test.json', 'w')
            json.dump(response.json(), output, indent=4)
            message = Markup("<pre style='position:absolute; width:50%; height: 75%; padding: 50px; overflow-x: hidden; overflow-y: auto;'><code>" + json.dumps(response.json(), indent=4) + "</code></pre>")
            flash(message)
            mongo.db.users.insert_one({"email" : mongusr, "Data" : response.json(), "Universal time stamp" : datetime.datetime.now()})
            #mongo.db.users.update({'$inc': {"username": mongusr , "_id" : 0}})
            #mongo.db.users.create_index( { "user_id" : 1}, {"_id": 1})
            #db_name.insert({'user': "test"})
            #db_name.create_index([('VirusTotal')], name='Caleb')
            #db_name.insert({'_id': 1})
            client.close()
        return render_template('uploadVT.html')
@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('vt'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'Email-address' : request.form['email']})

    if login_user:
        if  (crypt.check_password_hash(login_user['password'], request.form['pass'])):
            session['email'] = request.form['email']
            #Routes to the userpanel
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['email']})
        if existing_user is None:
            #db.createCollection({'name' : request.form['username'], 'password': crypt.generate_password_hash(request.form['password'])})
            #'Email-address' : request.form['email']
            users.insert({'Email-address' : request.form['email'], 'password': crypt.generate_password_hash(request.form['password']),'firstname' : request.form['firstname'],'lastname' : request.form['lastname'] })
            session['email'] = request.form['email']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


#to find the users/list there connection type in this command and select mongodb3
#db.users.collection.find()
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
