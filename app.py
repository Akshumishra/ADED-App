from flask import Flask, request, jsonify, render_template
import base64
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    button_clicked = request.form['button_clicked']
    if button_clicked == 'button1':
        # Execute encryption and decryption program
        action = request.form['action']
        message = request.form['message']
        password = request.form['password']
        if action == 'encrypt':
            result = encrypt_program(message, password)
        elif action == 'decrypt':
            result = decrypt_program(message, password)
        return render_template('result.html', result=result)
    
    elif button_clicked == 'button2':
        # Execute image encryption and decryption program
            result = image_encrypt_decrypt_program(request.form['message'], request.form['password'])
    elif button_clicked == 'button3':
        # Execute file transfer program
        result = file_transfer_program(request.form['message'], request.form['password'])
    elif button_clicked == 'button4':
        # Execute password manager program
        result = password_manager_program(request.form['message'], request.form['password'])
    return jsonify({'result': result})

def encrypt_program(message, password):
    if password:
        message_bytes = message.encode("ascii")
        message_bytes = bytearray(message_bytes)
        for i in range(len(message_bytes)):
            message_bytes[i] ^= ord(password[i % len(password)])
        base64_bytes = base64.b64encode(message_bytes)
        encrypt = base64_bytes.decode("ascii")
        return encrypt
    else:
        return "Error: Password is required"

def decrypt_program(message, password):
    if password:
        base64_bytes = message.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        message_bytes = bytearray(message_bytes)
        for i in range(len(message_bytes)):
            message_bytes[i] ^= ord(password[i % len(password)])
        decrypt = message_bytes.decode("ascii")
        return decrypt
    else:
        return "Error: Password is required"
        
def encrypt_decrypt_program(action, message, password):
    if action == 'encrypt':
        encrypt()
    # Implement encryption and decryption logic here
    return 'Encryption and decryption result'

def image_encrypt_decrypt_program(message, password):
    # Implement image encryption and decryption logic here
    return 'Image encryption and decryption result'

def file_transfer_program(message, password):
    # Implement file transfer logic here
    return 'File transfer result'

def password_manager_program(message, password):
    # Implement password manager logic here
    return 'Password manager result'

if __name__ == '__main__':
    app.run(debug=True)