# main.py
import argparse
import json
from inventory_source import NetboxInventorySource, QualysInventorySource, CrowdstrikeInventorySource
from inventory_manager import InventoryManager

NETBOX_API_URL = "https://my.api.mockaroo.com/ironclad/netbox/inventory.json"
QUALYS_API_URL = "https://my.api.mockaroo.com/ironclad/qualys/inventory.json"
CROWDSTRIKE_API_URL = "https://my.api.mockaroo.com/ironclad/crowdstrike/inventory.json"

def build_manager() -> InventoryManager:
    sources = {
        "netbox": NetboxInventorySource(NETBOX_API_URL),
        "qualys": QualysInventorySource(QUALYS_API_URL),
        "crowdstrike": CrowdstrikeInventorySource(CROWDSTRIKE_API_URL),
    }
    return InventoryManager(sources)

# Challenge C: Format rendering engine
def render_output(assets: list, output_format: str):
    if output_format == "json":
        json_data = [
            {
                "asset_id": a.asset_id, "hostname": a.hostname, "ip_address": a.ip_address,
                "os": a.os, "environment": a.environment, "owner_context": a.owner_context, "source": a.source
            }
            for a in assets
        ]
        print(json.dumps(json_data, indent=2))
    else:
        # High-visibility enterprise ASCII Table structure
        header = f"{'SOURCE':<12} | {'HOSTNAME':<25} | {'IP ADDRESS':<15} | {'OPERATING SYSTEM':<20} | {'ENV':<12} | {'OWNER'}"
        print(header)
        print("-" * len(header))
        for a in assets:
            print(f"{a.source.upper():<12} | {a.hostname or 'n/a':<25} | {a.ip_address or 'n/a':<15} | {a.os or 'n/a':<20} | {a.environment or 'n/a':<12} | {a.owner_context or 'n/a'}")

def cmd_pull(args) -> None:
    mgr = build_manager()
    mgr.pull(args.source)
    print("Pulled inventory successfully.")
    print("Stats:", mgr.stats())

def cmd_list(args) -> None:
    mgr = build_manager()
    mgr.pull(args.source)
    # Challenge B: Pipeline flags safely down to backend filters
    assets = mgr.list_assets(args.source, os_filter=args.os, env_filter=args.environment, owner_filter=args.owner)
    render_output(assets, args.format)

def cmd_search(args) -> None:
    mgr = build_manager()
    mgr.pull(args.source)
    results = mgr.search(args.query, args.source)
    render_output(results[:args.limit], args.format)

# Challenge D: Forensics command callback loop
def cmd_find_ip(args) -> None:
    mgr = build_manager()
    mgr.pull("all")
    results = mgr.find_by_ip(args.ip)
    print(f"IP Exposure Report for [{args.ip}]: {len(results)} matches located.")
    render_output(results, args.format)

def cmd_stats(args) -> None:
    mgr = build_manager()
    mgr.pull(args.source)
    print("Inventory Engine Statistics:", mgr.stats())

def main():
    p = argparse.ArgumentParser(prog="ironclad-inventory", description="Ironclad Unified Inventory CLI Pro")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_format_arg(parser):
        parser.add_argument("--format", choices=["table", "json"], default="table", help="Data format output style")

    p_pull = sub.add_parser("pull", help="Pull raw records from tracking endpoints")
    p_pull.add_argument("--source", choices=["netbox", "qualys", "crowdstrike", "all"], default="all")
    p_pull.set_defaults(func=cmd_pull)

    p_list = sub.add_parser("list", help="List assets")
    p_list.add_argument("--source", choices=["netbox", "qualys", "crowdstrike", "all"], default="all")
    # Challenge B arguments added:
    p_list.add_argument("--os", help="Filter lists by operating system keyword")
    p_list.add_argument("--environment", help="Filter lists by isolated deployment environment context")
    p_list.add_argument("--owner", help="Filter lists by managing owner identities")
    add_format_arg(p_list)
    p_list.set_defaults(func=cmd_list)

    p_search = sub.add_parser("search", help="Query properties matching substring tokens")
    p_search.add_argument("--source", choices=["netbox", "qualys", "crowdstrike", "all"], default="all")
    p_search.add_argument("--query", required=True)
    p_search.add_argument("--limit", type=int, default=50)
    add_format_arg(p_search)
    p_search.set_defaults(func=cmd_search)

    # Challenge D command parser added:
    p_find_ip = sub.add_parser("find-ip", help="Instantly scan inventory footprints for explicit IP footprints")
    p_find_ip.add_argument("--ip", required=True, help="Target IP signature to evaluate")
    add_format_arg(p_find_ip)
    p_find_ip.set_defaults(func=cmd_find_ip)

    p_stats = sub.add_parser("stats", help="Render global data distribution breakdown summaries")
    p_stats.add_argument("--source", choices=["netbox", "qualys", "crowdstrike", "all"], default="all")
    p_stats.set_defaults(func=cmd_stats)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
