import os
from time import sleep

from celery import Celery

client = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL'))

from . import test

@client.task
def reverse(string):
    sleep(5)
    return string[::-1]
