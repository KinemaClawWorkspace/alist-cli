#!/usr/bin/env python3
"""
AList CLI - 文件管理工具

Usage:
    alist login <username> <password>
    alist ls [path]
    alist get <path>
    alist mkdir <path>
    alist upload <local_path> <remote_path>
    alist rm <path>
    alist mv <src> <dst>
    alist search <keyword> [path]
    alist whoami
"""

import argparse
import json
import os
import sys
import urllib.parse
import requests

# 配置
DEFAULT_URL = os.environ.get("ALIST_URL", "https://cloud.xn--30q18ry71c.com")
TOKEN_FILE = os.path.expanduser("~/.alist_token")


class AList:
    def __init__(self, url=DEFAULT_URL):
        self.url = url.rstrip('/')
        self.token = self._load_token()
    
    def _load_token(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE) as f:
                return f.read().strip()
        return None
    
    def _save_token(self, token):
        with open(TOKEN_FILE, 'w') as f:
            f.write(token)
        self.token = token
    
    def _request(self, method, endpoint, **kwargs):
        url = f"{self.url}{endpoint}"
        headers = kwargs.pop('headers', {})
        if self.token:
            headers['Authorization'] = self.token
        headers.setdefault('Content-Type', 'application/json')
        
        resp = requests.request(method, url, headers=headers, **kwargs)
        return resp.json()
    
    def login(self, username, password):
        """登录"""
        data = self._request('POST', '/api/auth/login', json={
            "username": username, "password": password
        })
        if data['code'] == 200:
            self._save_token(data['data']['token'])
            print(f"✅ 登录成功！Token 已保存")
            return True
        print(f"❌ 登录失败: {data['message']}")
        return False
    
    def whoami(self):
        """获取当前用户信息"""
        data = self._request('GET', '/api/me')
        if data['code'] == 200:
            user = data['data']
            print(f"用户: {user['username']}")
            print(f"ID: {user['id']}")
            print(f"根目录: {user['base_path']}")
            return user
        print(f"❌ {data['message']}")
        return None
    
    def ls(self, path="/", page=1, per_page=20):
        """列出文件"""
        data = self._request('POST', '/api/fs/list', json={
            "path": path, "password": "", "page": page, 
            "per_page": per_page, "refresh": False
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return []
        
        files = data['data']['content']
        total = data['data']['total']
        print(f"📂 {path} ({total} items)\n")
        
        for f in files:
            icon = "📁" if f['is_dir'] else "📄"
            size = f.get('size', 0)
            size_str = self._format_size(size) if not f['is_dir'] else ""
            print(f"  {icon} {f['name']} {size_str}")
        return files
    
    def get(self, path):
        """获取文件信息"""
        data = self._request('POST', '/api/fs/get', json={
            "path": path, "password": ""
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return None
        
        f = data['data']
        print(f"📄 {f['name']}")
        print(f"   大小: {self._format_size(f.get('size', 0))}")
        print(f"   类型: {'文件夹' if f['is_dir'] else '文件'}")
        print(f"   修改: {f.get('modified', '')}")
        if f.get('raw_url'):
            print(f"   直链: {f['raw_url']}")
        return f
    
    def mkdir(self, path):
        """创建文件夹"""
        data = self._request('POST', '/api/fs/mkdir', json={"path": path})
        if data['code'] == 200:
            print(f"✅ 已创建文件夹: {path}")
            return True
        print(f"❌ {data['message']}")
        return False
    
    def upload(self, local_path, remote_path):
        """上传文件"""
        if not os.path.exists(local_path):
            print(f"❌ 文件不存在: {local_path}")
            return False
        
        with open(local_path, 'rb') as f:
            data = self._request('PUT', '/api/fs/put', 
                headers={
                    "File-Path": urllib.parse.quote(remote_path),
                    "Content-Type": "application/octet-stream"
                },
                data=f
            )
        
        if data['code'] == 200:
            print(f"✅ 上传成功: {remote_path}")
            return True
        print(f"❌ {data['message']}")
        return False
    
    def rm(self, path):
        """删除文件"""
        # 获取父目录和文件名
        parts = path.rsplit('/', 1)
        if len(parts) == 2:
            dir_path, name = parts
        else:
            dir_path = "/"
            name = path
        
        data = self._request('POST', '/api/fs/remove', json={
            "dir": dir_path, "names": [name]
        })
        if data['code'] == 200:
            print(f"✅ 已删除: {path}")
            return True
        print(f"❌ {data['message']}")
        return False
    
    def mv(self, src, dst):
        """移动文件"""
        src_dir = src.rsplit('/', 1)[0] or "/"
        name = src.split('/')[-1]
        
        data = self._request('POST', '/api/fs/move', json={
            "src_dir": src_dir,
            "dst_dir": dst if dst.endswith('/') else dst + '/',
            "names": [name]
        })
        if data['code'] == 200:
            print(f"✅ 已移动: {src} -> {dst}")
            return True
        print(f"❌ {data['message']}")
        return False
    
    def search(self, keyword, path="/"):
        """搜索文件"""
        data = self._request('POST', '/api/fs/search', json={
            "parent": path,
            "keywords": keyword,
            "scope": 0,
            "page": 1,
            "per_page": 20,
            "password": ""
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return []
        
        files = data['data']['content']
        print(f"🔍 搜索 '{keyword}' 在 {path}:\n")
        
        for f in files:
            icon = "📁" if f['is_dir'] else "📄"
            print(f"  {icon} {f['name']}")
        return files
    
    @staticmethod
    def _format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"


def main():
    parser = argparse.ArgumentParser(description="AList CLI")
    parser.add_argument("command", choices=["login", "ls", "get", "mkdir", "upload", "rm", "mv", "search", "whoami"])
    parser.add_argument("args", nargs="*", help="命令参数")
    
    args = parser.parse_args()
    alist = AList()
    
    if args.command == "login":
        if len(args.args) < 2:
            print("用法: alist login <username> <password>")
            sys.exit(1)
        alist.login(args.args[0], args.args[1])
    
    elif args.command == "whoami":
        alist.whoami()
    
    elif args.command == "ls":
        path = args.args[0] if args.args else "/"
        alist.ls(path)
    
    elif args.command == "get":
        if not args.args:
            print("用法: alist get <path>")
            sys.exit(1)
        alist.get(args.args[0])
    
    elif args.command == "mkdir":
        if not args.args:
            print("用法: alist mkdir <path>")
            sys.exit(1)
        alist.mkdir(args.args[0])
    
    elif args.command == "upload":
        if len(args.args) < 2:
            print("用法: alist upload <local_path> <remote_path>")
            sys.exit(1)
        alist.upload(args.args[0], args.args[1])
    
    elif args.command == "rm":
        if not args.args:
            print("用法: alist rm <path>")
            sys.exit(1)
        alist.rm(args.args[0])
    
    elif args.command == "mv":
        if len(args.args) < 2:
            print("用法: alist mv <src> <dst>")
            sys.exit(1)
        alist.mv(args.args[0], args.args[1])
    
    elif args.command == "search":
        if not args.args:
            print("用法: alist search <keyword> [path]")
            sys.exit(1)
        path = args.args[1] if len(args.args) > 1 else "/"
        alist.search(args.args[0], path)


if __name__ == "__main__":
    main()
