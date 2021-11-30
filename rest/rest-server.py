import os,sys,base64
import platform
from flask import Flask, request, Response
from flask_table import Table,Col
import pika,json,jsonpickle
from cassandra.cluster import Cluster

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
cassandraHost = os.getenv("CASSANDRA_HOST") or "host.docker.internal"

print("Connecting to rabbitmq({})".format(rabbitMQHost))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/srv/uploads/'
# app.config['UPLOAD_FOLDER'] = '/Users/ayu/Study/Courses/CSCI5253/TermProject/storage/'
# app.config['UPLOAD_FOLDER'] = './'

def toWorker(data):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='toWorker')
    rabbitMQChannel.basic_publish(exchange='',routing_key='toWorker', body=json.dumps(data))
    rabbitMQ.close()
def toLogs(message,key='info'):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
    key = f"{platform.node()}.rest.{key}"
    print("DEBUG:", message, file=sys.stdout)
    rabbitMQChannel.basic_publish(exchange='logs', routing_key=key, body=message)
    rabbitMQ.close()

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"



class songTable(Table):
    id = Col('Timestamp')
    name = Col('Name')
    filehash = Col('Hash')
@app.route('/songs')
def showAllSongs():
    try:
        cluster = Cluster([cassandraHost],port=9042)
        session = cluster.connect()
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS audioid
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}
        """)
        session.set_keyspace('audioid')
        table = songTable(session.execute(
            'SELECT * FROM songs'
            ).all())
        cluster.shutdown()
        return(table.__html__())
    except Exception as e:
        return f"<p>Something Wrong! {e}</p>"

class recogTable(Table):
    id =        Col('Timestamp')
    upload =    Col('Upload')
    match =     Col('Matched Name')
    confidence= Col('Confidence')
@app.route('/recogs')
def showAllRecogs():
    try:
        cluster = Cluster([cassandraHost],port=9042)
        session = cluster.connect()
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS audioid
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}
        """)
        session.set_keyspace('audioid')
        table = recogTable(session.execute(
            "SELECT * FROM recogs"
            ).all())
        cluster.shutdown()
        return(table.__html__())
    except Exception as e:
        return f"<p>Something Wrong! {e}</p>"




@app.route('/api/addNewSong', methods=['POST'])
def addNewSong():
    try:
        jsonIn = jsonpickle.decode(request.data)
        filepath = app.config['UPLOAD_FOLDER'] + jsonIn['filename']
        with open(filepath,'wb') as f:
            f.write(base64.b64decode(jsonIn['mp3'].encode()))
        body = {'cmd':'addNewSong','path':filepath}
        toWorker(body)
        toLogs(f"addNewSong: {jsonIn['filename']}")
        response = {'action':'queued'}
    except Exception as e:
        response = { 'addNewSong' : f'Something Wrong! {e}' }
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/recogFile', methods=['GET', 'POST'])
def recogFile():
    try:
        jsonIn = jsonpickle.decode(request.data)
        filepath = app.config['UPLOAD_FOLDER'] + jsonIn['filename']
        with open(filepath,'wb') as f:
            f.write(base64.b64decode(jsonIn['mp3'].encode()))
        body = {'cmd':'recogFile','path':filepath}
        toWorker(body)
        toLogs(f"recogFile: {jsonIn['filename']}")
        response = {'action':'queued'}
    except Exception as e:
        response = { 'recogFile' : f'Something Wrong! {e}' }
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/RESET', methods=['GET', 'POST'])
def reset():
    try:
        body = {'cmd':'reset'}
        toWorker(body)
        response = {'action':'queued'}
    except Exception as e:
        response = { 'reset' : f'Something Wrong! {e}' }
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# @app.route('/api/checkDB', methods=['GET', 'POST'])
# def checkDB():
#     try:
#         body = {'cmd':'checkDB'}
#         toWorker(body)
#         response = {'action':'queued'}
#     except Exception as e:
#         response = { 'checkDB' : f'Something Wrong! {e}' }
#     response_pickled = json.dumps(response)
#     return Response(response=response_pickled, status=200, mimetype="application/json")


app.run(host="0.0.0.0", port=5000)














