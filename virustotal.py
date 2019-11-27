from flask import Flask, render_template, Response, request, Markup, flash, send_file
import requests
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
apikey = ''
reportUrl = 'https://www.virustotal.com/vtapi/v2/file/report'
scanUrl = 'https://www.virustotal.com/vtapi/v2/file/scan'
@app.route('/', methods = ['GET', 'POST'])
def uploader():
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
    return render_template("uploadVT.html")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug=True)
