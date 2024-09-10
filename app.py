#Message Encryption and decryption
from flask import Flask, render_template, request
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index1():
    if request.method == 'POST':
        if request.form['action'] == 'Encrypt':
            password = request.form['password']
            message = request.form['message']
            encrypted_message = encrypt(password, message)
            return render_template('index1.html', encrypted_message=encrypted_message, password='', message='')
        elif request.form['action'] == 'Decrypt':
            password = request.form['password']
            message = request.form['message']
            decrypted_message = decrypt(password, message)
            return render_template('index1.html', decrypted_message=decrypted_message, password='', message='')
        elif request.form['action'] == 'Reset':
            return render_template('index1.html', password='', message='')
    return render_template('index1.html', password='', message='')

def encrypt(password, message):
    message_bytes = message.encode("ascii")
    message_bytes = bytearray(message_bytes)
    for i in range(len(message_bytes)):
        message_bytes[i] ^= ord(password[i % len(password)])
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode("ascii")

def decrypt(password, message):
    try:
        decode_message = base64.b64decode(message.encode("ascii"))
        decode_message = bytearray(decode_message)
        for i in range(len(decode_message)):
            decode_message[i] ^= ord(password[i % len(password)])
        return decode_message.decode("ascii")
    except:
        return "Invalid message or password"

if __name__ == '__main__':
    app.run(debug=True)