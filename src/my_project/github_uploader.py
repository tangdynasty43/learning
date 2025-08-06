#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub自动上传工具
简化Git操作，快速上传文件到GitHub
"""

import os
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

class GitHubUploader:
    """GitHub上传工具类"""
    
    def __init__(self, project_path=None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.git_config = {}
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        config_file = self.project_path / '.github_uploader_config.json'
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                self.git_config = json.load(f)
    
    def save_config(self):
        """保存配置文件"""
        config_file = self.project_path / '.github_uploader_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.git_config, f, ensure_ascii=False, indent=2)
    
    def run_command(self, command, cwd=None):
        """执行命令"""
        if cwd is None:
            cwd = self.project_path
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_git_installed(self):
        """检查Git是否已安装"""
        success, stdout, stderr = self.run_command("git --version")
        if success:
            print(f"✅ Git已安装: {stdout.strip()}")
            return True
        else:
            print("❌ Git未安装，请先安装Git")
            print("   下载地址: https://git-scm.com/downloads")
            return False
    
    def check_git_config(self):
        """检查Git配置"""
        print("🔧 检查Git配置...")
        
        # 检查用户名
        success, username, _ = self.run_command("git config --global user.name")
        if not success or not username.strip():
            print("⚠️ Git用户名未配置")
            return False
        
        # 检查邮箱
        success, email, _ = self.run_command("git config --global user.email")
        if not success or not email.strip():
            print("⚠️ Git邮箱未配置")
            return False
        
        print(f"✅ Git用户: {username.strip()}")
        print(f"✅ Git邮箱: {email.strip()}")
        return True
    
    def setup_git_config(self):
        """设置Git配置"""
        print("\n🔧 配置Git用户信息")
        
        username = input("请输入GitHub用户名: ").strip()
        email = input("请输入GitHub邮箱: ").strip()
        
        if not username or not email:
            print("❌ 用户名和邮箱不能为空")
            return False
        
        # 设置用户名
        success, _, stderr = self.run_command(f'git config --global user.name "{username}"')
        if not success:
            print(f"❌ 设置用户名失败: {stderr}")
            return False
        
        # 设置邮箱
        success, _, stderr = self.run_command(f'git config --global user.email "{email}"')
        if not success:
            print(f"❌ 设置邮箱失败: {stderr}")
            return False
        
        print("✅ Git配置完成")
        return True
    
    def check_ssh_key(self):
        """检查SSH密钥"""
        ssh_dir = Path.home() / '.ssh'
        public_key = ssh_dir / 'id_rsa.pub'
        
        if public_key.exists():
            print("✅ SSH密钥已存在")
            return True
        else:
            print("⚠️ SSH密钥不存在")
            return False
    
    def generate_ssh_key(self):
        """生成SSH密钥"""
        print("\n🔐 生成SSH密钥")
        
        success, email, _ = self.run_command("git config --global user.email")
        if not success:
            email = input("请输入邮箱地址: ").strip()
        else:
            email = email.strip()
        
        command = f'ssh-keygen -t rsa -C "{email}" -f ~/.ssh/id_rsa -N ""'
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print("✅ SSH密钥生成成功")
            self.show_public_key()
            return True
        else:
            print(f"❌ SSH密钥生成失败: {stderr}")
            return False
    
    def show_public_key(self):
        """显示公钥内容"""
        public_key_file = Path.home() / '.ssh' / 'id_rsa.pub'
        
        if public_key_file.exists():
            with open(public_key_file, 'r') as f:
                public_key = f.read().strip()
            
            print("\n📋 SSH公钥内容（请复制到GitHub）:")
            print("=" * 60)
            print(public_key)
            print("=" * 60)
            print("\n📝 添加SSH密钥到GitHub的步骤:")
            print("1. 登录GitHub")
            print("2. 点击右上角头像 → Settings")
            print("3. 左侧菜单选择 'SSH and GPG keys'")
            print("4. 点击 'New SSH key'")
            print("5. 粘贴上面的公钥内容")
            print("6. 点击 'Add SSH key'")
            
            input("\n按回车键继续...")
        else:
            print("❌ 公钥文件不存在")
    
    def test_ssh_connection(self):
        """测试SSH连接"""
        print("\n🔗 测试GitHub SSH连接...")
        
        success, stdout, stderr = self.run_command("ssh -T git@github.com")
        
        if "successfully authenticated" in stdout or "successfully authenticated" in stderr:
            print("✅ SSH连接成功")
            return True
        else:
            print("❌ SSH连接失败")
            print(f"错误信息: {stderr}")
            return False
    
    def is_git_repo(self):
        """检查是否为Git仓库"""
        git_dir = self.project_path / '.git'
        return git_dir.exists()
    
    def init_git_repo(self):
        """初始化Git仓库"""
        if self.is_git_repo():
            print("✅ 已是Git仓库")
            return True
        
        print("📁 初始化Git仓库...")
        success, stdout, stderr = self.run_command("git init")
        
        if success:
            print("✅ Git仓库初始化成功")
            return True
        else:
            print(f"❌ Git仓库初始化失败: {stderr}")
            return False
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        gitignore_file = self.project_path / '.gitignore'
        
        if gitignore_file.exists():
            print("✅ .gitignore文件已存在")
            return
        
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
uploads/
data/
*.log
.env
.github_uploader_config.json
""".strip()
        
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        print("✅ .gitignore文件创建成功")
    
    def add_files(self, files=None):
        """添加文件到暂存区"""
        if files is None:
            command = "git add ."
            print("📁 添加所有文件到暂存区...")
        else:
            files_str = ' '.join(f'"{f}"' for f in files)
            command = f"git add {files_str}"
            print(f"📁 添加指定文件到暂存区: {files}")
        
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print("✅ 文件添加成功")
            return True
        else:
            print(f"❌ 文件添加失败: {stderr}")
            return False
    
    def commit_files(self, message=None):
        """提交文件"""
        if message is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Update files - {timestamp}"
        
        command = f'git commit -m "{message}"'
        print(f"💾 提交文件: {message}")
        
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print("✅ 文件提交成功")
            return True
        elif "nothing to commit" in stdout:
            print("ℹ️ 没有需要提交的更改")
            return True
        else:
            print(f"❌ 文件提交失败: {stderr}")
            return False
    
    def add_remote_origin(self, repo_url):
        """添加远程仓库"""
        # 检查是否已有远程仓库
        success, stdout, _ = self.run_command("git remote get-url origin")
        
        if success and stdout.strip():
            print(f"✅ 远程仓库已存在: {stdout.strip()}")
            return True
        
        print(f"🔗 添加远程仓库: {repo_url}")
        success, stdout, stderr = self.run_command(f"git remote add origin {repo_url}")
        
        if success:
            print("✅ 远程仓库添加成功")
            self.git_config['repo_url'] = repo_url
            self.save_config()
            return True
        else:
            print(f"❌ 远程仓库添加失败: {stderr}")
            return False
    
    def push_to_github(self, branch='main'):
        """推送到GitHub"""
        print(f"🚀 推送到GitHub ({branch}分支)...")
        
        # 首次推送使用-u参数
        command = f"git push -u origin {branch}"
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print("✅ 推送成功")
            return True
        elif "master" in stderr and branch == "main":
            # 尝试推送到master分支
            print("🔄 尝试推送到master分支...")
            return self.push_to_github('master')
        else:
            print(f"❌ 推送失败: {stderr}")
            
            # 常见错误处理
            if "rejected" in stderr:
                print("\n💡 可能的解决方案:")
                print("1. 先拉取远程更新: git pull origin main")
                print("2. 解决冲突后重新推送")
                
                if input("是否尝试拉取远程更新? (y/n): ").lower() == 'y':
                    return self.pull_and_push(branch)
            
            return False
    
    def pull_and_push(self, branch='main'):
        """拉取更新并推送"""
        print(f"📥 拉取远程更新...")
        
        command = f"git pull origin {branch} --allow-unrelated-histories"
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print("✅ 拉取成功")
            return self.push_to_github(branch)
        else:
            print(f"❌ 拉取失败: {stderr}")
            return False
    
    def get_repo_status(self):
        """获取仓库状态"""
        success, stdout, stderr = self.run_command("git status --porcelain")
        
        if success:
            if stdout.strip():
                print("📋 仓库状态: 有未提交的更改")
                return 'modified'
            else:
                print("📋 仓库状态: 工作目录干净")
                return 'clean'
        else:
            print("❌ 无法获取仓库状态")
            return 'error'
    
    def quick_upload(self, commit_message=None, repo_url=None):
        """快速上传（一键操作）"""
        print("🚀 开始快速上传到GitHub")
        print("=" * 50)
        
        # 1. 检查Git
        if not self.check_git_installed():
            return False
        
        # 2. 检查Git配置
        if not self.check_git_config():
            if not self.setup_git_config():
                return False
        
        # 3. 检查SSH密钥
        if not self.check_ssh_key():
            if input("是否生成SSH密钥? (y/n): ").lower() == 'y':
                if not self.generate_ssh_key():
                    return False
            else:
                print("❌ 需要SSH密钥才能上传")
                return False
        
        # 4. 测试SSH连接
        if not self.test_ssh_connection():
            print("\n请确保已将SSH公钥添加到GitHub")
            self.show_public_key()
            if input("已添加SSH密钥到GitHub? (y/n): ").lower() != 'y':
                return False
            
            if not self.test_ssh_connection():
                return False
        
        # 5. 初始化仓库
        if not self.init_git_repo():
            return False
        
        # 6. 创建.gitignore
        self.create_gitignore()
        
        # 7. 添加文件
        if not self.add_files():
            return False
        
        # 8. 提交文件
        if not self.commit_files(commit_message):
            return False
        
        # 9. 添加远程仓库
        if repo_url:
            if not self.add_remote_origin(repo_url):
                return False
        elif 'repo_url' not in self.git_config:
            repo_url = input("请输入GitHub仓库SSH地址 (git@github.com:username/repo.git): ").strip()
            if not repo_url:
                print("❌ 仓库地址不能为空")
                return False
            if not self.add_remote_origin(repo_url):
                return False
        
        # 10. 推送到GitHub
        if not self.push_to_github():
            return False
        
        print("\n🎉 上传完成！")
        print(f"📁 项目路径: {self.project_path}")
        if 'repo_url' in self.git_config:
            repo_web_url = self.git_config['repo_url'].replace('git@github.com:', 'https://github.com/').replace('.git', '')
            print(f"🌐 GitHub地址: {repo_web_url}")
        
        return True

def main():
    """主函数"""
    print("🎯 GitHub自动上传工具")
    print("=" * 50)
    
    # 获取项目路径
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = input(f"请输入项目路径 (默认: {os.getcwd()}): ").strip()
        if not project_path:
            project_path = os.getcwd()
    
    if not os.path.exists(project_path):
        print(f"❌ 路径不存在: {project_path}")
        return
    
    # 创建上传器
    uploader = GitHubUploader(project_path)
    
    # 显示菜单
    while True:
        print("\n📋 选择操作:")
        print("1. 快速上传 (推荐)")
        print("2. 检查环境")
        print("3. 配置Git")
        print("4. 生成SSH密钥")
        print("5. 显示SSH公钥")
        print("6. 测试SSH连接")
        print("7. 查看仓库状态")
        print("8. 手动上传")
        print("0. 退出")
        
        choice = input("\n请选择 (0-8): ").strip()
        
        if choice == '1':
            commit_msg = input("提交信息 (可选): ").strip()
            repo_url = input("仓库地址 (可选): ").strip()
            uploader.quick_upload(commit_msg or None, repo_url or None)
        
        elif choice == '2':
            uploader.check_git_installed()
            uploader.check_git_config()
            uploader.check_ssh_key()
            uploader.test_ssh_connection()
        
        elif choice == '3':
            uploader.setup_git_config()
        
        elif choice == '4':
            uploader.generate_ssh_key()
        
        elif choice == '5':
            uploader.show_public_key()
        
        elif choice == '6':
            uploader.test_ssh_connection()
        
        elif choice == '7':
            uploader.get_repo_status()
        
        elif choice == '8':
            print("\n🔧 手动上传步骤:")
            if uploader.init_git_repo():
                uploader.create_gitignore()
                if uploader.add_files():
                    msg = input("提交信息: ").strip()
                    if uploader.commit_files(msg):
                        url = input("仓库SSH地址: ").strip()
                        if url and uploader.add_remote_origin(url):
                            uploader.push_to_github()
        
        elif choice == '0':
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")