from flask import Flask, request, render_template

import sys
import os

app = Flask(__name__)
port = int(sys.argv[1])

if not os.path.exists('../uploads'):
    os.makedirs('../uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('../uploads/'+file.filename)
    return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,)