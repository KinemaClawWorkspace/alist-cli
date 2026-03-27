# AList API Skill for OpenClaw

基于 AList API (v3) 的文件管理工具，供 OpenClaw AI 助手使用。

## 功能

- 登录认证
- 文件列表/浏览
- 文件上传/下载
- 创建文件夹
- 删除/移动/复制文件
- 搜索文件
- 获取文件直链
- 离线下载

## 快速开始

### 配置

```yaml
# config.yml
alist:
  url: "https://your-alist.example.com"
  username: "admin"
  password: "your_password"
```

### 使用

```
AList 登录
AList 列出文件 /
AList 上传文件 local.txt 到 /remote.txt
AList 获取直链 /file.txt
AList 创建文件夹 /new_folder
AList 删除 /file.txt
AList 移动 /old.txt 到 /new.txt
AList 搜索 keyword
```

## 文件结构

```
alist-skill/
├── README.md              # 本文件
├── SKILL.md              # 完整技能文档
├── scripts/
│   └── alist_cli.py     # CLI 工具
└── references/
    └── openapi.json      # API 完整规范
```

## API 文档

详见 [SKILL.md](./SKILL.md) 或 [AList 官方文档](https://alist.nn.ci/)。

## License

MIT
