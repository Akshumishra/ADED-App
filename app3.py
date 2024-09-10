from flask import Flask, render_template, request, redirect, url_for, send_file
from stegano import lsb
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['DOWNLOAD_FOLDER'] = 'static/downloads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return render_template('index.html', uploaded_image=file.filename)

@app.route('/hide', methods=['POST'])
def hide_data():
    message = request.form['message']
    image_file = request.form['image_file']
    
    if message and image_file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'hidden.png')
        
        secret_image = lsb.hide(input_path, message)
        secret_image.save(output_path)
        
        return render_template('index.html', uploaded_image=image_file, hidden_image='hidden.png')
    
    return redirect(url_for('index'))

@app.route('/reveal', methods=['POST'])
def reveal_data():
    image_file = request.form['image_file']
    
    if image_file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
        hidden_message = lsb.reveal(input_path)
        
        return render_template('index.html', uploaded_image=image_file, revealed_message=hidden_message)
    
    return redirect(url_for('index'))

@app.route('/download')
def download_image():
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'hidden.png')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
