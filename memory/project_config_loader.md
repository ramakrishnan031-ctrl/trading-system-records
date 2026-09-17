---
name: config_loader built and locked (CL1–CL6)
description: core/config_loader.py + 8 stub YAMLs + 25 tests green; CL1–CL6 locked
type: project
originSessionId: fed36863-cc65-4721-ae69-4940be7f7ec0
---
core/config_loader.py is built and green as of 2026-04-15.

**What was built:**
- CL1–CL6 locked in docs/locked_decisions.yaml under `config_loader:` section
- requirements.txt created (pyyaml==6.0.3, pydantic==2.13.0) — both already in venv
- config/ directory: 8 stub YAML files created (minimal-valid, all schemas pass)
- core/config_loader.py: all 8 Pydantic schemas + AppConfig + load_all()
- tests/unit/test_config_loader.py: 25 tests, all passing

**Key decisions (locked):**
- CL1: load_all(config_dir: Path = Path("config")) → AppConfig; module-level fn, no singleton
- CL2: Atomic — all 8 files or raises; ConfigMissingError (absent) or ConfigSchemaError (invalid)
- CL3: extra="forbid" on ALL Pydantic models — typos in keys raise immediately
- CL4: SHA-256 per file stored in AppConfig.file_hashes: dict[str, str]
- CL5: yaml.safe_load() only; no env-var expansion; values taken literally
- CL6: All 8 schemas in one file; split to core/config_schemas/ if >600 lines
- broker_product_map.yaml DOES NOT EXIST — product codes embedded in system_config.yaml under product_map: section

**Config files in scope for config_loader (strategies/*.yaml handled separately by strategies/loader.py):**
- system_config.yaml → SystemConfig
- broker_costs.yaml → BrokerCostsConfig
- broker_limits.yaml → BrokerLimitsConfig
- slippage_model.yaml → SlippageConfig
- scoring_weights.yaml → ScoringConfig
- scan_webhook_map.yaml → ScanWebhookMapConfig
- chartink_scanners.yaml → ChartinkScannersConfig
- nse_holidays_2026.yaml → NseHolidaysConfig

**Why:** Phase 0b of startup calls load_all() atomically before any subsystem initializes.

**How to apply:** When building modules that need config, inject the relevant sub-config (e.g. system_config → cfg.system, broker_costs → cfg.broker_costs). Never call load_all() in a module; only main.py does that.
