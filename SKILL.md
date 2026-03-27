---
name: alist
description: |
  AList file management API. AList is a file listing program that supports multiple storage backends, with features including upload, download, preview, and more.
  Trigger: User asks about file management, upload/download, AList operations.
---

# AList CLI for OpenClaw | AList CLI 文件管理工具

AList API-based file management tool for OpenClaw AI assistant.

基于 AList API 的文件管理工具，供 OpenClaw AI 助手使用。

## Features | 功能

- Login authentication | 登录认证
- File list/browse | 文件列表/浏览
- File upload/download | 文件上传/下载
- Create folder | 创建文件夹
- Delete/move/copy files | 删除/移动/复制文件
- Search files | 搜索文件
- Get direct file links | 获取文件直链
- Offline download | 离线下载

## Installation | 安装

```bash
npm i -g alist-cli
```

## Configuration | 配置

Configure environment variables in `scripts/openclaw-docker.sh`:

在 `scripts/openclaw-docker.sh` 中配置环境变量：

```bash
export ALIST_URL="https://your_alist_server"
export ALIST_USERNAME="your_username"
export ALIST_PASSWORD="your_password"
```

## Usage | 使用方法

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

## CLI Options | CLI 选项

| Command | Description | 说明 |
|---------|-------------|------|
| login \<user\> \<pass\> | Login | 登录 |
| ls [path] | List files | 列出文件 |
| get \<path\> | Get file info | 获取文件信息 |
| mkdir \<path\> | Create folder | 创建文件夹 |
| upload \<local\> \<remote\> | Upload file | 上传文件 |
| rm \<path\> | Delete file | 删除文件 |
| mv \<src\> \<dst\> | Move file | 移动文件 |
| search \<keyword\> [path] | Search | 搜索 |
| whoami | Current user | 当前用户 |

## Project Structure | 项目结构

```
alist-cli/
├── README.md
├── SKILL.md
├── scripts/
│   └── alist_cli.py
└── references/
    └── openapi.json
```

## License | 许可证

CC BY 4.0 - Attribution required, free to use

CC BY 4.0 - 必须著名来源，允许自由使用
