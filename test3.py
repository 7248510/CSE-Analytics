from flask import Flask, render_template, Response, request, Markup, flash, send_file, url_for,  session, redirect
# from flask_mysqldb import MySQL
# import yaml
#from camera import VideoCamera
import os
from werkzeug import secure_filename
from flask_socketio import SocketIO, emit
import urllib
import time
import datetime
import json
import requests
import socket
# import gspread
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import json
from bson.objectid import ObjectId

app = Flask(__name__)
crypt = Bcrypt(app)
#If you're using compass above is the login name. The URI/NAME is the collection name
app.config['MONGO_DBNAME'] = 'login' #Create a local mongo db instance title login or change the name
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/CSE' #Local instance. To use this create the database on the same server you're running CSE on.
app.config['MONGO_URI'] = 'mongodb://10.0.1.2:27017/CSE' #Remote instance. I'm sure the cloud has more security/a more complex uri but the concepts should be the same. In this case I'm testing it on a local Windows Server instance.
mongo = PyMongo(app)


serverIP = socket.gethostbyname(socket.gethostname()) #Local host
reportUrl = 'https://www.virustotal.com/vtapi/v2/file/report'
scanUrl = 'https://www.virustotal.com/vtapi/v2/file/scan'
app.config['SECRET_KEY'] = 'secret!'
apikey = ''

socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'email' in session:
        users = mongo.db.users
        #Outputs the username for the session.
        login_user = users.find_one({'email' : session['email']})
        dayFileCounter = 0
        monthFileCounter = 0
        monthFileVirusCounter = 0
        monthFileVirusScansCounter = 0
        day = datetime.datetime.now().strftime("%d")
        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%y")
        h = datetime.datetime.now().strftime("%H")
        m = datetime.datetime.now().strftime("%M")
        s = datetime.datetime.now().strftime("%S")
        if login_user['admin'] == 'false':
            message = Markup(session['firstname'])
            flash(message, 'username')
            vt = mongo.db.virustotal
            lastFile = vt.find({'email': session['email']}).sort([('_id', -1)]).limit(1)
            empty = 0
            for i in users.find({'email': session['email']}):
                flash(i['_id'], 'userID')
            print(lastFile.count())
            if lastFile.count() == 0:
                empty = 1
            else:
                for i in lastFile:
                        latestFileName = i['fileName']
                        latestFileDetected = str(i['Data']['positives'])
                        latestFileVirusScans = str(i['Data']['total'])
                        lastDate = i['month'] + '/' + i['day'] + '/' + i['year']
            for i in vt.find({'email': session['email']}).sort([('_id', -1)]):
                if i['year'] == year and i['month'] == month and (int(day) - int(i['day'])) <= 1:
                    dayFileCounter += 1;
                if i['year'] == year and (int(month) - int(i['month'])) <= 1:
                    monthFileCounter += 1;
                    monthFileVirusCounter += i['Data']['positives']
                    monthFileVirusScansCounter += i['Data']['total']
            if empty == 1:
                message = Markup('''
                        <li>''' + str(dayFileCounter) + ''' Files Scanned</li>
                        <li>Last File: none</li>
                        <li>Total Scans: none</li>
                        <li>Total detected: none</li>
                ''')
                lastMonth = Markup('''
                        <li>''' + str(monthFileCounter) + ''' Files Scanned</li>
                        <li>Total Viruses Found: ''' + str(monthFileVirusCounter) + '''</li>
                        <li>Total Antiviruses used to Scan: ''' + str(monthFileVirusScansCounter) + '''</li>
                        <li>Last Date a file was Scanned: none</li>
                ''')
            else:
                message = Markup('''
                        <li>''' + str(dayFileCounter) + ''' Files Scanned</li>
                        <li>Last File: ''' + latestFileName + '''</li>
                        <li>Total Scans: ''' + latestFileVirusScans + '''</li>
                        <li>Total detected: ''' + latestFileDetected + '''</li>
                ''')
                lastMonth = Markup('''
                        <li>''' + str(monthFileCounter) + ''' Files Scanned</li>
                        <li>Total Viruses Found: ''' + str(monthFileVirusCounter) + '''</li>
                        <li>Total Antiviruses used to Scan: ''' + str(monthFileVirusScansCounter) + '''</li>
                        <li>Last Date a file was Scanned: ''' + lastDate + '''</li>
                ''')
            flash(message, 'tfHours')
            flash(lastMonth, 'lastMonth')
            session['admin'] = 'false'
            return render_template('users3.html')
        else:
            users = mongo.db.users
            message = Markup(session['firstname'])
            flash(message, 'username')
            vt = mongo.db.virustotal
            lastFile = vt.find({'email': session['email']}).sort([('_id', -1)]).limit(1)
            empty = 0
            print(lastFile.count())
            if lastFile.count() == 0:
                empty = 1
            else:
                for i in lastFile:
                        latestFileName = i['fileName']
                        latestFileDetected = str(i['Data']['positives'])
                        latestFileVirusScans = str(i['Data']['total'])
                        lastDate = i['month'] + '/' + i['day'] + '/' + i['year']
            for i in vt.find({'email': session['email']}).sort([('_id', -1)]):
                if i['year'] == year and i['month'] == month and (int(day) - int(i['day'])) <= 1:
                    dayFileCounter += 1;
                if i['year'] == year and (int(month) - int(i['month'])) <= 1:
                    monthFileCounter += 1;
                    monthFileVirusCounter += i['Data']['positives']
                    monthFileVirusScansCounter += i['Data']['total']
            if empty == 1:
                message = Markup('''
                        <li>''' + str(dayFileCounter) + ''' Files Scanned</li>
                        <li>Last File: none</li>
                        <li>Total Scans: none</li>
                        <li>Total detected: none</li>
                ''')
                lastMonth = Markup('''
                        <li>''' + str(monthFileCounter) + ''' Files Scanned</li>
                        <li>Total Viruses Found: ''' + str(monthFileVirusCounter) + '''</li>
                        <li>Total Antiviruses used to Scan: ''' + str(monthFileVirusScansCounter) + '''</li>
                        <li>Last Date a file was Scanned: none</li>
                ''')
            else:
                message = Markup('''
                        <li>''' + str(dayFileCounter) + ''' Files Scanned</li>
                        <li>Last File: ''' + latestFileName + '''</li>
                        <li>Total Scans: ''' + latestFileVirusScans + '''</li>
                        <li>Total detected: ''' + latestFileDetected + '''</li>
                ''')
                lastMonth = Markup('''
                        <li>''' + str(monthFileCounter) + ''' Files Scanned</li>
                        <li>Total Viruses Found: ''' + str(monthFileVirusCounter) + '''</li>
                        <li>Total Antiviruses used to Scan: ''' + str(monthFileVirusScansCounter) + '''</li>
                        <li>Last Date a file was Scanned: ''' + lastDate + '''</li>
                ''')
            flash(message, 'tfHours')
            flash(lastMonth, 'lastMonth')
            for i in users.find():
                if i['email'] != session['email']:
                    message = Markup('''<tr onclick="window.location.href = '/adminUserStatistics?id=''' + str(i['_id']) + ''''"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'users')
            session['admin'] = 'true'
            return render_template('admin1.html')
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email' : request.form['email']})
    if login_user:
        if  (crypt.check_password_hash(login_user['password'], request.form['password'])):
            session['email'] = request.form['email']
            session['firstname'] = login_user['firstname']
            session['lastname'] = login_user['lastname']
            users.update({'email': request.form['email']}, {"$set": {"ip": request.form['ip']}})
            return redirect(url_for('index'))
    return 'Invalid username/password combination'
@app.route('/extensionlogin', methods=['POST'])
def extensionlogin():
    users = mongo.db.users
    login_user = users.find_one({'email' : request.form['email']})
    if login_user:
        if  (crypt.check_password_hash(login_user['password'], request.form['password'])):
            session['email'] = request.form['email']
            session['firstname'] = login_user['firstname']
            session['lastname'] = login_user['lastname']
            return redirect(url_for('index'))
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:

            users.insert({'email': request.form['email'], 'password': crypt.generate_password_hash(request.form['password']), 'firstname': request.form['firstname'], 'lastname': request.form['lastname'], 'admin' : "false", 'ip': request.form['ip']})

            session['email'] = request.form['email']
            session['firstname'] = request.form['firstname']
            session['lastname'] = request.form['lastname']
            return redirect(url_for('index'))

        return 'That email already exists!'

    return render_template('register.html')

@app.route('/logout')
def logout():
    users = mongo.db.users
    users.update({'email': session['email']}, {"$set":{"ip": ""}})
    session.clear()
    return redirect(url_for('index'))
@app.route('/adminUserStatistics')
def adminUserStatistics():
    if 'email' in session:
        dayFileCounter = 0
        monthFileCounter = 0
        monthFileVirusCounter = 0
        monthFileVirusScansCounter = 0
        day = datetime.datetime.now().strftime("%d")
        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%y")
        h = datetime.datetime.now().strftime("%H")
        m = datetime.datetime.now().strftime("%M")
        s = datetime.datetime.now().strftime("%S")
        if session['admin'] == 'true':
            id = request.args.get('id')
            users = mongo.db.users
            message = Markup(session['firstname'])
            flash(message, 'username')
            flash(id, 'id')
            objectid = ObjectId(id)
            for i in users.find({"_id" : objectid}):
                message = Markup('''
                    <li>First Name: ''' + i['firstname'] + '''</li>
                    <li>Last Name: ''' + i['lastname'] + '''</li>
                    <li>Email-Address: ''' + i['email'] + '''</li>
                    <li>IP Address: '''  + i['ip'] + '''</li>
                    <li>Admin: ''' + i['admin'] + '''</li>
                ''')
                flash(message, 'userInfo')
                flash(i['firstname'], 'name')
                flash(i['ip'], 'userIp')
            vt = mongo.db.virustotal
            lastFile = vt.find({'email': session['email']}).sort([('_id', -1)]).limit(1)
            empty = 0
            print(lastFile.count())
            if lastFile.count() == 0:
                empty = 1
            else:
                for i in lastFile:
                        latestFileName = i['fileName']
                        latestFileDetected = str(i['Data']['positives'])
                        latestFileVirusScans = str(i['Data']['total'])
                        lastDate = i['month'] + '/' + i['day'] + '/' + i['year']
            for i in vt.find({'email': session['email']}).sort([('_id', -1)]):
                if i['year'] == year and i['month'] == month and (int(day) - int(i['day'])) <= 1:
                    dayFileCounter += 1;
                if i['year'] == year and (int(month) - int(i['month'])) <= 1:
                    monthFileCounter += 1;
                    monthFileVirusCounter += i['Data']['positives']
                    monthFileVirusScansCounter += i['Data']['total']
            if empty == 1:
                message = Markup('''
                        <li>''' + str(dayFileCounter) + ''' Files Scanned</li>
                        <li>Last File: none</li>
                        <li>Total Scans: none</li>
                        <li>Total detected: none</li>
                ''')
                lastMonth = Markup('''
                        <li>''' + str(monthFileCounter) + ''' Files Scanned</li>
                        <li>Total Viruses Found: ''' + str(monthFileVirusCounter) + '''</li>
                        <li>Total Antiviruses used to Scan: ''' + str(monthFileVirusScansCounter) + '''</li>
                        <li>Last Date a file was Scanned: none</li>
                ''')
            else:
                message = Markup('''
                        <li>''' + str(dayFileCounter) + ''' Files Scanned</li>
                        <li>Last File: ''' + latestFileName + '''</li>
                        <li>Total Scans: ''' + latestFileVirusScans + '''</li>
                        <li>Total detected: ''' + latestFileDetected + '''</li>
                ''')
                lastMonth = Markup('''
                        <li>''' + str(monthFileCounter) + ''' Files Scanned</li>
                        <li>Total Viruses Found: ''' + str(monthFileVirusCounter) + '''</li>
                        <li>Total Antiviruses used to Scan: ''' + str(monthFileVirusScansCounter) + '''</li>
                        <li>Last Date a file was Scanned: ''' + lastDate + '''</li>
                ''')
            flash(message, 'tfHours')
            flash(lastMonth, 'lastMonth')
            for i in users.find():
                if i['email'] != session['email']:
                    message = Markup('''<tr onclick="window.location.href = '/adminUserStatistics?id=''' + str(i['_id']) + ''''"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'users')
            return render_template('adminUserStatistics.html')
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
@app.route('/adminUserStatisticsUserResults')
def adminUserStatisticsUserResults():
    if 'email' in session:
        if session['admin'] == 'true':
            id = request.args.get('id')
            objectid = ObjectId(id)
            users = mongo.db.users
            vt = mongo.db.virustotal
            message = Markup(session['firstname'])
            flash(message, "username")
            for i in users.find({"_id" : objectid}):
                email = i['email']
            if vt.find({'email': email}).sort([('_id',-1)]).count() == 0:
                message = Markup('''<tr id="header"><td id="Name">No results found in the Database</td></tr>''')
                flash(message, 'list')
            else:
                for i in vt.find({'email': email}).sort([('_id',-1)]):
                    message = Markup('''
                                        <tr id="header" onclick="window.location.href=' ''' + i['Data']['permalink'] + ''' '">
                                            <td id="date">''' + i['month'] + '''/''' + i['day'] + '''/''' + i['year'] + '''</td>
                                            <td id="time">''' + i['hour'] + ''':''' + i['minute'] + ''':''' + i['second'] + '''</td>
                                            <td id="Name">''' + i['fileName'] + '''</td>
                                            <td id="total">''' + str(i['Data']['total']) + '''</td>
                                            <td id="detected">''' + str(i['Data']['positives']) + '''</td>
                                        </tr>
                                    ''')
                    flash(message, 'list')
            for i in users.find():
                if i['email'] != session['email']:
                    message = Markup('''<tr onclick="window.location.href = '/adminUserStatistics?id=''' + str(i['_id']) + ''''"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'users')
            return render_template('adminUserStatisticsUserResults.html')
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
@app.route('/adminMessages')
def adminMessages():
    if 'email' in session:
        if session['admin'] == 'true':
            users = mongo.db.users
            message = Markup(session['firstname'])
            flash(message, 'username')
            for i in users.find():
                if i['email'] == session['email']:
                    flash(str(i['_id']), 'userID')
                if i['email'] != session['email']:
                    message = Markup('''<tr onclick="document.getElementById('receiverName').innerHTML = this.innerHTML; var table = document.getElementById('userMessage'); for(var i = 0, row; row = table.rows[i]; i++){row.style.backgroundColor = 'rgba(255,255,255,0)'}; this.style.backgroundColor = 'rgba(255, 255, 255, 0.35)';"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'userMessage')
                    message = Markup('''<tr onclick="window.location.href = '/adminUserStatistics?id=''' + str(i['_id']) + ''''"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'users')
            return render_template('adminMessages.html')
        else:
            return redirect(url_for('userMessage'))
    else:
        return redirect(url_for('index'))
@app.route('/adminResults')
def adminResults():
    if 'email' in session:
        if session['admin'] == 'true':
            users = mongo.db.users
            vt = mongo.db.virustotal
            message = Markup(session['firstname'])
            flash(message, "username")
            if vt.find({'email': session['email']}).sort([('_id',-1)]).count() == 0:
                message = Markup('''<tr id="header"><td id="Name">No results found in the Database</td></tr>''')
                flash(message, 'list')
            else:
                for i in vt.find({'email': session['email']}).sort([('_id',-1)]):
                    message = Markup('''
                                        <tr id="header" onclick="window.location.href=' ''' + i['Data']['permalink'] + ''' '">
                                            <td id="date">''' + i['month'] + '''/''' + i['day'] + '''/''' + i['year'] + '''</td>
                                            <td id="time">''' + i['hour'] + ''':''' + i['minute'] + ''':''' + i['second'] + '''</td>
                                            <td id="Name">''' + i['fileName'] + '''</td>
                                            <td id="total">''' + str(i['Data']['total']) + '''</td>
                                            <td id="detected">''' + str(i['Data']['positives']) + '''</td>
                                        </tr>
                                    ''')
                    flash(message, 'list')
            for i in users.find():
                if i['email'] != session['email']:
                    message = Markup('''<tr onclick="window.location.href = '/adminUserStatistics?id=''' + str(i['_id']) + ''''"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'users')
            return render_template('adminResults.html')
        else:
            return redirect(url_for('userResults'))
    else:
        return redirect(url_for('index'))
@app.route('/adminUpload')
def adminUpload():
    if 'email' in session:
        if session['admin'] == 'true':
            users = mongo.db.users
            message = Markup(session['firstname'])
            flash(message, 'username')
            for i in users.find():
                if i['email'] != session['email']:
                    message = Markup('''<tr onclick="window.location.href = '/adminUserStatistics?id=''' + str(i['_id']) + ''''"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'users')
            return render_template('adminUpload.html')
        else:
            return redirect(url_for('upload1'))
    else:
        return redirect(url_for('index'))
@app.route('/userResults')
def userResults():
    if 'email' in session:
        if session['admin'] != 'true':
            vt = mongo.db.virustotal
            message = Markup(session['firstname'])
            flash(message, "username")
            if vt.find({'email': session['email']}).sort([('_id',-1)]).count() == 0:
                message = Markup('''<tr id="header"><td id="Name">No results found in the Database</td></tr>''')
                flash(message, 'list')
            else:
                for i in vt.find({'email': session['email']}).sort([('_id',-1)]):
                    message = Markup('''
                                        <tr id="header" onclick="window.location.href=' ''' + i['Data']['permalink'] + ''' '">
                                            <td id="date">''' + i['month'] + '''/''' + i['day'] + '''/''' + i['year'] + '''</td>
                                            <td id="time">''' + i['hour'] + ''':''' + i['minute'] + ''':''' + i['second'] + '''</td>
                                            <td id="Name">''' + i['fileName'] + '''</td>
                                            <td id="total">''' + str(i['Data']['total']) + '''</td>
                                            <td id="detected">''' + str(i['Data']['positives']) + '''</td>
                                        </tr>
                                    ''')
                    flash(message, 'list')
            return render_template('userResults.html')
        else:
            return redirect(url_for('adminResults'))
    else:
        return redirect(url_for('index'))
@app.route('/upload1', methods=['POST', 'GET'])
def upload1():
    if 'email' in session:
        if session['admin'] != 'true':
            message = Markup(session['firstname'])
            flash(message)
            return render_template("upload1.html")
        else:
            return redirect(url_for('adminUpload'))
    else:
        return redirect(url_for('index'))
@app.route('/uploader1', methods=['POST'])
def uploader1():
    if 'email' in session:
        client = MongoClient('localhost', 27017)
        db = client['CSE']
        #db_name = db['users']
        if 'email' in session:
            mongusr = session['email']
            if request.method == 'POST':
                file = request.files['file']
                file.save('virustotal/' + file.filename)
                name = file.filename;
                params = {'apikey': apikey}
                files = {'file': (name, open('virustotal/' + name, 'rb'))}
                response = requests.post(scanUrl, files=files, params=params)
                resource = response.json()['resource']
                params = {'apikey': apikey, 'resource': resource}
                response = requests.get(reportUrl, params=params)

                day = datetime.datetime.now().strftime("%d")
                month = datetime.datetime.now().strftime("%m")
                year = datetime.datetime.now().strftime("%y")
                h = datetime.datetime.now().strftime("%H")
                m = datetime.datetime.now().strftime("%M")
                s = datetime.datetime.now().strftime("%S")
                notInQueue = "The requested resource is not among the finished, queued or pending scans"
                while response.json()['verbose_msg'] == notInQueue:
                    params = {'apikey': apikey}
                    files = {'file': (name, open('virustotal/' + name, 'rb'))}
                    response = requests.post(scanUrl, files=files, params=params)
                    resource = response.json()['resource']
                    params = {'apikey': apikey, 'resource': resource}
                    response = requests.get(reportUrl, params=params)
                    print(response.json())
                    time.sleep(10)
                    return Markup("<script>window.alert('Its taking a while to scan this file please wait 10s or go to another page!')")
                queue = "Your resource is queued for analysis"
                while response.json()['verbose_msg'] == queue:
                    params = {'apikey': apikey, 'resource': resource}
                    response = requests.get(reportUrl, params=params)
                    time.sleep(10)
                    return Markup("<script>window.alert('Its taking a while to scan this file please wait 10s or go to another page!')")
                if response.json()['verbose_msg'] != queue:
                    mongo.db.virustotal.insert_one({"email" : mongusr, "Data" : response.json(), 'day': day, 'month': month, 'year': year, 'hour': h, 'minute': m, 'second': s, 'fileName': name})
                    client.close()
            if session['admin'] == 'true':
                return redirect(url_for('adminResults'))
            else:
                return redirect(url_for('userResults'))
@app.route('/userMessage')
def userMessage():
    if 'email' in session:
        if session['admin'] != 'true':
            users = mongo.db.users
            message = Markup(session['firstname'])
            flash(message, 'username')
            for i in users.find():
                if i['email'] == session['email']:
                    flash(str(i['_id']), 'userID')
                if i['email'] != session['email']:
                    message = Markup('''<tr id="''' + str(i['_id']) + '''"onclick="document.getElementById('receiverName').innerHTML = this.innerHTML; document.getElementById('receiverName').setAttribute('name', this.id); var table = document.getElementById('users'); for(var i = 0, row; row = table.rows[i]; i++){row.style.backgroundColor = 'rgba(255,255,255,0)'}; this.style.backgroundColor = 'rgba(255, 255, 255, 0.35)';"><td>''' + i['firstname'] + ''' ''' + i['lastname'] + '''</td></tr>''')
                    flash(message, 'users')
            return render_template('userMessage.html')
        else:
            return redirect(url_for('adminMessages'))

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json)

@socketio.on('url')
def handle_my_custom_event1(url, name, ip):
    users = mongo.db.users
    # client = gspread.authorize(creds)
    urllib.request.urlretrieve(url, "virustotal/" + name)
    # print(ip)
    # print(name)
    print(ip)
    day = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%m")
    year = datetime.datetime.now().strftime("%y")
    h = datetime.datetime.now().strftime("%H")
    m = datetime.datetime.now().strftime("%M")
    s = datetime.datetime.now().strftime("%S")

    for i in users.find({"ip" : ip}):
        email = i['email']
    mongusr = email
    params = {'apikey': apikey}
    files = {'file': (name, open("virustotal/" + name, 'rb'))}
    response = requests.post(scanUrl, files=files, params=params)

    resource = response.json()['resource']

    params = {'apikey': apikey, 'resource': resource}
    response = requests.get(reportUrl, params=params)
 
    queue = "Your resource is queued for analysis"
    while response.json()['verbose_msg'] == queue:
        params = {'apikey': apikey, 'resource': resource}
        response = requests.get(reportUrl, params=params)
        time.sleep(10)
    if response.json()['verbose_msg'] != queue:
        mongo.db.virustotal.insert_one({"email" : mongusr, "Data" : response.json(), 'day': day, 'month': month, 'year': year, 'hour': h, 'minute': m, 'second': s, 'fileName': name})
        if response.json()['positives'] == 0:
            emit('redirect', url)
def gen(VideoCamera):
    while True:
        frame = VideoCamera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/ip_add')
def ip_add():
    server = socket.gethostbyname(socket.gethostname())
    return Response(server, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="80", debug=False) #0.0.0.0 binds teh website to all available IP addresses
