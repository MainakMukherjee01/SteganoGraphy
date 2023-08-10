import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from stegano import lsb
import uuid

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form:
        return "Error: No image or message provided."

    image = request.files['image']
    message = request.form['message']
    
    if image.filename == '' or not allowed_file(image.filename):
        return "Error: Invalid image file."
    
    filename = secure_filename(image.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(upload_path)
    
    try:
        encoded_image = lsb.hide(upload_path, message)
        encoded_filename = 'encoded.png'
        encoded_path = os.path.join(app.config['UPLOAD_FOLDER'], encoded_filename)
        encoded_image.save(encoded_path)
        return render_template('encode.html', encoded_image=encoded_filename)
    except Exception as e:
        return f"Error during encoding: {str(e)}"


@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return "Error: No image provided."

    image = request.files['image']
    
    if image.filename == '' or not allowed_file(image.filename):
        return "Error: Invalid image file."
    
    filename = secure_filename(image.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(upload_path)
    
    try:
        decoded_message = lsb.reveal(upload_path)
        return render_template('decode.html', decoded_message=decoded_message)
    except Exception as e:
        return f"Error during decoding: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
