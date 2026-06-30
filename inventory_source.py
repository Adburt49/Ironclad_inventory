$ cat inventory_source.py
# inventory_source.py
import os
import requests
from typing import Any
from asset import Asset

class InventorySource:
    name: str = "base"

    def __init__(self, api_url: str):
        self.api_url = api_url

    def fetch_raw(self) -> list[dict[str, Any]]:
        headers = {
            "X-API-Key": os.environ.get("IRONCLAD_API_KEY", "cf7bbbd0")
        }
        r = requests.get(self.api_url, headers=headers, timeout=10)
        if r.status_code != 200:
            raise RuntimeError(f"{self.name} fetch failed ({r.status_code}): {r.text[:200]}")
        data = r.json()
        if not isinstance(data, list):
            raise RuntimeError(f"{self.name} returned unexpected JSON (expected list).")
        return data

    def normalize(self, record: dict[str, Any]) -> Asset:
        raise NotImplementedError

    def fetch_assets(self) -> list[Asset]:
        raw = self.fetch_raw()
        results = []
        for each_record in raw:
            try:
                results.append(self.normalize(each_record))
            except Exception as e:
                # Shield runtime parsing from isolated row anomalies
                continue
        return results

class NetboxInventorySource(InventorySource):
    name = "netbox"

    def normalize(self, record: dict[str, Any]) -> Asset:
        return Asset(
            asset_id=str(record.get("id") or record.get("asset_id", "")),
            hostname=str(record.get("device_name") or record.get("hostname", "")),
            ip_address=record.get("primary_ip") or record.get("ip_address"),
            os=record.get("platform") or record.get("os"),
            environment=record.get("environment"),
            owner_context=record.get("tenant") or record.get("owner_context"),
            source=self.name,
            raw=record,
        )

class QualysInventorySource(InventorySource):
    name = "qualys"

    def normalize(self, record: dict[str, Any]) -> Asset:
        return Asset(
            asset_id=str(record.get("asset_id") or record.get("id", "")),
            hostname=str(record.get("hostname") or record.get("device_name", "")),
            ip_address=record.get("ip_address") or record.get("primary_ip"),
            os=record.get("operating_system") or record.get("os"),
            environment=record.get("asset_group") or record.get("environment"),
            owner_context=record.get("owner_context"),
            source=self.name,
            raw=record,
        )

class CrowdstrikeInventorySource(InventorySource):
    name = "crowdstrike"

    def normalize(self, record: dict[str, Any]) -> Asset:
        return Asset(
            asset_id=str(record.get("sensor_id") or record.get("asset_id", "")),
            hostname=str(record.get("hostname", "")),
            ip_address=record.get("local_ip") or record.get("ip_address"),
            os=record.get("os_version") or record.get("os"),
            environment=record.get("environment"),
            owner_context=record.get("logged_in_user") or record.get("owner_context"),
            source=self.name,
            raw=record,
