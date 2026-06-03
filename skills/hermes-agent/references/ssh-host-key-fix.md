# SSH Host Key Verification Fix

## Problem

When using git with SSH URLs (e.g., `git clone git@github.com:user/repo.git`), you may encounter:

```
No ED25519 host key is known for github.com and you have requested strict checking.
Host key verification failed.
```

This happens when `~/.ssh/known_hosts` doesn't contain the host's public key.

## Solution

### Quick Fix
```bash
# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh

# Add github.com host keys
ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null

# Verify the keys were added
ssh-keygen -lf ~/.ssh/known_hosts | grep github.com
```

### For Other Hosts
```bash
# Replace github.com with the target host
ssh-keyscan hostname >> ~/.ssh/known_hosts 2>/dev/null
```

### Alternative: Use HTTPS
For public repositories, HTTPS is simpler and doesn't require SSH configuration:
```bash
# Instead of SSH
git clone git@github.com:user/repo.git

# Use HTTPS
git clone https://github.com/user/repo.git
```

## When This Happens

- Fresh macOS installation
- New user account
- After clearing `~/.ssh/` directory
- When connecting to a host for the first time

## Security Note

`ssh-keyscan` automatically trusts the host key. For high-security environments, manually verify the fingerprint:

```bash
# Get the fingerprint
ssh-keygen -lf <(ssh-keyscan github.com 2>/dev/null | grep ssh-ed25519)

# Compare with GitHub's published fingerprint at:
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints
```

## Claude Code Plugin Installation

This issue commonly occurs when installing Claude Code plugins from GitHub:

```bash
# Error when installing plugin
/plugin marketplace add Imbad0202/academic-research-skills
# Error: SSH host key is not in your known_hosts file

# Fix: Add github.com to known_hosts first
mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null

# Then retry plugin installation
/plugin marketplace add Imbad0202/academic-research-skills
```