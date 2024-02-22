import os

redis_url = os.getenv('REDIS_URL') or 'redis://127.0.0.1:6379/0'
