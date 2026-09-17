---
name: ct-ct133-result
description: "CT133 Bad YAML Config — PASS; startup detects invalid YAML, exits code 3, no restart loop"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT133: Bad YAML Config** — PASS

Appended `invalid: yaml: [broken:` to gap_fade_long.yaml. On startup:
```
CRITICAL main — check_strategy_configs: strategy config validation failed: Invalid YAML syntax in config/strategies/gap_fade_long.yaml
CRITICAL main — Startup checks failed: ['invalid_strategy_configs']
systemd: Main process exited, code=exited, status=3/NOTIMPLEMENTED
```

Exit code 3 → systemd does NOT restart (RestartPreventExitStatus=3). Clean HALT behavior.

Related: [[ct-CT103-result]]
