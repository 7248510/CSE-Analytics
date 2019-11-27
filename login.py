from flask import Flask, render_template, Response, request, Markup, url_for, flash, send_file, session, redirect
import requests
import json
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
app = Flask(__name__)
crypt = Bcrypt(app)
apikey = ''
reportUrl = 'https://www.virustotal.com/vtapi/v2/file/report'
scanUrl = 'https://www.virustotal.com/vtapi/v2/file/scan'
app.config['MONGO_DBNAME'] = 'login'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/login'
mongo = PyMongo(app)
@app.route('/')
def index():
    if 'username' in session:
        #Outputs the username for the session.
        return 'Hello ' + session['username']
        #Returns the index.html page
    return render_template('login.html')

@app.route('/virusTotal', methods = ['GET', 'POST'])
def virustotal():
    if 'username' in session:
        if request.method == 'POST':
            users = mongo.db.users
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
            users.insert(response.json())
        return render_template("uploadVT.html")
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    #Checks if the login user is valid
    if login_user:
        if  (crypt.check_password_hash(login_user['password'], request.form['pass'])):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            #Mongodb insert command
            users.insert({'name': request.form['username'], 'password': crypt.generate_password_hash(request.form['password'])})

            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='localhost', port='80', debug=True)
