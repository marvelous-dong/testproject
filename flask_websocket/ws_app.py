from flask import Flask, request
from flask_cors import CORS
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer


app = Flask(__name__)
CORS(app, supports_credentials=True)
socket_dict = {}


@app.route("/ws/<username>")
def ws(username):
    sock = request.environ.get("wsgi.websocket")

    if not sock:
        return "请使用websocket"

    socket_dict[username] = sock

    while 1:
        msg = sock.receive()

        for i in socket_dict:
            rece_sock = socket_dict[i]
            rece_sock.send(msg)


if __name__ == '__main__':
    http_serv = WSGIServer(("127.0.0.1", 9528), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
