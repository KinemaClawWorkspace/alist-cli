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

Note: 
    - 用户路径是相对于 base_path 的虚拟路径
    - skill 自动处理 base_path 转换
"""

import argparse
import json
import os
import sys
import urllib.parse
import requests

# 配置
DEFAULT_URL = os.environ.get("ALIST_URL", "https://cloud.xn--30q18ry71c.com")
DEFAULT_USERNAME = os.environ.get("ALIST_USERNAME", "claw")
DEFAULT_PASSWORD = os.environ.get("ALIST_PASSWORD", "")
TOKEN_FILE = os.path.expanduser("~/.alist_token")
USER_INFO_FILE = os.path.expanduser("~/.alist_user_info")


class AList:
    def __init__(self, url=DEFAULT_URL):
        self.url = url.rstrip('/')
        self.token = self._load_token()
        self.base_path = self._load_user_info().get('base_path', '')
    
    def _load_token(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE) as f:
                return f.read().strip()
        return None
    
    def _save_token(self, token):
        with open(TOKEN_FILE, 'w') as f:
            f.write(token)
        self.token = token
    
    def _load_user_info(self):
        if os.path.exists(USER_INFO_FILE):
            with open(USER_INFO_FILE) as f:
                return json.load(f)
        return {}
    
    def _save_user_info(self, user_info):
        with open(USER_INFO_FILE, 'w') as f:
            json.dump(user_info, f)
        if 'base_path' in user_info:
            self.base_path = user_info['base_path']
    
    def _to_real_path(self, user_path):
        """将用户路径转换为实际路径（添加 base_path 前缀）"""
        user_path = user_path.lstrip('/')
        if self.base_path:
            return f"{self.base_path}/{user_path}".rstrip('/')
        return f"/{user_path}".rstrip('/') or '/'
    
    def _to_user_path(self, real_path):
        """将实际路径转换为用户路径（去掉 base_path 前缀）"""
        if self.base_path and real_path.startswith(self.base_path):
            return real_path[len(self.base_path):] or '/'
        return real_path
    
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
            # 登录后获取用户信息
            user_data = self._request('GET', '/api/me')
            if user_data['code'] == 200:
                user_info = user_data['data']
                self._save_user_info(user_info)
                print(f"✅ 登录成功！")
                print(f"   用户: {user_info['username']}")
                print(f"   根目录: {user_info.get('base_path', '/')}")
            else:
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
            print(f"根目录 (base_path): {user.get('base_path', '/')}")
            print(f"用户视角根目录: /")
            return user
        print(f"❌ {data['message']}")
        return None
    
    def ls(self, path="/", page=1, per_page=20):
        """列出文件"""
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/list', json={
            "path": real_path, "password": "", "page": page, 
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
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/get', json={
            "path": real_path, "password": ""
        })
        if data['code'] != 200:
            print(f"❌ {data['message']}")
            return None
        
        f = data['data']
        print(f"📄 {f['name']}")
        print(f"   用户路径: {path}")
        print(f"   实际路径: {real_path}")
        print(f"   大小: {self._format_size(f.get('size', 0))}")
        print(f"   类型: {'文件夹' if f['is_dir'] else '文件'}")
        print(f"   修改: {f.get('modified', '')}")
        if f.get('raw_url'):
            # 构建用户可访问的 URL
            raw_url = f['raw_url']
            # 将实际路径替换为用户路径显示
            print(f"   直链: {raw_url}")
        return f
    
    def mkdir(self, path):
        """创建文件夹"""
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/mkdir', json={"path": real_path})
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
        
        real_path = self._to_real_path(remote_path)
        filename = os.path.basename(local_path)
        
        with open(local_path, 'rb') as f:
            data = self._request('PUT', '/api/fs/put', 
                headers={
                    "File-Path": urllib.parse.quote(real_path),
                    "Content-Type": "application/octet-stream"
                },
                data=f
            )
        
        if data['code'] == 200:
            print(f"✅ 上传成功!")
            print(f"   用户路径: {remote_path}")
            print(f"   实际路径: {real_path}")
            print(f"   访问链接: {self.url}{real_path}")
            return True
        print(f"❌ {data['message']}")
        return False
    
    def rm(self, path):
        """删除文件"""
        real_path = self._to_real_path(path)
        # 获取父目录和文件名
        parts = real_path.rsplit('/', 1)
        if len(parts) == 2:
            dir_path, name = parts
        else:
            dir_path = "/"
            name = real_path
        
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
        real_src = self._to_real_path(src)
        real_dst = self._to_real_path(dst)
        
        src_dir = real_src.rsplit('/', 1)[0] or "/"
        name = real_src.split('/')[-1]
        
        data = self._request('POST', '/api/fs/move', json={
            "src_dir": src_dir,
            "dst_dir": real_dst if real_dst.endswith('/') else real_dst + '/',
            "names": [name]
        })
        if data['code'] == 200:
            print(f"✅ 已移动: {src} -> {dst}")
            return True
        print(f"❌ {data['message']}")
        return False
    
    def search(self, keyword, path="/"):
        """搜索文件"""
        real_path = self._to_real_path(path)
        data = self._request('POST', '/api/fs/search', json={
            "parent": real_path,
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
            # 显示用户视角路径
            parent = f.get('parent', '')
            user_parent = self._to_user_path(parent)
            print(f"  {icon} {user_parent}/{f['name']}")
        return files
    
    @staticmethod
    def _format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"


def main():
    parser = argparse.ArgumentParser(description="AList CLI - 文件管理工具")
    parser.add_argument("command", choices=["login", "ls", "get", "mkdir", "upload", "rm", "mv", "search", "whoami"])
    parser.add_argument("args", nargs="*", help="命令参数")
    
    args = parser.parse_args()
    alist = AList()
    
    if args.command == "login":
        # 如果没有提供参数，使用环境变量
        username = args.args[0] if len(args.args) > 0 else DEFAULT_USERNAME
        password = args.args[1] if len(args.args) > 1 else DEFAULT_PASSWORD
        if not username or not password:
            print("❌ 请提供用户名和密码，或设置环境变量 ALIST_USERNAME 和 ALIST_PASSWORD")
            sys.exit(1)
        alist.login(username, password)
    
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
