import atexit
import configparser
import socket
from multiprocessing import Queue
from threading import Thread

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from data_server.data_dispatcher import DataDispatcher
from data_server.data_server import DataServer, ThreadedTCPRequestHandler
from data_server.rolling_data_base import RollingDataBase

config = configparser.ConfigParser()
config.read("app.ini")

app = Flask(__name__)
app.config['SECRET_KEY'] = config.get("server.graphs", "secret_key")
socket_io = SocketIO(app)

# Configuring and loading database
database = RollingDataBase(config.get("database", "db_folder"),
                           auto_save_s=config.getint("database", "auto_save_s"))
database.load()

# Configuring DataServer
if config.getboolean("server.data", "auto_host"):
    data_server_host = socket.gethostbyname(socket.gethostname())
else:
    data_server_host = config.getboolean("server.data", "host")
data_server_port = config.getint("server.data", "port")
data_queue = Queue()
data_server = DataServer((data_server_host, data_server_port),
                         ThreadedTCPRequestHandler,
                         data_queue=data_queue)


def dispatch_update(data):
    name, x_y = data
    socket_io.emit("data_update", [name, x_y])
    database.add(name, x_y)


data_dispatcher = DataDispatcher(data_queue, dispatch_update)


@socket_io.on('request_initial_values')
def give_initial_params():
    emit("initial_values", database.get_all())


@app.route('/')
def main_page():
    return render_template('index.html')


@atexit.register
def closing_resources():
    print("Closing resources")
    data_server.shutdown()
    data_dispatcher.stop()
    database.stop_auto_save()
    database.save()


if __name__ == '__main__':
    data_server_thread = Thread(target=data_server.serve_forever)
    data_server_thread.start()

    data_dispatcher_thread = Thread(target=data_dispatcher.run)
    data_dispatcher_thread.start()

    if config.getboolean("server.graphs", "auto_host"):
        graph_server_host = socket.gethostbyname(socket.gethostname())
    else:
        graph_server_host = config.getboolean("server.graphs", "host")
    graph_server_port = config.getint("server.graphs", "port")
    socket_io.run(app, host=graph_server_host, port=graph_server_port)
