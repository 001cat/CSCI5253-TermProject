import os,sys
import json,pika

def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode())
    except:
        data = body.decode()
    print(data)
    
    filepath = os.path.join(data['directory'],data['filename'])
    
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    sys.stdout.flush()
    sys.stderr.flush()

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toWorker')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toWorker', on_message_callback=callback)
rabbitMQChannel.start_consuming()