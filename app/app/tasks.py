import os

import services
from celery import Celery

broker = "redis://%s:%s/0" % (os.environ["REDIS_HOST"], os.environ["REDIS_PORT"])
app = Celery('tasks', broker=broker)


# TODO: Implement periodic tasks scheduling http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

@app.task
def check_orv_wallets(arg):
    return services.ORVService.check_for_updates()


@app.task
def check_user_wallets(arg):
    return services.UserWalletsService.check_for_updates()


@app.task
def sync_orv_wallet(address):
    service = services.ORVService(address)
    return service.sync()


@app.task
def sync_user_wallet(address):
    service = services.UserWalletsService(address)
    return service.sync()
