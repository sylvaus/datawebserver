import atexit
from multiprocessing import Queue
from threading import Thread

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from data_server.data_dispatcher import DataDispatcher
from data_server.data_server import DataServer, ThreadedTCPRequestHandler
from data_server.rolling_data_base import RollingDataBase

HOST, PORT = "192.168.0.101", 8889

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisHasToBeChanged!'
socket_io = SocketIO(app)

database = RollingDataBase("./db", auto_save_s=0)
database.load()
data_queue = Queue()
data_server = DataServer((HOST, PORT), ThreadedTCPRequestHandler, data_queue=data_queue)


def dispatch_update(data):
    name = data[0]
    x_y = data[1]
    socket_io.emit("data_update", [name, x_y])
    database.add(name, x_y)


data_dispatcher = DataDispatcher(data_queue, dispatch_update)


@socket_io.on('request_initial_values')
def give_initial_params():
    emit("initial_values", database.get_all())


@app.route('/')
def hello_world():
    return render_template('index.html')


@atexit.register
def closing_resources():
    print("Closing resources")
    data_server.shutdown()
    data_dispatcher.stop()
    database.save()


if __name__ == '__main__':
    data_server_thread = Thread(target=data_server.serve_forever)
    data_server_thread.start()

    data_dispatcher_thread = Thread(target=data_dispatcher.run)
    data_dispatcher_thread.start()

    socket_io.run(app, host=HOST, port=5000)
