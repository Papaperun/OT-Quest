# Project Ferrous — Bill of Materials & Sources
**Procurement Index & Library Dependencies**

---

## Hardware Components (Tier 3)

| Component | Specification | Source |
|-----------|--------------|--------|
| ESP32 Smart Display (CYD) | ESP32-2432S028R, 2.8" TFT LCD, Resistive Touch, Type-C USB | AliExpress / Amazon: `"ESP32-2432S028R Choice"` |
| GPS Module | u-blox NEO-6M (GY-NEO6MV2) with external ceramic patch antenna | AliExpress / DIYmalls: `"GY-NEO6MV2 GPS Module"` |
| GPS Add-on Board (optional) | HedgeTech/Elecrow CYD 2.8" Battery + GPS No-Solder Daughterboard | Tindie / Elecrow: `"CYD Marauder Battery GPS Mod"` |
| LiPo Battery | 3.7V 1100mAh, 1.25mm JST Connector (Model 603443) | Amazon / Hobby retailers: `"3.7V LiPo 1100mAh 1.25mm JST"` |

---

## Pin Connections — CYD CN1 Expansion Bus

```
CYD CN1 Pin 1 (VCC)      ----> GPS VCC
CYD CN1 Pin 2 (GPIO 27)  ----> GPS RX
CYD CN1 Pin 3 (GPIO 22)  <---- GPS TX
CYD CN1 Pin 4 (GND)      ----> GPS GND
```

---

## Firmware Libraries (Tier 3 — Arduino/ESP32)

| Library | Purpose | Source |
|---------|---------|--------|
| TinyGPS++ v1.0.3+ | Parses NMEA stream from GPS UART | [github.com/mikalhart/TinyGPSPlus](https://github.com/mikalhart/TinyGPSPlus) |
| TFT_eSPI v2.5.0+ | Hardware display driver for ILI9341 SPI screens | [github.com/Bodmer/TFT_eSPI](https://github.com/Bodmer/TFT_eSPI) |
| ArduinoJson v6.x/7.x | Low-allocation JSON parsing, prevents heap fragmentation | [arduinojson.org](https://arduinojson.org) |
| WiFi.h | ESP32 WiFi (built-in) | Arduino Library Manager |
| HTTPClient.h | HTTP requests (built-in ESP32) | Arduino Library Manager |

---

## Software Stack (Tier 2 — Android/Python)

| Software | Purpose | Source |
|----------|---------|--------|
| Termux | Native terminal / sandboxed Linux on Android | [f-droid.org](https://f-droid.org/packages/com.termux/) |
| Termux:API | Bridges scripts to hardware (GPS, camera, etc.) | [f-droid.org](https://f-droid.org/packages/com.termux.api/) |
| shodan-python | Official Shodan API Python library | `pip install shodan` |

---

## Shodan API Tiers

| Tier | Cost | Notes |
|------|------|-------|
| Free | $0 | 100 results/query, no real-time data |
| Membership | ~$69 one-time | Unlimited queries, filters, real-time — sufficient for this tool |
| API Plan | Monthly subscription | Full commercial use |

---

## 3D Printed Enclosures

| Asset | Description | Source |
|-------|-------------|--------|
| CYD Portable Case | Snap-fit housing for CYD + battery | Thingiverse / MakerWorld: `"CYD Portable Battery Case"` |

---

## Conceptual Origin

The aviation tracking reference that inspired the geo-query architecture:
- ESP32-based ADS-B aircraft trackers (open-source community)
- Demonstrated that sub-$20 hardware could process live wireless telemetry and render it dynamically

---

*OT-Quest | [github.com/Papaperun/OT-Quest](https://github.com/Papaperun/OT-Quest)*
