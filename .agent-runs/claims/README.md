# Claims

`uv run awf claim-work --write` records one worker claim per ready item here. Claims keep cron workers separated.

Keep only active top-level `*.json` claim files here. Move historical or stale claim snapshots into dated archive
subdirectories so the workflow's active-claim scan and repo-hygiene directory limits stay focused on current work.
