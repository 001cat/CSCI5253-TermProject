import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pika

UPLOAD_FOLDER = '/Users/ayu/Study/Courses/CSCI5253/TermProject/webFrontend/tmp/'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def toRabbitMQ(body):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='toWorker')
    # rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
    rabbitMQChannel.basic_publish(exchange='',routing_key='toWorker', body=body)
    rabbitMQ.close()

@app.route('/', methods=['GET', 'POST'])
def addNewSongs():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(len(request.data))
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename #secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            toRabbitMQ({'directory':app.config['UPLOAD_FOLDER'],'filename':filename})
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

