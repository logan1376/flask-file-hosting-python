from flask import Flask, render_template, request, jsonify, send_file, redirect
import os
import uuid 
import datetime
import json

app = Flask(__name__)

# Set server port here
SERVER_PORT = 8080
# Note: If ip is numbers remove '' if its letters add ''
SERVER_IP = 'localhost'
UPLOAD_FOLDER = 'videos'
UPLOAD_IMAGE_FOLDER = 'images'
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

# Update videos.json function
def update_videos_array():
    videos = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        video_info = {
            'filename': file,
            'path': os.path.join(app.config['UPLOAD_FOLDER'], file),
        }
        videos.append(video_info)

    with open('videos.json', 'w') as json_file:
        json.dump(videos, json_file)
# Update images.json function
def update_image_array():
    images = []
    for file in os.listdir(app.config['UPLOAD_IMAGE_FOLDER']):
        image_info = {
            'filename': file,
            'path': os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], file),
        }
        images.append(image_info)

    with open('images.json', 'w') as json_file:
        json.dump(images, json_file)

# Video upload page and saving (Updates videos.json)
@app.route('/uploadvideo', methods=['GET', 'POST'])
def upload_video_page():
    if request.method == 'POST':
        if 'video' not in request.files:
            return jsonify({'error': 'No video part'})
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No selected video file'})
        if file and allowed_video_file(file.filename):
            random_string = str(uuid.uuid4())
            file_name, file_extension = os.path.splitext(file.filename)
            new_filename = f"{file_name}_{random_string}{file_extension}"
            filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(filename)
            update_videos_array()
            return redirect("/")
        return jsonify({'error': 'Invalid file format'})
    return render_template('uploadvideo.html')

# Image upload page and saving (Updates images.json)
@app.route('/uploadimage', methods=['GET', 'POST'])
def upload_image_page():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image part'})
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected image file'})
        if file and allowed_image_file(file.filename):
            random_string = str(uuid.uuid4())
            file_name, file_extension = os.path.splitext(file.filename)
            new_filename = f"{file_name}_{random_string}{file_extension}"
            filename = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], new_filename)
            file.save(filename)
            update_image_array()
            return redirect("/")
        return jsonify({'error': 'Invalid file format'})
    return render_template('uploadimage.html')

# Video list from videos.json
@app.route('/videos')
def get_videos():
    with open('videos.json', 'r') as json_file:
        videos = json.load(json_file)

    video_list = ''.join([f"<li><a href='/video/{video['filename']}' target='_blank'>{video['filename']}</a></li>" for video in videos])
    return f"<ul>{video_list}</ul>"

# Video list from videos.json
@app.route('/image')
def get_image():
    with open('images.json', 'r') as json_file:
        images = json.load(json_file)

    image_list = ''.join([f"<li><a href='/image/{image['filename']}' target='_blank'>{image['filename']}</a></li>" for image in images])
    return f"<ul>{image_list}</ul>"

# Send video to user
@app.route('/video/<filename>')
def serve_video(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# Send image to user
@app.route('/image/<filename>')
def serve_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))

# Show lists of files
@app.route('/')
def videos_page():
    with open('videos.json', 'r') as videos_file:
        videos = json.load(videos_file)
    with open('images.json', 'r') as images_file:
        images = json.load(images_file)

    return render_template('videos.html', videos=videos, images=images)

# Info page
@app.route('/info')
def info():
    return render_template('info.html')

# Start server and update json files
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    elif not os.path.exists(app.config['UPLOAD_IMAGE_FOLDER']):
        os.makedirs(app.config['UPLOAD_IMAGE_FOLDER'])
    update_videos_array()
    update_image_array()
    app.run(port=SERVER_PORT, host=SERVER_IP)
