# asset.py
"""Immutable asset model representing an inventory item from any source."""

from typing import Any, Optional


class Asset:
    """A normalized inventory asset with uniform fields across all sources."""

    __slots__ = (
        "asset_id", "hostname", "ip_address", "os",
        "environment", "owner_context", "source", "raw",
    )

    def __init__(
        self,
        asset_id: str = "",
        hostname: str = "",
        ip_address: Optional[str] = None,
        os: Optional[str] = None,
        environment: Optional[str] = None,
        owner_context: Optional[str] = None,
        source: str = "",
        raw: Optional[dict[str, Any]] = None,
    ) -> None:
        self.asset_id = asset_id or ""
        self.hostname = hostname or ""
        self.ip_address = ip_address
        self.os = os
        self.environment = environment
        self.owner_context = owner_context
        self.source = source or ""
        self.raw = raw if raw is not None else {}

    # ── Queries ──────────────────────────────────────────────────────

    def matches(self, query: str) -> bool:
        """Return True if *query* appears in any searchable field (case-insensitive)."""
        q = query.lower()
        return any(
            q in str(v).lower()
            for v in (
                self.asset_id,
                self.hostname,
                self.ip_address,
                self.os,
                self.environment,
                self.owner_context,
                self.source,
            )
            if v is not None
        )

    # ── Serialisation ────────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dict suitable for JSON serialisation."""
        return {
            "asset_id": self.asset_id,
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "os": self.os,
            "environment": self.environment,
            "owner_context": self.owner_context,
            "source": self.source,
        }

    # ── Display ──────────────────────────────────────────────────────

    def summary(self) -> str:
        """Human-readable one-liner."""
        def _fmt(val: Any, fallback: str = "n/a") -> str:
            return str(val) if val is not None else fallback

        return (
            f"[{self.source.upper():<11}] {self.hostname:<25}  "
            f"ip={_fmt(self.ip_address):<15} "
            f"os={_fmt(self.os):<20} "
            f"env={_fmt(self.environment):<12} "
            f"owner={_fmt(self.owner_context)}"
        )

    def __str__(self) -> str:
        return self.summary()

    def __repr__(self) -> str:
        return (
            f"Asset(asset_id={self.asset_id!r}, hostname={self.hostname!r}, "
            f"source={self.source!r})"
        )

    # ── Value semantics ──────────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Asset):
            return NotImplemented
        return (
            self.asset_id == other.asset_id
            and self.hostname == other.hostname
            and self.ip_address == other.ip_address
            and self.source == other.source
        )

    def __hash__(self) -> int:
        return hash((self.asset_id, self.hostname, self.ip_address, self.source))
