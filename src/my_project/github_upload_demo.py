#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub上传演示脚本
自动化演示GitHub上传过程
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

class GitHubUploadDemo:
    """GitHub上传演示类"""
    
    def __init__(self, project_path=None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        print(f"📁 项目路径: {self.project_path}")
    
    def run_command(self, command, show_output=True):
        """执行命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if show_output:
                if result.stdout:
                    print(f"📤 输出: {result.stdout.strip()}")
                if result.stderr and result.returncode != 0:
                    print(f"⚠️ 错误: {result.stderr.strip()}")
            
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            print(f"❌ 命令执行异常: {e}")
            return False, "", str(e)
    
    def check_git_installed(self):
        """检查Git是否已安装"""
        print("\n🔍 检查Git安装状态...")
        success, stdout, stderr = self.run_command("git --version", False)
        
        if success:
            print(f"✅ Git已安装: {stdout.strip()}")
            return True
        else:
            print("❌ Git未安装")
            print("💡 请从以下地址下载安装Git:")
            print("   https://git-scm.com/downloads")
            return False
    
    def check_git_config(self):
        """检查Git配置"""
        print("\n🔧 检查Git配置...")
        
        # 检查用户名
        success, username, _ = self.run_command("git config --global user.name", False)
        if success and username.strip():
            print(f"✅ Git用户名: {username.strip()}")
        else:
            print("⚠️ Git用户名未配置")
            print("💡 配置命令: git config --global user.name \"你的用户名\"")
            return False
        
        # 检查邮箱
        success, email, _ = self.run_command("git config --global user.email", False)
        if success and email.strip():
            print(f"✅ Git邮箱: {email.strip()}")
        else:
            print("⚠️ Git邮箱未配置")
            print("💡 配置命令: git config --global user.email \"你的邮箱\"")
            return False
        
        return True
    
    def check_ssh_key(self):
        """检查SSH密钥"""
        print("\n🔐 检查SSH密钥...")
        ssh_dir = Path.home() / '.ssh'
        public_key = ssh_dir / 'id_rsa.pub'
        
        if public_key.exists():
            print("✅ SSH密钥已存在")
            print(f"📍 公钥位置: {public_key}")
            
            # 显示公钥内容
            try:
                with open(public_key, 'r') as f:
                    key_content = f.read().strip()
                print("\n📋 SSH公钥内容:")
                print("-" * 50)
                print(key_content)
                print("-" * 50)
                print("\n💡 PowerShell复制命令:")
                print(f"Get-Content '{public_key}' | Set-Clipboard")
            except Exception as e:
                print(f"❌ 读取公钥失败: {e}")
            
            return True
        else:
            print("❌ SSH密钥不存在")
            print("💡 生成SSH密钥命令:")
            print('ssh-keygen -t rsa -C "your_email@example.com"')
            return False
    
    def test_ssh_connection(self):
        """测试SSH连接"""
        print("\n🔗 测试GitHub SSH连接...")
        
        success, stdout, stderr = self.run_command("ssh -T git@github.com", False)
        
        if "successfully authenticated" in stdout or "successfully authenticated" in stderr:
            print("✅ SSH连接成功")
            return True
        else:
            print("❌ SSH连接失败")
            print("💡 请确保:")
            print("   1. SSH密钥已生成")
            print("   2. 公钥已添加到GitHub")
            print("   3. GitHub账户设置正确")
            return False
    
    def check_git_repo(self):
        """检查Git仓库状态"""
        print("\n📂 检查Git仓库状态...")
        
        git_dir = self.project_path / '.git'
        if git_dir.exists():
            print("✅ 已是Git仓库")
            
            # 检查远程仓库
            success, stdout, _ = self.run_command("git remote get-url origin", False)
            if success and stdout.strip():
                print(f"🔗 远程仓库: {stdout.strip()}")
            else:
                print("⚠️ 未配置远程仓库")
            
            # 检查状态
            success, stdout, _ = self.run_command("git status --porcelain", False)
            if success:
                if stdout.strip():
                    print("📝 有未提交的更改")
                else:
                    print("✨ 工作目录干净")
            
            return True
        else:
            print("❌ 不是Git仓库")
            print("💡 初始化命令: git init")
            return False
    
    def show_git_commands(self):
        """显示常用Git命令"""
        print("\n📚 常用Git命令参考:")
        print("=" * 50)
        
        commands = [
            ("初始化仓库", "git init"),
            ("添加文件", "git add ."),
            ("提交更改", 'git commit -m "提交信息"'),
            ("添加远程仓库", "git remote add origin git@github.com:用户名/仓库名.git"),
            ("推送到GitHub", "git push -u origin main"),
            ("查看状态", "git status"),
            ("查看日志", "git log --oneline"),
            ("拉取更新", "git pull origin main"),
        ]
        
        for desc, cmd in commands:
            print(f"  {desc:12} : {cmd}")
        
        print("=" * 50)
    
    def show_github_setup_guide(self):
        """显示GitHub设置指南"""
        print("\n🎯 GitHub设置指南:")
        print("=" * 50)
        
        steps = [
            "1. 注册GitHub账户 (https://github.com)",
            "2. 创建新仓库 (点击右上角 + 号)",
            "3. 配置Git用户信息",
            "4. 生成SSH密钥",
            "5. 添加SSH公钥到GitHub",
            "6. 测试SSH连接",
            "7. 初始化本地仓库",
            "8. 添加远程仓库",
            "9. 推送代码到GitHub"
        ]
        
        for step in steps:
            print(f"  {step}")
        
        print("=" * 50)
    
    def demo_upload_process(self):
        """演示上传过程"""
        print("\n🚀 GitHub上传过程演示")
        print("=" * 50)
        
        # 检查环境
        if not self.check_git_installed():
            return False
        
        if not self.check_git_config():
            return False
        
        self.check_ssh_key()
        self.test_ssh_connection()
        self.check_git_repo()
        
        # 显示指南
        self.show_git_commands()
        self.show_github_setup_guide()
        
        print("\n✨ 演示完成！")
        print("💡 如果环境配置完整，可以使用以下步骤上传:")
        print("   1. git add .")
        print("   2. git commit -m \"Initial commit\"")
        print("   3. git remote add origin <你的仓库地址>")
        print("   4. git push -u origin main")
        
        return True

def main():
    """主函数"""
    print("🎯 GitHub上传演示")
    print("=" * 50)
    
    # 使用当前目录作为项目路径
    current_dir = os.getcwd()
    demo = GitHubUploadDemo(current_dir)
    
    # 运行演示
    demo.demo_upload_process()
    
    print("\n📖 更多信息请参考:")
    print("   - GitHub上传教程.md")
    print("   - github_uploader.py (完整工具)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 演示中断")
    except Exception as e:
        print(f"\n❌ 演示错误: {e}")