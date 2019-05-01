from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

@app.task
def add(x, y):
    for i in range(200000000):
        x +=y
        y+=1
    return x + y

add.delay(4,4)