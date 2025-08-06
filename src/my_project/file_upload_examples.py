"""Python文件上传完整示例
这个文件展示了多种Python文件上传的实现方式，包括：
1. 使用requests库上传文件到服务器
2. Flask框架接收文件上传
3. Django框架处理文件上传
4. 文件上传的安全性和最佳实践
"""

import os
import requests
from pathlib import Path
import mimetypes
from datetime import datetime

# ==================== 1. 使用requests库上传文件 ====================

def upload_file_with_requests(file_path, upload_url, field_name='file'):
    """使用requests库上传文件到服务器
    
    Args:
        file_path (str): 要上传的文件路径
        upload_url (str): 上传接口URL
        field_name (str): 文件字段名，默认为'file'
    
    Returns:
        dict: 上传结果
    """
    if not os.path.exists(file_path):
        return {'success': False, 'error': '文件不存在'}
    
    try:
        # 打开文件
        with open(file_path, 'rb') as file:
            # 准备文件数据
            files = {field_name: file}
            
            # 可选：添加额外的表单数据
            data = {
                'description': '通过Python上传的文件',
                'upload_time': datetime.now().isoformat()
            }
            
            # 发送POST请求上传文件
            response = requests.post(upload_url, files=files, data=data)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': '文件上传成功',
                    'response': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            else:
                return {
                    'success': False,
                    'error': f'上传失败，状态码: {response.status_code}',
                    'response': response.text
                }
                
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'网络错误: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'上传异常: {str(e)}'}

def upload_multiple_files(file_paths, upload_url):
    """上传多个文件
    
    Args:
        file_paths (list): 文件路径列表
        upload_url (str): 上传接口URL
    
    Returns:
        dict: 上传结果
    """
    try:
        files = []
        for i, file_path in enumerate(file_paths):
            if os.path.exists(file_path):
                files.append(('files', open(file_path, 'rb')))
        
        if not files:
            return {'success': False, 'error': '没有有效的文件'}
        
        response = requests.post(upload_url, files=files)
        
        # 关闭文件
        for _, file_obj in files:
            file_obj.close()
        
        if response.status_code == 200:
            return {
                'success': True,
                'message': f'成功上传 {len(files)} 个文件',
                'response': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        else:
            return {
                'success': False,
                'error': f'上传失败，状态码: {response.status_code}'
            }
            
    except Exception as e:
        return {'success': False, 'error': f'上传异常: {str(e)}'}

def upload_with_progress(file_path, upload_url):
    """带进度显示的文件上传
    
    Args:
        file_path (str): 文件路径
        upload_url (str): 上传URL
    """
    if not os.path.exists(file_path):
        print("文件不存在")
        return
    
    file_size = os.path.getsize(file_path)
    print(f"开始上传文件: {file_path}")
    print(f"文件大小: {file_size / 1024 / 1024:.2f} MB")
    
    try:
        with open(file_path, 'rb') as file:
            # 创建一个包装器来跟踪上传进度
            class ProgressFile:
                def __init__(self, file_obj):
                    self.file_obj = file_obj
                    self.uploaded = 0
                
                def read(self, size):
                    data = self.file_obj.read(size)
                    self.uploaded += len(data)
                    progress = (self.uploaded / file_size) * 100
                    print(f"\r上传进度: {progress:.1f}%", end='', flush=True)
                    return data
                
                def __getattr__(self, name):
                    return getattr(self.file_obj, name)
            
            progress_file = ProgressFile(file)
            files = {'file': progress_file}
            
            response = requests.post(upload_url, files=files)
            print(f"\n上传完成，状态码: {response.status_code}")
            
            return response
            
    except Exception as e:
        print(f"\n上传失败: {str(e)}")
        return None

# ==================== 2. Flask框架接收文件上传 ====================

def create_flask_upload_server():
    """创建Flask文件上传服务器示例"""
    flask_code = '''
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制文件大小为16MB

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理单个文件上传"""
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有文件'}), 400
        
        file = request.files['file']
        
        # 检查文件名
        if file.filename == '':
            return jsonify({'success': False, 'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            # 确保上传目录存在
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # 安全的文件名
            filename = secure_filename(file.filename)
            
            # 添加时间戳避免文件名冲突
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            
            # 保存文件
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 获取文件信息
            file_size = os.path.getsize(file_path)
            
            return jsonify({
                'success': True,
                'message': '文件上传成功',
                'filename': filename,
                'size': file_size,
                'path': file_path
            })
        else:
            return jsonify({'success': False, 'error': '不允许的文件类型'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload_multiple', methods=['POST'])
def upload_multiple_files():
    """处理多个文件上传"""
    try:
        uploaded_files = []
        
        for file in request.files.getlist('files'):
            if file and file.filename != '' and allowed_file(file.filename):
                # 确保上传目录存在
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                # 安全的文件名
                filename = secure_filename(file.filename)
                
                # 添加时间戳
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{name}_{timestamp}{ext}"
                
                # 保存文件
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                uploaded_files.append({
                    'filename': filename,
                    'size': os.path.getsize(file_path),
                    'path': file_path
                })
        
        if uploaded_files:
            return jsonify({
                'success': True,
                'message': f'成功上传 {len(uploaded_files)} 个文件',
                'files': uploaded_files
            })
        else:
            return jsonify({'success': False, 'error': '没有有效的文件'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload_form', methods=['GET'])
def upload_form():
    """显示上传表单"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>文件上传</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h2>单个文件上传</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="上传文件">
        </form>
        
        <h2>多个文件上传</h2>
        <form action="/upload_multiple" method="post" enctype="multipart/form-data">
            <input type="file" name="files" multiple required>
            <input type="submit" value="上传文件">
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
    
    return flask_code

# ==================== 3. Django框架处理文件上传 ====================

def create_django_upload_example():
    """创建Django文件上传示例"""
    
    # Django视图代码
    views_code = '''
# views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from datetime import datetime

@csrf_exempt
def upload_file(request):
    """Django文件上传视图"""
    if request.method == 'POST':
        try:
            # 获取上传的文件
            uploaded_file = request.FILES.get('file')
            
            if not uploaded_file:
                return JsonResponse({'success': False, 'error': '没有文件'})
            
            # 生成唯一文件名
            name, ext = os.path.splitext(uploaded_file.name)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            
            # 保存文件
            file_path = default_storage.save(filename, ContentFile(uploaded_file.read()))
            
            return JsonResponse({
                'success': True,
                'message': '文件上传成功',
                'filename': filename,
                'path': file_path,
                'size': uploaded_file.size
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # GET请求显示上传表单
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django文件上传</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h2>Django文件上传</h2>
        <form action="" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="上传文件">
        </form>
    </body>
    </html>
    """)

def handle_uploaded_file(f, save_path):
    """处理上传的文件"""
    with open(save_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
'''
    
    # Django表单代码
    forms_code = '''
# forms.py
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    
    def clean_file(self):
        file = self.cleaned_data['file']
        
        # 文件大小限制（10MB）
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError('文件大小不能超过10MB')
        
        # 文件类型限制
        allowed_types = ['image/jpeg', 'image/png', 'application/pdf', 'text/plain']
        if file.content_type not in allowed_types:
            raise forms.ValidationError('不支持的文件类型')
        
        return file
'''
    
    # Django模型代码
    models_code = '''
# models.py
from django.db import models
from django.core.validators import FileExtensionValidator

class UploadedFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
'''
    
    return {
        'views': views_code,
        'forms': forms_code,
        'models': models_code
    }

# ==================== 4. 文件上传工具类 ====================

class FileUploader:
    """文件上传工具类"""
    
    def __init__(self, upload_url, max_size=10*1024*1024):
        self.upload_url = upload_url
        self.max_size = max_size
        self.allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip'}
    
    def validate_file(self, file_path):
        """验证文件"""
        if not os.path.exists(file_path):
            return False, "文件不存在"
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        if file_size > self.max_size:
            return False, f"文件大小超过限制 ({self.max_size / 1024 / 1024:.1f}MB)"
        
        # 检查文件扩展名
        ext = Path(file_path).suffix[1:].lower()
        if ext not in self.allowed_extensions:
            return False, f"不支持的文件类型: {ext}"
        
        return True, "文件验证通过"
    
    def upload(self, file_path, additional_data=None):
        """上传文件"""
        # 验证文件
        is_valid, message = self.validate_file(file_path)
        if not is_valid:
            return {'success': False, 'error': message}
        
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                data = additional_data or {}
                
                response = requests.post(self.upload_url, files=files, data=data)
                
                if response.status_code == 200:
                    return {
                        'success': True,
                        'message': '上传成功',
                        'response': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                    }
                else:
                    return {
                        'success': False,
                        'error': f'上传失败，状态码: {response.status_code}'
                    }
                    
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def batch_upload(self, file_paths):
        """批量上传文件"""
        results = []
        
        for file_path in file_paths:
            print(f"正在上传: {file_path}")
            result = self.upload(file_path)
            results.append({
                'file': file_path,
                'result': result
            })
            
            if result['success']:
                print(f"✅ {file_path} 上传成功")
            else:
                print(f"❌ {file_path} 上传失败: {result['error']}")
        
        return results

# ==================== 5. 使用示例 ====================

def demo_file_upload():
    """文件上传演示"""
    print("🎯 Python文件上传演示")
    print("=" * 50)
    
    # 示例1：使用requests上传文件
    print("\n📤 1. 使用requests上传文件")
    
    # 创建一个测试文件
    test_file = "test_upload.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("这是一个测试上传的文件\n")
        f.write(f"创建时间: {datetime.now()}\n")
        f.write("文件内容: Python文件上传测试")
    
    print(f"✅ 创建测试文件: {test_file}")
    
    # 模拟上传（需要真实的上传URL）
    upload_url = "http://httpbin.org/post"  # 测试用的URL
    
    result = upload_file_with_requests(test_file, upload_url)
    print(f"📊 上传结果: {result['success']}")
    if not result['success']:
        print(f"❌ 错误: {result['error']}")
    
    # 示例2：使用工具类上传
    print("\n🔧 2. 使用工具类上传文件")
    
    uploader = FileUploader(upload_url)
    result = uploader.upload(test_file, {'description': '工具类上传测试'})
    print(f"📊 工具类上传结果: {result['success']}")
    
    # 示例3：获取文件信息
    print("\n📋 3. 文件信息")
    
    file_info = {
        '文件名': os.path.basename(test_file),
        '文件大小': f"{os.path.getsize(test_file)} 字节",
        'MIME类型': mimetypes.guess_type(test_file)[0],
        '修改时间': datetime.fromtimestamp(os.path.getmtime(test_file)).strftime('%Y-%m-%d %H:%M:%S')
    }
    
    for key, value in file_info.items():
        print(f"  {key}: {value}")
    
    # 清理测试文件
    os.remove(test_file)
    print(f"\n🧹 清理测试文件: {test_file}")
    
    print("\n📚 更多示例:")
    print("  - Flask服务器代码: create_flask_upload_server()")
    print("  - Django上传示例: create_django_upload_example()")
    print("  - 带进度的上传: upload_with_progress()")
    print("  - 多文件上传: upload_multiple_files()")

if __name__ == "__main__":
    # 运行演示
    demo_file_upload()
    
    print("\n" + "=" * 50)
    print("🎉 Python文件上传示例完成！")
    print("\n💡 主要功能:")
    print("  ✅ requests库文件上传")
    print("  ✅ Flask文件接收服务器")
    print("  ✅ Django文件处理")
    print("  ✅ 文件验证和安全性")
    print("  ✅ 进度显示和批量上传")
    print("  ✅ 错误处理和最佳实践")