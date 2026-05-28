# AList CLI for OpenClaw

基于 AList API 的文件管理 CLI 工具，支持上传、下载、搜索、直链获取，认证令牌自动管理。

## 功能

- 文件上传/下载
- 文件列表浏览
- 创建文件夹、删除、移动文件
- 文件搜索
- 获取文件预览链接和下载直链
- 自动登录认证 + 令牌自动刷新

## 适用场景

- 通过对话管理 AList 云存储文件
- 上传文件并获取分享链接
- 搜索和浏览远程存储

## 使用方式

本 skill 为 OpenClaw/Claude Code 技能，安装后可通过对话触发：

```
上传这个文件到云存储
帮我看看 /public/docs 下有什么文件
搜索一下 xxx 相关的文件
把文件分享给别人
```

首次使用需完成 [ONBOARDING.md](ONBOARDING.md) 配置（设置环境变量和安装脚本）。

## 命令列表

| 命令 | 说明 |
|------|------|
| `login` | 登录认证 |
| `ls [path]` | 列出文件 |
| `upload <local> <remote>` | 上传文件 |
| `get <path>` | 获取文件信息 |
| `url <path>` | 获取预览/下载链接 |
| `mkdir <path>` | 创建文件夹 |
| `rm <path>` | 删除文件 |
| `mv <src> <dst>` | 移动文件 |
| `search <keyword>` | 搜索文件 |
| `whoami` | 当前用户 |

## 项目结构

```
alist-cli/
├── SKILL.md
├── ONBOARDING.md
├── scripts/
│   └── alist_cli.py
└── references/
    └── openapi.json
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)
