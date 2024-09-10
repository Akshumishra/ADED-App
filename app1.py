from flask import Flask, render_template, request
from stegano import lsb

app = Flask(__name__)

@app.route('/image-encryption-decryption', methods=['GET', 'POST'])
def image_encryption_decryption():
    if request.method == 'POST':
        # Get input from GUI
        image_file = request.form['image_file']
        message = request.form['message']

        # Encrypt or decrypt the message
        if request.form['action'] == 'encrypt':
            encrypted_image = lsb.hide(image_file, message)
            return render_template('image_encryption_decryption.html', result='Encrypted image saved as hidden.png')
        elif request.form['action'] == 'decrypt':
            decrypted_message = lsb.reveal(image_file)
            return render_template('image_encryption_decryption.html', result=decrypted_message)

    return render_template('image_encryption_decryption.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # run the app on localhost:5000