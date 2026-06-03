# Fix: Duplicated Line-Number Artifacts in Vault Files

## Problem

Vault files edited via tooling can develop duplicated line-number prefixes on every line:

```
    1|    1|---
    2|    2|tags:
    3|    3|  - "#机器学习"
```

This happens when a merge operation injects its line-number markers into the actual file bytes.

## Fix Recipe

Read raw bytes with `cat` (not `read_file`, which hides the corruption in display rendering), then strip all leading `N|` patterns:

```python
import subprocess, re

path = "/path/to/corrupted/file.md"
result = subprocess.run(["cat", path], capture_output=True, text=True)
lines = result.stdout.split('\n')

fixed_lines = []
for line in lines:
    stripped = re.sub(r'^\s+\d+\|', '', line)
    fixed_lines.append(stripped)

fixed_content = '\n'.join(fixed_lines)

from hermes_tools import write_file
write_file(path, fixed_content)
```

## Why `read_file` Doesn't Help

`read_file` adds its own display prefixes like `    1|content` — this is rendering, not file bytes. If the file is already corrupted, you see `    1|    1|content` and can't tell which prefix is real and which is display. Always use `cat` to inspect the raw content first.

## Verification

After fixing, the file should have clean markdown — no leading numbers, no pipe characters before content. Check the first 15 lines with the same `cat` approach.
