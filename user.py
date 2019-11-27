from flask import Flask, render_template, Response, request, Markup, flash
from camera import VideoCamera
import socket
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
serverIP = socket.gethostbyname(socket.gethostname())
def gen(VideoCamera):
    while True:
        frame = VideoCamera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/streaming')
def streaming():
    return render_template('streaming.html')
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename("./" + f.filename))
        return render_template('uploadResults.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host=serverIP, port="80")
