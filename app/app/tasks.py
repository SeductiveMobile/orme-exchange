from .celery import app
from .services import ORVService, UserWalletsService


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """ Periodic tasks via Celery Beat
    See examples at http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

    :param sender: internally used param
    :param kwargs: not used
    :return: None
    """
    # Calls check_orv_wallets() every 600 seconds.
    sender.add_periodic_task(600.0, check_orv_wallets.s('no argument'), name='add every 10 minutes')

    # Calls check_user_wallets() every 600 seconds.
    sender.add_periodic_task(600.0, check_user_wallets.s('no argument'), name='add every 10 minutes')


@app.task
def check_orv_wallets(arg):
    # print('check_orv_wallets')
    return ORVService.check_for_updates()


@app.task
def check_user_wallets(arg):
    # print('check_user_wallets')
    return UserWalletsService.check_for_updates()


@app.task
def sync_orv_wallet(address):
    # print('sync_orv_wallet')
    service = ORVService(address)
    return service.sync()


@app.task
def sync_user_wallet(address):
    # print('sync_user_wallet')
    service = UserWalletsService(address)
    return service.sync()
