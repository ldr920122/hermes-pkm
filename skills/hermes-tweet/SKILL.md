---
name: hermes-tweet
description: |
  Use Hermes Tweet as a companion skill for X/Twitter research, monitoring,
  tweet context, user lookup, follower exports, and reviewed social actions in
  Hermes Agent.
---

# Hermes Tweet

Hermes Tweet connects Hermes Agent workflows to X/Twitter reads, monitoring, and
explicitly gated actions. It pairs naturally with article publishing and
knowledge-work workflows that need current social context before drafting or
distributing content.

## Install

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

## Environment

- `XQUIK_API_KEY` is required for read, lookup, export, and monitoring tools.
- `HERMES_TWEET_ENABLE_ACTIONS=true` is additionally required before post,
  reply, DM, or other action tools are available.

Keep credentials in the Hermes environment. Do not write keys, account material,
or session data into Obsidian notes, examples, or shared skill files.

## Workflow

1. Use read-only tools to collect tweet, reply, user, follower, or monitor
   context.
2. Convert the results into notes with source links, handles, timestamps, and
   query terms.
3. Use the context to support drafts, article distribution, launch monitoring,
   or research updates.
4. Treat any post, reply, or DM as an explicit reviewed action.
5. Confirm the target account, destination, final text, and action gate before
   dispatch.

Repository: <https://github.com/Xquik-dev/hermes-tweet>
