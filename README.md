# trading-system-records -- READ-ONLY SNAPSHOT OF PROJECT RECORDS

**This repository is a snapshot. It is never a deploy target.** Do not push it to any machine or bare repository.

It holds the records that describe BOTH trading machines (production and testing) and the project itself --
`docs/SYSTEM_MAP.md`, `PATHS.md`, the project memory (rules, hazards, board, ledger, notes), `docs/audit/` and
`_preservation/`. What is in it, what was left out and why, and every redaction: see `SNAPSHOT_MANIFEST.md`.

## Cloning on Windows -- long paths are required

Some paths are too long for Windows' default 260-character limit. Clone with long paths enabled, or the checkout
fails with `Filename too long`:

```
git -c core.longpaths=true clone --config core.longpaths=true https://github.com/ramakrishnan031-ctrl/trading-system-records.git
```

(or once, machine-wide: `git config --global core.longpaths true`). Keep line endings byte-exact as well:
add `--config core.autocrlf=false`.
