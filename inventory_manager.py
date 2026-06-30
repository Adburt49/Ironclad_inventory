# inventory_manager.py
# inventory_manager.py
from inventory_source import InventorySource
from asset import Asset

class InventoryManager:
    def __init__(self, sources: dict[str, InventorySource]):
        self.sources = sources
        self.assets: list[Asset] = []

    def pull(self, source: str) -> None:
        self.assets.clear()
        if source == "all":
            for src in self.sources.values():
                self.assets.extend(src.fetch_assets())
        else:
            if source not in self.sources:
                raise ValueError(f"Unknown source: {source}")
            self.assets.extend(self.sources[source].fetch_assets())

    def list_assets(self, source: str = "all", os_filter: str = None, env_filter: str = None, owner_filter: str = None) -> list[Asset]:
        assets = list(self.assets) if source == "all" else [a for a in self.assets if a.source == source]

        # Challenge B: Apply target attribute filtering dynamically
        if os_filter:
            assets = [a for a in assets if a.os and os_filter.lower() in a.os.lower()]
        if env_filter:
            assets = [a for a in assets if a.environment and env_filter.lower() in a.environment.lower()]
        if owner_filter:
            assets = [a for a in assets if a.owner_context and owner_filter.lower() in a.owner_context.lower()]

        return assets

    def search(self, query: str, source: str = "all") -> list[Asset]:
        return [a for a in self.list_assets(source) if a.matches(query)]

    # Challenge D: Targeted internal IP scanner lookups
    def find_by_ip(self, ip: str) -> list[Asset]:
        target_ip = ip.strip()
        return [a for a in self.assets if a.ip_address and target_ip == a.ip_address.strip()]

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = {"total": len(self.assets)}
        for a in self.assets:
            counts[a.source] = counts.get(a.source, 0) + 1
        return counts
