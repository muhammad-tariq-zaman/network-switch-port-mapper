import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import analyse

def row(switch, port, vlan, device, mac=""):
    return {"switch": switch, "port": port, "vlan": vlan, "device": device, "mac": mac}

class TestSwitchPortMapper(unittest.TestCase):
    def test_empty_port_flagged(self):
        r = analyse([row("SW-1", "Gi0/1", "10", "")])
        self.assertEqual(r["empty"], [("SW-1", "Gi0/1", "10")])
    def test_device_port_not_empty(self):
        r = analyse([row("SW-1", "Gi0/1", "10", "PC-1", "aa:bb:cc:00:00:01")])
        self.assertEqual(r["empty"], [])
    def test_mac_conflict_found(self):
        r = analyse([row("SW-1", "Gi0/1", "10", "PC-1", "aa:bb:cc:00:00:01"),
                     row("SW-2", "Gi0/5", "10", "PC-2", "AA:BB:CC:00:00:01")])
        self.assertEqual(r["conflicts"]["aa:bb:cc:00:00:01"],
                         [("SW-1", "Gi0/1"), ("SW-2", "Gi0/5")])
    def test_same_mac_same_port_not_conflict(self):
        r = analyse([row("SW-1", "Gi0/1", "10", "PC-1", "aa:bb:cc:00:00:01")])
        self.assertEqual(r["conflicts"], {})
    def test_vlan_grouping(self):
        r = analyse([row("SW-1", "Gi0/1", "10", "PC-1"), row("SW-1", "Gi0/2", "20", "PC-2")])
        self.assertEqual(sorted(r["switches"]["SW-1"]), ["10", "20"])
    def test_empty_input(self):
        r = analyse([])
        self.assertEqual((r["switches"], r["empty"], r["conflicts"]), ({}, [], {}))
