"""Map switch ports to VLANs and devices, flagging gaps and conflicts.

Usage: python3 main.py ports.csv
CSV columns: switch,port,vlan,device,mac.
- EMPTY: a port with no device recorded.
- MAC CONFLICT: the same MAC address on more than one switch
  port (a device moved, or a loop / spoofed address).
Per switch, ports are grouped by VLAN and listed in port order;
the report ends with the empty ports and MAC conflicts.
"""
import argparse, csv, sys
from collections import defaultdict

def analyse(rows):
    by_switch = defaultdict(lambda: defaultdict(list))
    empty = []
    mac_ports = defaultdict(set)
    for row in rows:
        switch = row["switch"].strip()
        port = row["port"].strip()
        vlan = row["vlan"].strip()
        device = row["device"].strip()
        mac = row["mac"].strip().lower()
        by_switch[switch][vlan].append((port, device, mac))
        if not device:
            empty.append((switch, port, vlan))
        if mac:
            mac_ports[mac].add((switch, port))
    conflicts = {mac: sorted(ports) for mac, ports in mac_ports.items() if len(ports) > 1}
    return {"switches": dict(by_switch), "empty": sorted(empty),
            "conflicts": conflicts}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        result = analyse(list(csv.DictReader(f)))
    for switch in sorted(result["switches"]):
        print(f"Switch {switch}:")
        for vlan in sorted(result["switches"][switch]):
            print(f"  VLAN {vlan}:")
            for port, device, mac in sorted(result["switches"][switch][vlan]):
                detail = device if device else "EMPTY"
                print(f"    {port}: {detail}" + (f" ({mac})" if mac else ""))
    for switch, port, vlan in result["empty"]:
        print(f"{switch} {port} (VLAN {vlan}): EMPTY")
    for mac, ports in sorted(result["conflicts"].items()):
        print(f"MAC {mac}: CONFLICT on {', '.join(f'{s} {p}' for s, p in ports)}")
    print(f"{len(result['empty'])} empty port(s), {len(result['conflicts'])} MAC conflict(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
