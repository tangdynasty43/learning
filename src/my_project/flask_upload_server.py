#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask文件上传服务器演示
提供完整的文件上传功能，包括Web界面和API接口
"""

import os
from flask import Flask, request, render_template_string, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import mimetypes
from datetime import datetime

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_info(filepath):
    """获取文件信息"""
    if not os.path.exists(filepath):
        return None
    
    stat = os.stat(filepath)
    mime_type, _ = mimetypes.guess_type(filepath)
    
    return {
        'filename': os.path.basename(filepath),
        'size': stat.st_size,
        'mime_type': mime_type or 'unknown',
        'modified_time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    }

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文件上传演示</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-area {
            border: 2px dashed #ddd;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin-bottom: 20px;
            transition: border-color 0.3s;
        }
        .upload-area:hover {
            border-color: #007bff;
        }
        .upload-area.dragover {
            border-color: #007bff;
            background-color: #f8f9fa;
        }
        input[type="file"] {
            margin: 10px 0;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .progress {
            width: 100%;
            height: 20px;
            background-color: #f0f0f0;
            border-radius: 10px;
            margin: 10px 0;
            overflow: hidden;
            display: none;
        }
        .progress-bar {
            height: 100%;
            background-color: #007bff;
            width: 0%;
            transition: width 0.3s;
        }
        .file-list {
            margin-top: 20px;
        }
        .file-item {
            background: #f8f9fa;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📤 Python文件上传演示</h1>
        
        <div class="upload-area" id="uploadArea">
            <p>📁 拖拽文件到这里或点击选择文件</p>
            <input type="file" id="fileInput" multiple>
            <br><br>
            <button onclick="uploadFiles()">🚀 上传文件</button>
        </div>
        
        <div class="progress" id="progressContainer">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        
        <div id="messages"></div>
        
        <div class="file-list">
            <h3>📋 已上传的文件</h3>
            <div id="fileList">
                {% for file in files %}
                <div class="file-item">
                    <span>📄 {{ file.filename }} ({{ file.size }} 字节)</span>
                    <a href="/download/{{ file.filename }}" target="_blank">下载</a>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const progressContainer = document.getElementById('progressContainer');
        const progressBar = document.getElementById('progressBar');
        const messages = document.getElementById('messages');
        const fileList = document.getElementById('fileList');

        // 拖拽上传
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            fileInput.files = e.dataTransfer.files;
        });

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        function showMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = text;
            messages.appendChild(messageDiv);
            setTimeout(() => messageDiv.remove(), 5000);
        }

        function uploadFiles() {
            const files = fileInput.files;
            if (files.length === 0) {
                showMessage('请选择要上传的文件', 'error');
                return;
            }

            const formData = new FormData();
            for (let file of files) {
                formData.append('files', file);
            }

            progressContainer.style.display = 'block';
            progressBar.style.width = '0%';

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                progressBar.style.width = '100%';
                if (data.success) {
                    showMessage(`成功上传 ${data.uploaded_files.length} 个文件`, 'success');
                    location.reload(); // 刷新页面显示新文件
                } else {
                    showMessage(`上传失败: ${data.message}`, 'error');
                }
            })
            .catch(error => {
                showMessage(`上传错误: ${error.message}`, 'error');
            })
            .finally(() => {
                setTimeout(() => {
                    progressContainer.style.display = 'none';
                }, 1000);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """主页面"""
    # 获取已上传的文件列表
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_info = get_file_info(filepath)
                if file_info:
                    files.append(file_info)
    
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_files():
    """处理文件上传"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        uploaded_files = []
        errors = []
        
        for file in files:
            if file and file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # 避免文件名冲突
                    counter = 1
                    original_filename = filename
                    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                        name, ext = os.path.splitext(original_filename)
                        filename = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    file_info = get_file_info(filepath)
                    uploaded_files.append(file_info)
                else:
                    errors.append(f"文件 {file.filename} 类型不允许")
        
        if uploaded_files:
            message = f"成功上传 {len(uploaded_files)} 个文件"
            if errors:
                message += f"，{len(errors)} 个文件失败"
            return jsonify({
                'success': True,
                'message': message,
                'uploaded_files': uploaded_files,
                'errors': errors
            })
        else:
            return jsonify({
                'success': False,
                'message': '没有文件上传成功',
                'errors': errors
            })
            
    except RequestEntityTooLarge:
        return jsonify({'success': False, 'message': '文件太大，请选择小于16MB的文件'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'})

@app.route('/download/<filename>')
def download_file(filename):
    """下载文件"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': '文件不存在'}), 404

@app.route('/api/files')
def list_files():
    """API: 获取文件列表"""
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_info = get_file_info(filepath)
                if file_info:
                    files.append(file_info)
    
    return jsonify({'files': files})

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API: 文件上传接口"""
    return upload_files()

@app.errorhandler(413)
def too_large(e):
    return jsonify({'success': False, 'message': '文件太大，请选择小于16MB的文件'}), 413

if __name__ == '__main__':
    print("🚀 启动Flask文件上传服务器...")
    print(f"📁 上传目录: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"📏 最大文件大小: {MAX_FILE_SIZE // (1024*1024)}MB")
    print(f"📋 允许的文件类型: {', '.join(ALLOWED_EXTENSIONS)}")
    print("\n🌐 访问地址:")
    print("   主页面: http://localhost:5000")
    print("   API接口: http://localhost:5000/api/upload")
    print("   文件列表: http://localhost:5000/api/files")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)