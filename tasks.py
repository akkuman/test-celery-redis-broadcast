from celery import Celery
# from celery.utils.log import get_task_logger
from kombu.common import Broadcast, Exchange
from config import redis_url


app = Celery('tasks', broker=redis_url)

# task_queues 此处必须要定义
app.conf.task_queues = (Broadcast('broadcast_tasks', exchange=Exchange('broadcast_tasks', type='fanout'), routing_key='celery'),)
app.conf.task_routes = {
    'tasks.broadcast_fn': {
        'queue': 'broadcast_tasks',
        'exchange': 'broadcast_tasks',
        # 'exchange': Exchange('broadcast_tasks', type='fanout'),
        'routing_key': 'celery'
    }
}
app.conf.worker_pool = 'solo'
app.conf.worker_concurrency = 2
# app.conf.broker_transport_options = {'supports_fanout': True}


# logger = get_task_logger(__name__)


@app.task(name='tasks.broadcast_fn')
def broadcast_fn():
    print('call broadcast_fn')

if __name__ == '__main__':
    worker = app.Worker()
    worker.start()