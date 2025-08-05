from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
app.config['AUDIO_FOLDER'] = 'audio'

if not os.path.exists(app.config['AUDIO_FOLDER']):
    os.makedirs(app.config['AUDIO_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    if request.method == 'POST':
        text = request.form.get('text')
        lang = request.form.get('lang')
        speed = request.form.get('speed')
        gender = request.form.get('gender')   # Not used by gTTS

        if text:
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(app.config['AUDIO_FOLDER'], filename)
            tts = gTTS(text=text, lang=lang, slow=True if speed == 'slow' else False)
            tts.save(filepath)
            audio_file = filename

    return render_template('index.html', audio_file=audio_file)

@app.route('/audio/<filename>')
def get_audio(filename):
    filepath = os.path.join(app.config['AUDIO_FOLDER'], filename)
    return send_file(filepath, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
