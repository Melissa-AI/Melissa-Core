from flask import Flask, render_template
from flask_socketio import SocketIO

# Melissa
from melissa.profile_loader import load_profile
from melissa.tts import tts
from melissa.brain import query

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def hello():
    return render_template('index.html')


@socketio.on('user speaks')
def handle_json(json):
    speech_text = json['data']
    print('Melissa thinks you said: ' + speech_text)

    # emit('melissa replies', 'thank you')

    if speech_text is None:
        pass
    else:
        query(speech_text)


def main():
    data = load_profile(True)
    tts('Welcome ' + data['name'] + ', how can I help you?')
    socketio.run(app)


if __name__ == '__main__':
    main()
