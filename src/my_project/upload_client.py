#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python文件上传客户端示例
演示如何使用requests库向Flask服务器上传文件
"""

import requests
import os
from pathlib import Path
import json
from typing import List, Dict, Optional
import time

class FileUploadClient:
    """文件上传客户端"""
    
    def __init__(self, server_url: str = "http://localhost:5000"):
        self.server_url = server_url.rstrip('/')
        self.session = requests.Session()
    
    def upload_file(self, file_path: str, progress_callback=None) -> Dict:
        """上传单个文件"""
        if not os.path.exists(file_path):
            return {'success': False, 'message': f'文件不存在: {file_path}'}
        
        try:
            with open(file_path, 'rb') as f:
                files = {'files': (os.path.basename(file_path), f)}
                
                if progress_callback:
                    # 模拟进度回调
                    file_size = os.path.getsize(file_path)
                    progress_callback(0, file_size)
                
                response = self.session.post(
                    f"{self.server_url}/api/upload",
                    files=files,
                    timeout=30
                )
                
                if progress_callback:
                    progress_callback(file_size, file_size)
                
                return response.json()
                
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': f'网络错误: {str(e)}'}
        except Exception as e:
            return {'success': False, 'message': f'上传失败: {str(e)}'}
    
    def upload_multiple_files(self, file_paths: List[str], progress_callback=None) -> Dict:
        """上传多个文件"""
        if not file_paths:
            return {'success': False, 'message': '没有指定文件'}
        
        # 检查文件是否存在
        valid_files = []
        for file_path in file_paths:
            if os.path.exists(file_path):
                valid_files.append(file_path)
            else:
                print(f"⚠️ 文件不存在，跳过: {file_path}")
        
        if not valid_files:
            return {'success': False, 'message': '没有有效的文件'}
        
        try:
            files = []
            total_size = 0
            
            for file_path in valid_files:
                total_size += os.path.getsize(file_path)
                files.append(('files', (os.path.basename(file_path), open(file_path, 'rb'))))
            
            if progress_callback:
                progress_callback(0, total_size)
            
            response = self.session.post(
                f"{self.server_url}/api/upload",
                files=files,
                timeout=60
            )
            
            # 关闭文件句柄
            for _, (_, file_obj) in files:
                file_obj.close()
            
            if progress_callback:
                progress_callback(total_size, total_size)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': f'网络错误: {str(e)}'}
        except Exception as e:
            return {'success': False, 'message': f'上传失败: {str(e)}'}
        finally:
            # 确保所有文件都被关闭
            for _, (_, file_obj) in files:
                if not file_obj.closed:
                    file_obj.close()
    
    def get_file_list(self) -> Dict:
        """获取服务器上的文件列表"""
        try:
            response = self.session.get(f"{self.server_url}/api/files", timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f'网络错误: {str(e)}'}
        except Exception as e:
            return {'error': f'获取文件列表失败: {str(e)}'}
    
    def download_file(self, filename: str, save_path: str = None) -> bool:
        """下载文件"""
        try:
            response = self.session.get(
                f"{self.server_url}/download/{filename}",
                timeout=30,
                stream=True
            )
            
            if response.status_code == 200:
                if save_path is None:
                    save_path = filename
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return True
            else:
                print(f"下载失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"下载错误: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """测试服务器连接"""
        try:
            response = self.session.get(f"{self.server_url}/api/files", timeout=5)
            return response.status_code == 200
        except:
            return False

def progress_callback(uploaded: int, total: int):
    """进度回调函数"""
    if total > 0:
        percent = (uploaded / total) * 100
        bar_length = 30
        filled_length = int(bar_length * uploaded // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r📤 上传进度: |{bar}| {percent:.1f}% ({uploaded}/{total} 字节)", end='', flush=True)
        if uploaded == total:
            print()  # 换行

def create_test_files():
    """创建测试文件"""
    test_files = []
    
    # 创建文本文件
    text_file = "test_document.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("这是一个测试文档\n")
        f.write("包含中文内容\n")
        f.write("用于演示文件上传功能\n")
        f.write(f"创建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    test_files.append(text_file)
    
    # 创建JSON文件
    json_file = "test_data.json"
    test_data = {
        "name": "测试数据",
        "version": "1.0",
        "items": ["项目1", "项目2", "项目3"],
        "timestamp": time.time()
    }
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    test_files.append(json_file)
    
    # 创建CSV文件
    csv_file = "test_data.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("姓名,年龄,城市\n")
        f.write("张三,25,北京\n")
        f.write("李四,30,上海\n")
        f.write("王五,28,广州\n")
    test_files.append(csv_file)
    
    return test_files

def demo_upload():
    """演示文件上传功能"""
    print("🎯 Python文件上传客户端演示")
    print("=" * 50)
    
    # 创建客户端
    client = FileUploadClient()
    
    # 测试连接
    print("🔗 测试服务器连接...")
    if not client.test_connection():
        print("❌ 无法连接到服务器，请确保Flask服务器正在运行")
        print("   启动命令: python flask_upload_server.py")
        return
    print("✅ 服务器连接成功")
    
    # 创建测试文件
    print("\n📝 创建测试文件...")
    test_files = create_test_files()
    for file in test_files:
        print(f"   ✅ 创建: {file}")
    
    # 单文件上传
    print("\n📤 单文件上传演示:")
    result = client.upload_file(test_files[0], progress_callback)
    if result['success']:
        print(f"✅ 上传成功: {result['message']}")
    else:
        print(f"❌ 上传失败: {result['message']}")
    
    # 多文件上传
    print("\n📤 多文件上传演示:")
    result = client.upload_multiple_files(test_files[1:], progress_callback)
    if result['success']:
        print(f"✅ 批量上传成功: {result['message']}")
        if 'uploaded_files' in result:
            for file_info in result['uploaded_files']:
                print(f"   📄 {file_info['filename']} ({file_info['size']} 字节)")
    else:
        print(f"❌ 批量上传失败: {result['message']}")
    
    # 获取文件列表
    print("\n📋 获取服务器文件列表:")
    file_list = client.get_file_list()
    if 'files' in file_list:
        print(f"   服务器上共有 {len(file_list['files'])} 个文件:")
        for file_info in file_list['files']:
            print(f"   📄 {file_info['filename']} - {file_info['size']} 字节 - {file_info['modified_time']}")
    else:
        print(f"   ❌ 获取失败: {file_list.get('error', '未知错误')}")
    
    # 下载文件测试
    if 'files' in file_list and file_list['files']:
        print("\n📥 下载文件演示:")
        first_file = file_list['files'][0]['filename']
        download_path = f"downloaded_{first_file}"
        if client.download_file(first_file, download_path):
            print(f"✅ 下载成功: {download_path}")
        else:
            print(f"❌ 下载失败: {first_file}")
    
    # 清理测试文件
    print("\n🧹 清理测试文件:")
    for file in test_files:
        try:
            os.remove(file)
            print(f"   🗑️ 删除: {file}")
        except:
            pass
    
    # 清理下载的文件
    if 'download_path' in locals() and os.path.exists(download_path):
        try:
            os.remove(download_path)
            print(f"   🗑️ 删除: {download_path}")
        except:
            pass
    
    print("\n🎉 文件上传客户端演示完成！")
    print("\n💡 主要功能:")
    print("   ✅ 单文件上传")
    print("   ✅ 多文件批量上传")
    print("   ✅ 上传进度显示")
    print("   ✅ 文件列表获取")
    print("   ✅ 文件下载")
    print("   ✅ 连接测试")
    print("   ✅ 错误处理")

if __name__ == "__main__":
    demo_upload()