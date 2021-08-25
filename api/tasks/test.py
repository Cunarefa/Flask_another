from time import sleep

from api.tasks import client


@client.task
def test_task(a, b):
    sleep(4)
    print('It is working!')
    return a + b
