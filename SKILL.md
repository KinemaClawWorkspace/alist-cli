---
name: alist
description: |
  AList 文件管理 API。AList 是一个支持多存储的文件列表程序，支持上传、下载、预览等多种功能。
  触发条件：用户询问文件管理、上传下载、AList 操作等。
---

# AList Skill - 文件管理

基于 AList API (v3) 的文件管理工具。

## 前提条件

需要配置 AList 服务地址和认证信息。

### 环境变量（必需）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ALIST_URL` | AList 服务地址 | `https://cloud.xn--30q18ry71c.com` |
| `ALIST_USERNAME` | 用户名 | `claw` |
| `ALIST_PASSWORD` | 密码 | (需配置) |

这些变量需要在 `scripts/openclaw-docker.sh` 中配置，重启容器后自动加载。

---

## API 概览

### 认证 Auth

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/login` | POST | 登录获取 token |
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login/hash` | POST | Hash 登录 |
| `/api/me` | GET | 获取当前用户信息 |

### 文件系统 FS

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/fs/list` | POST | 列出文件目录 |
| `/api/fs/get` | POST | 获取文件/目录信息 |
| `/api/fs/dirs` | POST | 获取目录列表 |
| `/api/fs/search` | POST | 搜索文件 |
| `/api/fs/mkdir` | POST | 新建文件夹 |
| `/api/fs/rename` | POST | 重命名文件 |
| `/api/fs/batch_rename` | POST | 批量重命名 |
| `/api/fs/move` | POST | 移动文件 |
| `/api/fs/copy` | POST | 复制文件 |
| `/api/fs/remove` | POST | 删除文件 |
| `/api/fs/form` | PUT | 表单上传文件 |
| `/api/fs/put` | PUT | 流式上传文件 |
| `/api/fs/add_offline_download` | POST | 添加离线下载 |

### 公开 Public

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/public/settings` | GET | 获取站点设置 |
| `/ping` | GET | 连通性检测 |

### 管理 Admin

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/admin/user/list` | GET | 用户列表 |
| `/api/admin/storage/list` | GET | 存储列表 |
| `/api/admin/meta/list` | GET | 元信息列表 |

---

## 使用方法

### 登录

```
AList 登录
```

返回 token，后续请求需要使用此 token。

### 列出文件

```
AList 列出文件 [路径:/]
```

### 上传文件

```
AList 上传文件 <filepath>到<目标路径>
```

### 下载/获取直链

```
AList 获取直链 <文件路径>
```

### 创建文件夹

```
AList 创建文件夹 <路径>
```

### 删除文件

```
AList 删除 <文件路径>
```

### 移动文件

```
AList 移动 <源路径> 到 <目标路径>
```

### 搜索文件

```
AList 搜索 <关键词> [路径:/]
```

---

## API 调用示例

### 1. 登录获取 Token

```bash
curl -X POST "https://cloud.xn--30q18ry71c.com/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"claw","password":"your_password"}'
```

### 2. 列出文件

```bash
TOKEN="your_token"
curl -X POST "https://cloud.xn--30q18ry71c.com/api/fs/list" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path":"/","password":"","page":1,"per_page":0,"refresh":false}'
```

### 3. 上传文件

```bash
TOKEN="your_token"
curl -X PUT "https://cloud.xn--30q18ry71c.com/api/fs/put" \
  -H "Authorization: $TOKEN" \
  -H "File-Path: /test.txt" \
  -H "Content-Type: text/plain" \
  --data-binary @test.txt
```

### 4. 获取文件直链

```bash
TOKEN="your_token"
curl -X POST "https://cloud.xn--30q18ry71c.com/api/fs/get" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path":"/test.txt","password":""}'
```

### 5. 创建文件夹

```bash
TOKEN="your_token"
curl -X POST "https://cloud.xn--30q18ry71c.com/api/fs/mkdir" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path":"/new_folder"}'
```

### 6. 删除文件

```bash
TOKEN="your_token"
curl -X POST "https://cloud.xn--30q18ry71c.com/api/fs/remove" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"names":["test.txt"],"dir":"/"}'
```

### 7. 移动文件

```bash
TOKEN="your_token"
curl -X POST "https://cloud.xn--30q18ry71c.com/api/fs/move" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"src_dir":"/old","dst_dir":"/new","names":["file.txt"]}'
```

### 8. 搜索文件

```bash
TOKEN="your_token"
curl -X POST "https://cloud.xn--30q18ry71c.com/api/fs/search" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"parent":"/","keywords":"test","scope":0,"page":1,"per_page":10,"password":""}'
```

---

## Python 示例

```python
import requests
import urllib.parse

class AList:
    def __init__(self, url, token=None):
        self.url = url.rstrip('/')
        self.token = token
    
    def login(self, username, password):
        """登录获取 token"""
        resp = requests.post(
            f"{self.url}/api/auth/login",
            json={"username": username, "password": password}
        )
        data = resp.json()
        if data['code'] == 200:
            self.token = data['data']['token']
            return self.token
        raise Exception(data['message'])
    
    def list(self, path="/", page=1, per_page=0):
        """列出文件"""
        resp = requests.post(
            f"{self.url}/api/fs/list",
            headers={"Authorization": self.token},
            json={"path": path, "password": "", "page": page, "per_page": per_page, "refresh": False}
        )
        return resp.json()
    
    def get(self, path, password=""):
        """获取文件信息（含直链）"""
        resp = requests.post(
            f"{self.url}/api/fs/get",
            headers={"Authorization": self.token},
            json={"path": path, "password": password}
        )
        return resp.json()
    
    def mkdir(self, path):
        """创建文件夹"""
        resp = requests.post(
            f"{self.url}/api/fs/mkdir",
            headers={"Authorization": self.token},
            json={"path": path}
        )
        return resp.json()
    
    def upload(self, local_path, remote_path):
        """上传文件"""
        with open(local_path, 'rb') as f:
            resp = requests.put(
                f"{self.url}/api/fs/put",
                headers={
                    "Authorization": self.token,
                    "File-Path": urllib.parse.quote(remote_path),
                    "Content-Type": "application/octet-stream"
                },
                data=f
            )
        return resp.json()
    
    def remove(self, dir_path, names):
        """删除文件"""
        resp = requests.post(
            f"{self.url}/api/fs/remove",
            headers={"Authorization": self.token},
            json={"dir": dir_path, "names": names}
        )
        return resp.json()
    
    def move(self, src_dir, dst_dir, names):
        """移动文件"""
        resp = requests.post(
            f"{self.url}/api/fs/move",
            headers={"Authorization": self.token},
            json={"src_dir": src_dir, "dst_dir": dst_dir, "names": names}
        )
        return resp.json()
    
    def search(self, parent, keywords, scope=0, page=1, per_page=10):
        """搜索文件"""
        resp = requests.post(
            f"{self.url}/api/fs/search",
            headers={"Authorization": self.token},
            json={
                "parent": parent,
                "keywords": keywords,
                "scope": scope,
                "page": page,
                "per_page": per_page,
                "password": ""
            }
        )
        return resp.json()

# 使用示例
alist = AList("https://cloud.xn--30q18ry71c.com")
alist.login("claw", "your_password")

# 列出文件
files = alist.list("/")
for f in files['data']['content']:
    print(f"{'📁' if f['is_dir'] else '📄'} {f['name']}")

# 上传文件
alist.upload("test.txt", "/test.txt")

# 获取直链
info = alist.get("/test.txt")
print(info['data']['raw_url'])
```

---

## 配置

在 OpenClaw 中配置环境变量：

```yaml
# config.yml
alist:
  url: "https://cloud.xn--30q18ry71c.com"
  username: "claw"
  password: "your_password"
```

---

## 错误处理

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 401 | token 无效 |
| 403 | 权限不足 |
| 404 | 文件不存在 |
| 500 | 服务器错误 |

---

## 相关文档

- [AList 官方文档](https://alist.nn.ci/)
- [API 完整规范](references/openapi.json) - OpenAPI 3.0 格式
