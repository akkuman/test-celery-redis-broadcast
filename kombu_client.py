from kombu import Connection, Producer, Exchange
from kombu.common import Broadcast
from config import redis_url
import time

task_queue_bcast = Broadcast('broadcast_tasks', exchange=Exchange('broadcast_tasks', type='fanout'), routing_key='celery')
task_queue_bcast = Broadcast('broadcast_tasks')

with Connection(redis_url) as conn:
    with conn.channel() as channel:
        producer = Producer(channel)
        exchange = Exchange('name', type='direct')
        producer.publish(
            {'hello': 'world'},
            retry=True,
            exchange=task_queue_bcast.exchange,
            routing_key=task_queue_bcast.routing_key,
            declare=[task_queue_bcast],
        )
        time.sleep(100)