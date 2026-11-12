# network-switch-port-mapper

Map switch ports to VLANs and devices from a CSV: ports grouped by switch and VLAN, EMPTY ports listed, and the same MAC address on more than one port flagged as a MAC CONFLICT.

## How to run

```sh
python3 main.py ports.csv
```

## Example output

```
Switch SW-1:
  VLAN 10:
    Gi0/1: PC-1 (aa:bb:cc:00:00:01)
    Gi0/2: EMPTY
SW-1 Gi0/2 (VLAN 10): EMPTY
1 empty port(s), 0 MAC conflict(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
