from kombu import Connection
from kombu.mixins import ConsumerMixin
from kombu.common import Broadcast
from config import redis_url

class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        print('Got message: {0}'.format(body))
        message.ack()

task_queue_bcast = Broadcast('broadcast_tasks')
with Connection(redis_url) as conn:
    worker = Worker(conn, [task_queue_bcast,])
    worker.run()
