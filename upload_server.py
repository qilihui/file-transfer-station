
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        ctime = datetime.fromtimestamp(os.path.getctime(filepath))
        size = os.path.getsize(filepath)  # 获取文件大小(字节)
        # 转换为更友好的格式(KB/MB)
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.2f} KB"
        else:
            size_str = f"{size/(1024*1024):.2f} MB"
        files.append({
            'name': filename,
            'upload_time': ctime.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': ctime.timestamp(),
            'size': size_str,
            'raw_size': size
        })
    # 按上传时间降序排序
    files.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
