import sys
import os
from urllib.parse import quote, unquote
from flask import Flask, request, render_template, send_from_directory

FTP_DIR_NAME = "shared"

app = Flask(__name__)
port = int(sys.argv[1])

if not os.path.exists(f'../{FTP_DIR_NAME}'):
    os.makedirs(f'../{FTP_DIR_NAME}')


def urlEncode(url):
    return quote(url)
    

print(urlEncode("hello World"))
def serveFile(path):
    base_dir_pair = os.path.split(path)
    return send_from_directory(directory= base_dir_pair[0], path=base_dir_pair[1], as_attachment=True)

def format_file_size(size):
    # Determine the appropriate suffix and scaling factor
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    scaling_factor = 1024
    suffix_index = 0
    while size > scaling_factor and suffix_index < len(suffixes) - 1:
        suffix_index += 1
        size /= scaling_factor
    
    # Format the size string with the appropriate suffix
    size_string = "{:.2f}{}".format(size, suffixes[suffix_index])
    return size_string

def serveDirectory(path, root_path, hasPrev = False, ): 
    dir_contents = os.listdir(path)

    content_list = []

    

    if(hasPrev): 
        prevDir = os.path.dirname(root_path)
        prevDir =   urlEncode(prevDir) if prevDir != '' else "/"

        content_list.append({
                "name": "../",
                "url": prevDir,
            })

    for item in dir_contents:
        item_path = os.path.join(path, item)
        print(root_path)
        content = {
                "name": item,
                "url": urlEncode( os.path.join(unquote(root_path) , item)),
        }
        
        if os.path.isfile(item_path):
            content["type"] = "file"
            content["size"] = format_file_size(os.path.getsize(item_path))
        elif os.path.isdir(item_path):
            content["type"] = "directory"
            content["name"] = item
        
        content_list.append(content)
    
    return render_template('index.html', content_list = content_list)

@app.route('/<path:path>')
def serve_directory(path):
    print(path)
    root_dir = os.getcwd()
    dir_path = os.path.join(root_dir, '..', FTP_DIR_NAME , path)
    
    if os.path.isfile(dir_path):
        return serveFile(dir_path)
    
    elif os.path.isdir(dir_path):
        return serveDirectory(dir_path, hasPrev= path!='', root_path=path)
    


@app.route('/')
def index():
    return serve_directory('')

@app.route('/upload')
def upload():
    return render_template('upload-form.html')

@app.route('/shared/upload', methods=['POST'])
def uploadHandler():
    file = request.files['file']
    file.save(f'../{FTP_DIR_NAME}/'+file.filename)
    return 'File uploaded successfully!'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,)