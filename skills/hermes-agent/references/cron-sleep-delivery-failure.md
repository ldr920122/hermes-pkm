# Cron Job Delivery Failures: macOS Sleep & Network

## Symptom

Cron job runs at scheduled time but delivery fails with DNS errors:

```
last_status: error
last_delivery_error: delivery error: Telegram send failed: httpx.ConnectError: [Errno 8] nodename nor servname provided, or not known
```

## Root Cause

macOS puts the machine to sleep. At the scheduled time, network interfaces are down → DNS resolution fails → delivery of the cron result (Telegram, email, webhook) cannot connect.

The cron scheduler itself runs (it's in-process), but the delivery transport cannot reach external hosts.

## Diagnosis

```bash
hermes cron list | grep -A5 "last_status\|last_delivery_error"
```

Key indicators:
- `last_status: error`
- `last_delivery_error` contains `ConnectError`, `nodename nor servname`, or similar DNS/network errors
- `last_run_at` shows the job DID run at the expected time

## Fix Options

### Option A: Prevent sleep during cron window (recommended)

Use **Amphetamine** (macOS app) to schedule a wake session before cron runs:
- Set a session that keeps Mac awake from e.g. 7:55–8:10 AM
- Free, no scripting needed

### Option B: Shift cron schedule later

If the user naturally wakes the Mac by a certain time, push the cron 30 minutes later:

```bash
hermes cron edit <job_id>
# Change schedule from "0 8 * * *" to "30 8 * * *"
```

### Option C: Run manually on wake (quick fix)

Always works: `hermes cron run <job_id>` after waking the Mac. The cron result will be delivered immediately.

### Option D: Deploy to always-on machine

Move Hermes gateway to a VPS or home server that never sleeps. Cron delivery will work regardless of Mac state.

## Verification

After fixing, trigger a manual run to confirm delivery works:

```bash
hermes cron run <job_id>
# Check: hermes cron list | grep last_status
# Should show "success"
```
