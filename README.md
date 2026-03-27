# AList CLI for OpenClaw

基于 AList API 的文件管理工具，供 OpenClaw AI 助手使用。

## 功能

- 登录认证
- 文件列表/浏览
- 文件上传/下载
- 创建文件夹
- 删除/移动/复制文件
- 搜索文件
- 获取文件直链
- 离线下载

## 安装

```bash
npm i -g alist-cli
```

## 配置

在 `scripts/openclaw-docker.sh` 中配置环境变量：

```bash
export ALIST_URL="https://your_alist_server"
export ALIST_USERNAME="your_username"
export ALIST_PASSWORD="your_password"
```

## 使用

```bash
alist login
alist ls /
alist upload local.txt /remote.txt
alist get /file.txt
alist mkdir /folder
alist rm /file.txt
alist mv /old /new
alist search keyword
alist whoami
```

## CLI 选项

| 命令 | 说明 |
|------|------|
| login <user> <pass> | 登录 |
| ls [path] | 列出文件 |
| get <path> | 获取文件信息 |
| mkdir <path> | 创建文件夹 |
| upload <local> <remote> | 上传文件 |
| rm <path> | 删除文件 |
| mv <src> <dst> | 移动文件 |
| search <keyword> [path] | 搜索 |
| whoami | 当前用户 |

## 项目结构

```
alist-cli/
├── README.md
├── SKILL.md
├── scripts/
│   └── alist_cli.py
└── references/
    └── openapi.json
```

## License

CC BY 4.0 - 必须著名来源，允许自由使用
