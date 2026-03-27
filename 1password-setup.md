# 在宿主机安装 1Password CLI 并挂载到 Docker 容器

## 步骤 1: 安装 1Password CLI

### macOS
```bash
brew install --cask 1password-cli
```

### Linux (Ubuntu/Debian)
```bash
# 添加仓库
curl -sS https://downloads.1password.com/linux/keys/1password.asc | sudo gpg --dearmor -o /usr/share/keyrings/1password-archive-keyring.gpg

echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian stable main' | sudo tee /etc/apt/sources.list.d/1password.list

sudo apt update && sudo apt install 1password-cli
```

### Windows
```bash
winget install 1Password.1password
```

---

## 步骤 2: 登录 1Password

```bash
# 首次登录（需要打开 1Password App 授权）
op signin

# 验证
op whoami
```

---

## 步骤 3: 创建凭据 Item（可选）

如果还没有，创建存储 token 的 item：

```bash
# 创建 Login item（如果需要）
op item create --category Login --title "GitHub Token" --url "github.com" --field username=KinemaClaw --field password=<你的token>

op item create --category Login --title "AList Token" --url "https://cloud.xn--30q18ry71c.com" --field username=claw --field password=<你的密码>
```

---

## 步骤 4: 挂载到 Docker 容器

### 4.1 创建配置目录
```bash
mkdir -p ~/.config/op
```

### 4.2 修改 Docker Compose

编辑 `docker-compose.yml`：

```yaml
version: '3.3'
services:
  openclaw:
    image: ...
    volumes:
      - ~/.config/op:/home/node/.config/op:ro    # 1Password CLI 配置（只读）
      - /run/1password:/run/1password:ro       # 1Password Socket（只读）
    environment:
      - OP_CONNECT_INTEGRATION_TOKEN=<你的token>  # 可选：用于自动化
```

### 4.3 重新创建容器
```bash
docker compose down
docker compose up -d
```

---

## 步骤 5: 在容器中使用

```bash
# 验证
docker exec -it <container> op whoami

# 读取凭据
docker exec -it <container> op read "op://GitHub Token/password"
docker exec -it <container> op read "op://AList Token/password"
```

---

## 常见问题

### Q: 提示 "not signed in"
A: 需要在宿主机先运行 `op signin` 登录，确保 1Password App 已解锁。

### Q: Socket 路径不对
A: 检查 1Password 设置中的 Socket 位置，Linux 通常是 `/run/1password`。

### Q: 容器内无法运行 op
A: 确保挂载了 `~/.config/op` 目录。

---

## 参考

- [1Password CLI 官方文档](https://developer.1password.com/docs/cli/)
- [Docker 集成](https://developer.1password.com/docs/cli/docker)
