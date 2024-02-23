from celery import Celery
from celery.utils.log import get_task_logger
from kombu.common import Broadcast
from config import redis_url


app = Celery('tasks', broker=redis_url)

# 这种方式测试下来不行
# 只能用于任务发送端
broadcast_tasks_queue = Broadcast('broadcast_tasks', routing_key='celery')
app.conf.task_routes = {
    'tasks.broadcast_fn': {
        'queue': broadcast_tasks_queue,
        # 如果只用于任务发送端，则下面的 exchange 和 routing_key 可以直接注释
        'exchange': broadcast_tasks_queue.exchange,
        'routing_key': broadcast_tasks_queue.routing_key
    }
}
app.conf.worker_pool = 'solo'
app.conf.worker_concurrency = 1

with app.producer_or_acquire() as p:
    broadcast_tasks_queue.declare(channel=p.channel)


logger = get_task_logger(__name__)


@app.task(name='tasks.broadcast_fn')
def broadcast_fn():
    logger.info('call broadcast_fn')

if __name__ == '__main__':
    worker = app.Worker()
    worker.start()