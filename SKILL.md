---
name: alist-cli
version: 1.1.1
description: |
  AList file management CLI for OpenClaw. Supports upload, download, list, mkdir, rm, mv, search.
  Auth via environment variables with auto-refresh. Trigger: file management, AList operations, upload/download.
---

# AList CLI

AList file management CLI. Auth token managed via environment variables with auto-login and auto-refresh.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ALIST_URL` | ✅ | AList server URL (e.g. `https://your-alist-server`) |
| `ALIST_USERNAME` | ✅ | Login username |
| `ALIST_PASSWORD` | ✅ | Login password |
| `ALIST_AUTH_TOKEN` | ❌ | Auth token (auto-obtained via login, skip manual set) |
| `ALIST_USER_INFO` | ❌ | User info JSON (auto-obtained via login, skip manual set) |

## ⚡ Pre-flight: Ensure Python + Dependencies

**Before running the script, ensure `requests` is available. Follow this order:**

### Step 1: Check if requests is importable

```bash
python3 -c "import requests" 2>/dev/null && echo "OK" || echo "NEED_INSTALL"
```

If "OK", skip to [Run Commands](#run-commands).
If "NEED_INSTALL", proceed to Step 2.

### Step 2: Try system install

```bash
uv pip install --system requests 2>/dev/null \
  || pip3 install requests 2>/dev/null \
  || sudo pip3 install --break-system-packages requests
```

If any succeeds, skip to [Run Commands](#run-commands).
If all fail (PEP 668 / no permissions), proceed to Step 3.

### Step 3: Use uv venv (isolated, no system Python needed)

```bash
# Install uv if missing
command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create venv in skill directory and install deps
SKILL_DIR="<skill_directory>"  # e.g. ~/.openclaw/workspace/skills/alist-cli
cd "$SKILL_DIR" && uv venv .venv && uv pip install requests
```

When using venv, **always** call the script via venv python:

```bash
"$SKILL_DIR/.venv/bin/python" "$SKILL_DIR/scripts/alist_cli.py" <command> [args]
```

## Run Commands

```bash
python3 scripts/alist_cli.py <command> [args]
# or with venv:
# .venv/bin/python scripts/alist_cli.py <command> [args]
```

### Commands

| Command | Description |
|---------|-------------|
| `login [username] [password]` | Login (outputs export statements to source) |
| `ls [path]` | List files |
| `get <path>` | Get file info + raw URL |
| `mkdir <path>` | Create folder |
| `upload <local> <remote>` | Upload file (outputs signed URL) |
| `rm <path>` | Delete file |
| `mv <src> <dst>` | Move file |
| `search <keyword> [path]` | Search files |
| `whoami` | Current user info |

## Auth Behavior

- **Auto-login**: Script checks `ALIST_AUTH_TOKEN` on startup. If missing, auto-logins with `ALIST_USERNAME` + `ALIST_PASSWORD`.
- **Auto-refresh**: If API returns 401, automatically re-logins and retries.
- **Manual login**: `alist login` command outputs `export` statements. User should `eval $(alist login)` or manually `source` them.

## References

- `references/openapi.json` - AList API specification
