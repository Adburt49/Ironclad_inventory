# Ironclad Unified Inventory CLI (Pro Edition)

## Engineering Normalization Layout
This implementation relies on a clean **Adapter Design Pattern** to intake diverse third-party structures into a single internal, immutable application context model:

| Target Model Field | NetBox Key Mapping | Qualys Key Mapping | CrowdStrike Key Mapping |
| :--- | :--- | :--- | :--- |
| **asset_id** | `id` | `asset_id` | `sensor_id` |
| **hostname** | `device_name` | `hostname` | `hostname` |
| **ip_address** | `primary_ip` | `ip_address` | `local_ip` |
| **os** | `platform` | `operating_system` | `os_version` |
| **environment** | `environment` | `asset_group` | *Not Present* |
| **owner_context** | `tenant` | *Not Present* | `logged_in_user` |

## Extended Capability Enhancements (Part 6 Challenges)
The tool features three architectural expansions:
1. **Challenge B (Multi-Attribute Filters):** Isolates specific inventory components via granular command execution criteria flags (`--os`, `--environment`, `--owner`).
2. **Challenge C (Adaptive Formatting Views):** Shifts dynamically between a highly clean layout ASCII table representation and standard structural raw JSON datasets (`--format json`).
3. **Challenge D (Target Network Forensics IP Tracker):** Runs an explicitly optimized reverse tracking algorithm to search for precise exposures across network fields (`find-ip --ip <address>`).
