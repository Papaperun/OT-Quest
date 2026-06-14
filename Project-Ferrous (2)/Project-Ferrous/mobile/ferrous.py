#!/usr/bin/env python3
"""
Project Ferrous — Tier 2 Mobile CLI Field Recon Engine
OT-Quest | Joshua Brunner | Class A Water Treatment Operator

Unified Live Infrastructure and Local Simulation Build.
Pulls position data, tracks perimeter deltas, queries threat matrices,
and cross-references discoveries against localized asset/CVE databases.
"""

import json
import subprocess
import time
import sys
import requests
import shodan

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SHODAN_API_KEY   = "YOUR_SHODAN_API_KEY"  # Requires Shodan Membership Tier
SEARCH_RADIUS    = 1        # Kilometers around current physical position
MAX_RESULTS      = 5        # Maximum exposure records to render on screen
POLL_INTERVAL    = 10       # Dropped to 10s for snappier bench testing/simulation
DISTANCE_GATE    = 0.05     # Minimum movement delta (50 meters) before re-querying

# Targeted Industrial Operational Technology Ports
OT_PORTS = "port:502,47808,1911,20000,102"

# ─── SIMULATION MOCK DATA LAYER (PLACEHOLDER DATABASE) ────────────────────────
MOCK_GPS_INDEX = 0
MOCK_GPS_ROUTE = [
    (30.6150, -97.6600),  # Checkpoint 1: Nearing Booster Station
    (30.6123, -97.6543),  # Checkpoint 2: Directly outside Water Plant
    (30.6200, -97.6700),  # Checkpoint 3: Elevated Tank Zone
    (30.6500, -97.7000)   # Checkpoint 4: Clear Perimeter Zone
]

MOCK_THREAT_DATABASE = {
    "30.6150,-97.6600": {
        "total": 1,
        "matches": [{
            "ip_str": "192.168.42.11", "port": 502, "org": "Municipal Water District",
            "location": {"city": "Booster Station 1"},
            "data": "Protocol: Modbus TCP\nFunction Codes Supported: 01, 02, 03, 04, 05, 06\nDevice: Schneider Quantum PLC"
        }]
    },
    "30.6123,-97.6543": {
        "total": 2,
        "matches": [
            {
                "ip_str": "10.240.12.5", "port": 102, "org": "City Utility Grid Operations",
                "location": {"city": "Water Plant Primary Intake"},
                "data": "Protocol: Siemens S7 (ISO-on-TCP)\nComponent: S7-300 CPU\nFirmware: v3.2.1\nCRITICAL: CVE-2022-38773 (CVSS 9.8) - Active Exploit Known"
            },
            {
                "ip_str": "10.240.12.6", "port": 1911, "org": "City Utility Grid Operations",
                "location": {"city": "Water Plant High Service Pumps"},
                "data": "Protocol: Tridium Niagara Fox\nVersion: 4.10.0.154\nAuth: Unencrypted Cleartext"
            }
        ]
    },
    "30.6200,-97.6700": {
        "total": 1,
        "matches": [{
            "ip_str": "172.16.89.4", "port": 47808, "org": "County Water Infrastructure",
            "location": {"city": "Elevated Storage Tank telemetry"},
            "data": "Protocol: BACnet IP\nVendor: Delta Controls\nObject Name: Tank_Level_Transmitter"
        }]
    }
}

# ─── GEOSPATIAL MATH (HAVERSINE) ──────────────────────────────────────────────
def distance_km(lat1, lon1, lat2, lon2):
    """Calculates the absolute distance delta between two coordinate pairs."""
    import math
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ─── HARDWARE INTERFACES (LIVE vs SIMULATION) ─────────────────────────────────
def get_device_gps_LIVE():
    """Pulls current location directly from phone hardware via Termux API."""
    cmd = ["termux-location", "-p", "gps", "-r", "once"]
    proc = None
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(timeout=25)
        if proc.returncode != 0:
            return None, None
        data = json.loads(stdout.decode("utf-8"))
        return data["latitude"], data["longitude"]
    except subprocess.TimeoutExpired:
        print("  [-] GPS Hardware Timeout — Satellite lock dropped or obscured.")
        if proc:
            proc.kill()
            proc.wait()
        return None, None
    except Exception as e:
        print(f"  [-] Local Location Framework Error: {e}")
        return None, None

def get_device_gps_SIMULATED():
    """Simulates a field walk by stepping through predefined test coordinates."""
    global MOCK_GPS_INDEX
    lat, lon = MOCK_GPS_ROUTE[MOCK_GPS_INDEX]
    MOCK_GPS_INDEX = (MOCK_GPS_INDEX + 1) % len(MOCK_GPS_ROUTE)
    print(f"  [SIMULATOR] Stepping to next route sector vector...")
    return lat, lon

# ─── DATA RETRIEVAL INTERFACES (LIVE vs SIMULATION) ───────────────────────────
def query_shodan_LIVE(api, lat, lon):
    """Executes a live geo-contextualized search via Shodan API."""
    query_string = f"geo:{lat:.4f},{lon:.4f},{SEARCH_RADIUS} {OT_PORTS}"
    print(f"  [API] Dispatching Shodan Outbound Query: \"{query_string}\"")
    try:
        results = api.search(query_string)
        return results
    except shodan.APIError as e:
        print(f"  [!] Shodan API Authentication/Tier Error: {e}")
        return None
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("  [!] Connection Interrupted — Device operating in air-gapped field fallback.")
        return None

def query_shodan_SIMULATED(api, lat, lon):
    """Intercepts queries locally and serves mock threat data."""
    key = f"{lat:.4f},{lon:.4f}"
    print(f"  [SIMULATOR] Intercepting geo-query for zone: {key}")
    time.sleep(1)
    return MOCK_THREAT_DATABASE.get(key, {"total": 0, "matches": []})

# ─── REPORT OUTPUT ────────────────────────────────────────────────────────────
def print_report(results, lat, lon):
    """Renders contextual asset findings to CLI."""
    if not results:
        return

    print(f"\n  {'+'*54}")
    print(f"  TACTICAL INTEL REPORT | GRID: {lat:.4f}, {lon:.4f}")
    print(f"  TOTAL EXPOSURES IN CELL BOUNDARY: {results['total']}")
    print(f"  {'+'*54}")

    if results['total'] == 0:
        print("  [SECURE] No public internet exposure signatures at this grid footprint.\n")
        return

    for i, match in enumerate(results['matches'][:MAX_RESULTS]):
        print(f"\n  [{i+1}] EXPOSURE NODE: {match['ip_str']}:{match['port']}")
        print(f"      Organization : {match.get('org', 'Unlisted Signature')}")
        print(f"      Facility     : {match.get('location', {}).get('city', 'Unknown')}")
        banner = match.get('data', '').strip().replace('\n', ' | ')
        print(f"      Payload      : {banner[:100]}...")
        print(f"      {'-'*50}")

# ─── MAIN ENGINE ──────────────────────────────────────────────────────────────
def main():
    print("\n  ==================================================")
    print("  PROJECT FERROUS — MOBILE OT FIELD RECON ENGINE")
    print("  OT-Quest | Authorized Use Only")
    print("  ==================================================\n")

    api = None

    # ─── RUNTIME TOGGLE ───────────────────────────────────────────────────────
    # STATE A: SIMULATION MODE (default — safe for demo)
    print("  [RUN CONFIG] SIMULATION BENCH TEST ACTIVE\n")
    get_position  = get_device_gps_SIMULATED
    fetch_threats = query_shodan_SIMULATED

    # STATE B: LIVE FIELD MODE (uncomment below to go live)
    # print("  [RUN CONFIG] LIVE WIRE FIELD CAPTURE ACTIVE\n")
    # if SHODAN_API_KEY == "YOUR_SHODAN_API_KEY":
    #     print("  [ERROR] Provide an authorized Shodan API key.")
    #     sys.exit(1)
    # api = shodan.Shodan(SHODAN_API_KEY)
    # get_position  = get_device_gps_LIVE
    # fetch_threats = query_shodan_LIVE
    # ──────────────────────────────────────────────────────────────────────────

    last_lat = None
    last_lon = None

    print(f"  [*] Core Engine Online. Poll interval: {POLL_INTERVAL}s")
    print(f"  [*] Distance gate: {DISTANCE_GATE * 1000}m")
    print(f"  [!] Press Ctrl+C to safely disarm.\n")

    while True:
        try:
            print("[*] Monitoring perimeter vector changes...")
            lat, lon = get_position()

            if lat is None or lon is None:
                time.sleep(POLL_INTERVAL)
                continue

            if last_lat is not None:
                dist = distance_km(last_lat, last_lon, lat, lon)
                if dist < DISTANCE_GATE:
                    print(f"  [~] Position static (delta: {dist*1000:.1f}m). Holding.")
                    time.sleep(POLL_INTERVAL)
                    continue

            print(f"  [+] Position: {lat:.4f}, {lon:.4f}")
            results = fetch_threats(api, lat, lon)

            if results:
                print_report(results, lat, lon)

            last_lat = lat
            last_lon = lon

            print(f"  [*] Cycle complete. Next in {POLL_INTERVAL}s...\n")
            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n  [*] Engine disarmed. Stay authorized out there.\n")
            sys.exit(0)
        except Exception as e:
            print(f"  [CRITICAL] Core loop error: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
