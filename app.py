from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from collections import defaultdict
import json

app = Flask(__name__)
socketio = SocketIO()

socketio.init_app(app, cors_allowed_origin='*')

message_storage = defaultdict(list)

@socketio.on('connect')
def handle_connect():
    print('Client Connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')
    
@socketio.on('message')
def handle_message(message):
    if isinstance(message, str):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            print('Received invalid JSON string')
            return
    # print(f'Message Received: {message}')
    # socketio.emit('message', message)
    user = message.get('user')
    text = message.get('text')
    
    if user and text:
        message_storage[user].append(text)
        print(f'Message Storage: {dict(message_storage)}')
        emit('message', message, broadcast=True)
    else:
        print('Invalid message format')

        
@app.route("/")
def home():
    return render_template('base.html')
    

if __name__ == '__main__':
    
    app.debug = True
    socketio.run(app)