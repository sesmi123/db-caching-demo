import pika

class RabbitMQ:
    def __init__(self, host, port, vhost, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, virtual_host=vhost))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name

    def publish_message(self, data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=data)

    def close_connection(self):
        self.connection.close()