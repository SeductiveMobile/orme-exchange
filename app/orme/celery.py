from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

broker = "redis://%s:%s/0" % (os.environ["REDIS_HOST"], os.environ["REDIS_PORT"])
# app = Celery('orme', broker=broker, include=['orme.tasks'])
app = Celery('orme', broker=broker)

if __name__ == '__main__':
    app.start()
