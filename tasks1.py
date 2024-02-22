from celery import Celery
from celery.utils.log import get_task_logger
from kombu.common import Broadcast
from config import redis_url


app = Celery('tasks', broker=redis_url)

# 这种方式测试下来不行
# 只能用于任务发送端
broadcast_tasks_queue = Broadcast('broadcast_tasks')
app.conf.task_routes = {
    'tasks.broadcast_fn': {
        'queue': broadcast_tasks_queue,
        'exchange': broadcast_tasks_queue.exchange,
        'routing_key': 'celery'
    }
}
app.conf.worker_pool = 'solo'
app.conf.worker_concurrency = 1


logger = get_task_logger(__name__)


@app.task(name='tasks.broadcast_fn')
def broadcast_fn():
    logger.info('call broadcast_fn')

if __name__ == '__main__':
    worker = app.Worker()
    worker.start()