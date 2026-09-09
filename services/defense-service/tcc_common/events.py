import json, os, threading
import pika

EXCHANGE=os.getenv("RABBITMQ_EXCHANGE","tcc.events")

def publish(event_type, payload):
    url=os.getenv("RABBITMQ_URL","amqp://tcc:tcc@localhost:5672/%2F")
    conn=pika.BlockingConnection(pika.URLParameters(url))
    ch=conn.channel(); ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    body=json.dumps({"type":event_type,"payload":payload})
    ch.basic_publish(exchange=EXCHANGE,routing_key=event_type,body=body,properties=pika.BasicProperties(delivery_mode=2,content_type="application/json"))
    conn.close()

def consume(queue, binding_keys, callback):
    url=os.getenv("RABBITMQ_URL","amqp://tcc:tcc@localhost:5672/%2F")
    conn=pika.BlockingConnection(pika.URLParameters(url)); ch=conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    ch.queue_declare(queue=queue,durable=True)
    for key in binding_keys: ch.queue_bind(exchange=EXCHANGE,queue=queue,routing_key=key)
    def handler(ch, method, props, body):
        try:
            callback(json.loads(body))
            ch.basic_ack(method.delivery_tag)
        except Exception as exc:
            print("event error:",exc,flush=True); ch.basic_nack(method.delivery_tag,requeue=False)
    ch.basic_qos(prefetch_count=10); ch.basic_consume(queue=queue,on_message_callback=handler)
    ch.start_consuming()
