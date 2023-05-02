from flask import Flask, request, render_template, send_from_directory
import sys
import os

FTP_DIR_NAME = "shared"

app = Flask(__name__)
port = int(sys.argv[1])

if not os.path.exists(f'../{FTP_DIR_NAME}'):
    os.makedirs(f'../{FTP_DIR_NAME}')



# @app.route('/<path:path>')
# def sendFile(path):
#     root_dir = os.getcwd()
#     

def serveFile(path):
    base_dir_pair = os.path.split(path)
    return send_from_directory(directory= base_dir_pair[0], path=base_dir_pair[1], as_attachment=True)

def serveDirectory(path): 
    dir_contents = os.listdir(path)
    return '<br>'.join(dir_contents)

@app.route('/<path:path>')
def serve_directory(path):
    root_dir = os.getcwd()
    dir_path = os.path.join(root_dir, '..', FTP_DIR_NAME , path)
    
    if os.path.isfile(dir_path):
        return serveFile(dir_path)
    
    elif os.path.isdir(dir_path):
        return serveDirectory(dir_path)
    


@app.route('/')
def index():
    return serve_directory('')

@app.route('/upload')
def upload():
    return render_template('index.html')

@app.route('/shared/upload', methods=['POST'])
def uploadHandler():
    file = request.files['file']
    file.save(f'../{FTP_DIR_NAME}/'+file.filename)
    return 'File uploaded successfully!'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,)