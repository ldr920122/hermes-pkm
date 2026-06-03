# HTML Dashboard: obsidian:// Protocol Fix

## Problem

When creating HTML dashboards for Obsidian, `obsidian://open?vault=...&file=...` protocol links don't work when the HTML file is opened in a browser via `file://` protocol. This is because `file://` blocks custom protocol handlers entirely — no JS workaround can bypass this security sandbox.

## Solution 1: Local HTTP Server (RECOMMENDED — works 100%)

**The only reliable way** to make `obsidian://` links work from a local HTML file is to serve it via HTTP.

Create a launch script (`启动工作台.sh`) in vault root:

```bash
#!/bin/bash
PORT=8088
VAULT_DIR="/Users/wbaoc/Documents/Obsidian/wbaoc-wiki"
cd "$VAULT_DIR"
python3 -m http.server "$PORT" &>/dev/null &
sleep 1
open "http://localhost:$PORT/工作台.html"
echo "✅ 工作台已打开 · 服务器PID: $!"
echo "   要停止: kill $!"
```

User double-clicks this script → browser opens `http://localhost:8088/工作台.html` → all `obsidian://` links work natively.

**Why this is the only solution:**
- `file://` → browser security blocks custom protocols (obsidian://, mailto:, etc.)
- `http://localhost` → browser treats it as a real web page, allows protocol handlers
- No JS workaround (setTimeout, window.location.href, window.open) can bypass the `file://` security sandbox

## Solution 2: Clipboard Fallback (when HTTP server is not an option)

If user opens HTML directly via `file://` (no server), `obsidian://` links will NOT work. The only fallback is clipboard copy:

```html
<a href="obsidian://open?vault=wbaoc-wiki&file=PATH" 
   class="quick-link" 
   data-path="PATH">
    <span class="quick-link-label">LABEL</span>
    <span class="quick-link-title">TITLE</span>
</a>
```

```javascript
document.querySelectorAll('.quick-link').forEach(link => {
    link.addEventListener('click', async function(e) {
        e.preventDefault();
        const path = this.dataset.path;
        try {
            await navigator.clipboard.writeText(path);
            const titleEl = this.querySelector('.quick-link-title');
            const originalText = titleEl.textContent;
            titleEl.textContent = '✓ 已复制路径';
            this.style.color = 'var(--accent)';
            setTimeout(() => {
                titleEl.textContent = originalText;
                this.style.color = '';
            }, 2000);
        } catch (err) {
            console.log('路径:', path);
        }
    });
    link.style.cursor = 'pointer';
});
```

## Solutions that DO NOT work

These approaches were tried and failed:
- `<a href="obsidian://...">` with no JS → blocked by `file://` security
- `window.location.href = 'obsidian://...'` → blocked by `file://` security
- `window.open('obsidian://...')` → blocked by `file://` security
- setTimeout trick (try protocol, fallback to clipboard) → protocol never fires from `file://`

## Technical Notes

- `obsidian://open?vault=VAULT_NAME&file=FILE_PATH` format
- Vault name must match exactly (case-sensitive)
- File path relative to vault root, NO `.md` extension needed
- For sections/anchors: `obsidian://open?vault=VAULT&file=FILE#SECTION`
- When served via HTTP (`http://localhost`), all obsidian:// links work natively

---

*Last updated: 2026-05-27*
*Source session: HTML工作台链接跳转修复 — 发现 `file://` 完全阻断 `obsidian://` 协议*
