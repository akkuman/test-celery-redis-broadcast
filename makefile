server:
	.venv/bin/python3 -m celery -A tasks worker --loglevel=INFO -P threads -Q broadcast_tasks
client:
	.venv/bin/python3 client.py
