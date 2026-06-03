# Fast Note Sync 诊断与修复指南

## 架构概览

- **插件ID**: `fast-note-sync`
- **GitHub 插件**: `haierkeys/obsidian-fast-note-sync`
- **服务端 Docker 镜像**: `haierkeys/fast-note-sync-service:latest`
- **容器名**: `fast-note-sync-service`
- **端口**: 9000 (HTTP/WebSocket), 9001 (private HTTP)
- **数据库**: SQLite, 容器内 `/fast-note-sync/storage/database/db.sqlite3`
- **配置文件**: `/fast-note-sync/config/config.yaml`
- **用户数据库按 uid 分片**: `db_user_{uid}.sqlite3`, `db_user_folder_{uid}.sqlite3`, `db_user_file_{uid}.sqlite3` 等

## 快速诊断三板斧

```bash
# 1. 容器是否运行
docker ps --filter "name=fast-note-sync-service"

# 2. 最近的日志（看错误）
docker logs fast-note-sync-service --tail 50 2>&1 | grep -iE "error|fail|unauth|malformed"

# 3. 健康检查
curl -s http://localhost:9000/api/health
```

## Token 认证问题（最常见故障）

### 症状

日志中出现：
```
WS Authorization FAILD  {"error": "token is malformed: token contains an invalid number of segments"}
WS Client Leave (Unauth)
```

插件 WebSocket 同步状态显示"未连接"或"认证失败"。

### 根因

插件更新后（如 v2.0.16），插件持有的 token 与服务端不匹配。可能原因：
- Token 过期（默认 7 天，见 config.yaml `security.token-expiry: 7d`）
- 插件版本升级后 token 格式变化
- 插件未曾正确配置过 token（数据库中只有 WebGui token，无 ObsidianPlugin token）

### 修复步骤

1. **打开 Web 管理页面** — 浏览器访问 `http://localhost:9000`，登录
2. **生成/重建插件 token** — 在 Tokens 页面，创建一个 scope 包含 `p:rest` + `c:ObsidianPlugin` 的新 token
3. **删除旧 token** — 如果存在旧的 plugin token 先删掉
4. **复制新 token 到插件** — Obsidian 设置 → Fast Note Sync → Auth Token 字段粘贴
5. **验证** — `docker logs -f fast-note-sync-service` 不再出现 malformed 错误

### 直接查看数据库中的 token

```bash
# 导出数据库
docker cp fast-note-sync-service:/fast-note-sync/storage/database/db.sqlite3 /tmp/

# 用 Python 检查
python3 -c "
import sqlite3
conn = sqlite3.connect('/tmp/db.sqlite3')
cur = conn.execute('SELECT id, uid, token_string, scope, client_type, status, expired_at FROM auth_token')
for r in cur: print(r)
"
```

如果只看到 `client_type=WebGui` 的 token，没有 `ObsidianPlugin` 的 —— 说明插件从未正确配过 token。

### 直接注入 token 到数据库（无需 Web GUI）

当用户找不到 Web GUI 或无法通过界面操作时，可以直接往 SQLite 数据库写入 token：

```python
import sqlite3, subprocess, tempfile, os, json, base64

# 从容器导出数据库
tmpdir = tempfile.mkdtemp()
subprocess.run(["docker", "cp", "fast-note-sync-service:/fast-note-sync/storage/database/db.sqlite3", tmpdir], check=True)
db_path = os.path.join(tmpdir, "db.sqlite3")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 解码 JWT payload 获取 tokenId 和过期时间
token = "<用户提供的 JWT token>"
payload_b64 = token.split('.')[1]
payload_b64 += '=' * (4 - len(payload_b64) % 4)
payload = json.loads(base64.urlsafe_b64decode(payload_b64))
token_id = payload['tokenId']
uid = payload['uid']
exp_dt = datetime.fromtimestamp(payload['exp']).strftime('%Y-%m-%d %H:%M:%S')

# 插入或更新
cur.execute("SELECT id FROM auth_token WHERE id = ?", (token_id,))
if cur.fetchone():
    cur.execute("UPDATE auth_token SET token_string=?, scope='p:rest c:ObsidianPlugin f:*', client_type='ObsidianPlugin', status=1, expired_at=?, updated_at=datetime('now') WHERE id=?", (token, exp_dt, token_id))
else:
    cur.execute("INSERT INTO auth_token (id,uid,token_string,scope,client_type,status,issue_type,expired_at,created_at,updated_at) VALUES (?,?,?,'p:rest c:ObsidianPlugin f:*','ObsidianPlugin',1,2,?,datetime('now'),datetime('now'))", (token_id, uid, token, exp_dt))

conn.commit()
conn.close()
subprocess.run(["docker", "cp", tmpdir + "/db.sqlite3", "fast-note-sync-service:/fast-note-sync/storage/database/db.sqlite3"], check=True)
```

**关键点**：
- Token scope 必须匹配：`p:rest c:ObsidianPlugin f:*` 是插件需要的格式
- `auth-token-key` 在 config.yaml 中是 `fast-note-sync-Auth-Token`，JWT 用这个密钥签名
- 数据库写入后，插件端也需要同步更新 `data.json` 中的 `apiToken` 字段，重启 Obsidian 后生效

## 插件配置检查

```bash
VAULT="<vault path>"

# 插件是否启用
grep "fast-note-sync" "$VAULT/.obsidian/community-plugins.json"

# 插件配置
cat "$VAULT/.obsidian/plugins/fast-note-sync/data.json"

# 插件版本
cat "$VAULT/.obsidian/plugins/fast-note-sync/manifest.json" | grep version

# 发现插件期望的配置字段名（版本间可能变化）
grep -oP '"(api|apiToken|vault|serverUrl|remoteUrl|token)"' "$VAULT/.obsidian/plugins/fast-note-sync/main.js" | sort -u
```

版本升级后字段名可能变化（如 `serverUrl` → `api`），用 grep 扫描 main.js 确认当前版本实际期望的字段名再手动补入 data.json。

**注意**: v2.0.16 升级后 `data.json` 常常缺少 `api`、`apiToken`、`vault` 三个字段，导致插件连不上服务器。插件代码从 `this.plugin.settings` 读取这些值（见 main.js 中 `let{api:s,vault:r,apiToken:a,...}=this.plugin.settings`），如果 data.json 里没有，插件就无目标可连。修复方法是直接在 data.json 末尾补上：

```json
  "api": "http://localhost:9000",
  "apiToken": "<JWT token>",
  "vault": "wbaoc-wiki"
```

可以用 `patch` 工具追加到最后一个字段后面（在 closing `}` 前加逗号）。

## 服务端自身更新

容器内有两个二进制：`fast-note-sync-service`（当前）和 `fast-note-sync-service.old`（旧版备份）。服务端可能自动更新过。

镜像更新：
```bash
docker pull haierkeys/fast-note-sync-service:latest
docker stop fast-note-sync-service
docker rm fast-note-sync-service
# 重新启动（用原来的参数/docker-compose）
```

## 常见问题速查

| 症状 | 原因 | 解决 |
|------|------|------|
| `token malformed: invalid number of segments` | 插件 token 过期/格式错误 | Web GUI 重新生成 token |
| `WS Client Leave (Unauth)` | 同上，WebSocket 认证失败 | 同上 |
| data.json 无 `api`/`apiToken`/`vault` 字段 | 插件升级后配置丢失 | 直接 patch data.json 补上三字段 + DB 注入 token，重启 Obsidian |
| Docker 容器不在 | Mac 未开机/Docker Desktop 没启动 | `docker ps -a` 确认；考虑迁移 VPS |
| 手机装不了插件 | Safe Mode 未关闭 | Settings → Community plugins → Turn off Safe Mode |
| 手机同步慢 | 网络 + WebSocket 延迟 | 手机端用只读模式避免冲突 |

## VPS 部署

```bash
git clone https://github.com/haierkeys/obsidian-fast-note-sync-service.git
cd obsidian-fast-note-sync-service
docker compose up -d
# 启动后输出授权配置 JSON → 复制到各设备插件设置
```

## 多设备策略

- **Mac（主设备）**: 读写模式
- **手机/平板**: 只读模式（`readonlySyncEnabled: true`），避免移动端误操作冲突
- **服务端 URL**: 用域名 + HTTPS（Nginx 反代），不要裸 IP
