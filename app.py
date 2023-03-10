from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    img_bytes = file.read()
    img = np.array(Image.open(io.BytesIO(img_bytes)))
    enhanced_img = enhance_image(img)
    original_url = save_image(img)
    enhanced_url = save_image(enhanced_img)
    return jsonify({'original': original_url, 'enhanced': enhanced_url})

def enhance_image(img):
    # Add the code to enhance the image here
    enhanced_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return enhanced_img

def save_image(img):
    filename = 'image.png'
    cv2.imwrite(filename, img)
    with open(filename, 'rb') as f:
        img_bytes = f.read()
    return f'data:image/png;base64,{img_bytes.encode("base64").decode()}'

if __name__ == '__main__':
    app.run()