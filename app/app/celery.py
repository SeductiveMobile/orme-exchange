import os

from celery import Celery

broker = "redis://%s:%s/0" % (os.environ["REDIS_HOST"], os.environ["REDIS_PORT"])
app = Celery('app', broker=broker, include=['app.tasks'])

if __name__ == '__main__':
    app.start()
