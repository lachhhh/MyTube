import os
import secrets
from flask import Flask, render_template, request, redirect, url_for
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)

@app.route('/')
def index():
    videos = []
    with open('videos.txt', 'r') as file:
        for line in file:
            filename, thumbnail = line.strip().split(',')
            videos.append({
                'filename': filename,
                'thumbnail': thumbnail
            })
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return redirect(request.url)

    video_file = request.files['video']
    if video_file.filename == '':
        return redirect(request.url)

    filename = secrets.token_hex(8) + '.mp4'
    video_path = os.path.join('static', 'videos', filename)
    video_file.save(video_path)

    clip = VideoFileClip(video_path)
    thumbnail_path = os.path.join('static', 'thumbnails', filename.replace('.mp4', '.jpg'))
    clip.save_frame(thumbnail_path, t=0.1)
    clip.close()

    with open('videos.txt', 'a') as file:
        file.write(f'{filename},{os.path.basename(thumbnail_path)}\n')

    return redirect(url_for('index'))

@app.route('/play/<filename>')
def play(filename):
    return render_template('play.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
