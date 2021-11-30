import os
from flask import Flask, flash, request, redirect, url_for
# from werkzeug.utils import secure_filename
import pika,json

app = Flask(__name__)
app.config['STORAGE_TYPE'] = 'k8s' # k8s or local
app.config['UPLOAD_FOLDER_K8S'] = '/srv/uploads/'
app.config['UPLOAD_FOLDER_LOCAL'] = '/Users/ayu/Study/Courses/CSCI5253/TermProject/storage/'

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
# rabbitMQHost = "host.docker.internal"

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3'}

def toRabbitMQ(data):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='toWorker')
    # rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
    rabbitMQChannel.basic_publish(exchange='',routing_key='toWorker', body=json.dumps(data))
    rabbitMQ.close()

def saveSong(file):
    if app.config['STORAGE_TYPE'] == 'local':
        dirPath = app.config['UPLOAD_FOLDER_LOCAL']
        file.save(os.path.join(dirPath, file.filename))
        return os.path.join(dirPath, file.filename)
    elif app.config['STORAGE_TYPE'] == 'k8s':
        dirPath = app.config['UPLOAD_FOLDER_K8S']
        # os.makedirs(dirPath,exist_ok=True)
        file.save(os.path.join(dirPath, file.filename))
        return os.path.join(dirPath, file.filename)
    else:
        raise ValueError('Wrong storage type!')

@app.route('/', methods=['GET', 'POST'])
def addNewSong():
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
            body = {'storageType':app.config['STORAGE_TYPE'],'path':saveSong(file)}
            toRabbitMQ(body)
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

app.run(host="0.0.0.0", port=5000)