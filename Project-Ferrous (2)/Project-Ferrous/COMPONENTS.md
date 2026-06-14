# Project Ferrous — Components & Build Evolution
**OT-Quest | Joshua Brunner**

---

## How I Got Here

I didn't start with a shopping list. I started with an idea and worked backward.

When I first saw the ESP32 aircraft tracker that inspired this project, I did what any reasonable person does — I looked at what they used. Breadboard, jumper wires, a microcontroller, a small display. Standard hobbyist stack. I started pricing it out.

Then I looked at the CYD — the ESP32 Cheap Yellow Display — and realized it already had almost everything built in. Screen, ESP32, USB, touch. The only things missing were a battery and a GPS module. So I priced those two parts instead of a whole component list and immediately cut the build complexity in half.

Then I looked at the GPS module price and thought — wait. If I've already got a phone in my pocket, I've already got GPS. A Python script in Termux and Termux:API gives me everything the hardware does, for free, on a device I'm already carrying. Tier 2 was born out of me being practical, not clever.

Then I hit the Shodan wall. The geo filter needs a paid membership. And I'm standing there thinking about the cost and I realize — I don't actually need the API at all for the most basic version. I can Google my GPS coordinates and paste them into Shodan manually in a browser. Zero cost. Zero hardware. Tier 1 was literally me finding the floor.

That's how you get three tiers. Not from an architecture diagram. From asking "what's the cheapest version of this that still works" at every step.

---

## Tier 1 — The Free Version
**Cost: $0**

No hardware. No API subscription required for basic use.

- Any device with a browser
- Google Maps or phone GPS for coordinates
- Shodan free account for manual queries

**How it works:** Pull your GPS coordinates, manually build a Shodan geo query, read the results. Slow, manual, identity-linked to your browser session — but it works and it costs nothing.

---

## Tier 2 — Phone/Tablet
**Cost: $0 in hardware (software only)**

Runs on any Android device you already own.

| Component | Cost | Source |
|-----------|------|--------|
| Termux | Free | F-Droid |
| Termux:API | Free | F-Droid |
| shodan-python | Free | pip install shodan |
| Shodan Membership | ~$69 one-time | account.shodan.io |

> ⚠️ The geo: filter requires a Shodan Membership. Free tier will not work for automated GPS queries.

**How it works:** ferrous.py pulls your phone's live GPS via Termux:API and fires the Shodan query automatically. No extra hardware. Your phone does everything.

---

## Tier 3 — Dedicated Hardware (CYD Build)
**Cost: $10–30 depending on sourcing**

| Component | Spec | Where to Buy | Est. Cost |
|-----------|------|-------------|-----------|
| ESP32 CYD | ESP32-2432S028R, 2.8" TFT, touch, Type-C | AliExpress: "ESP32-2432S028R Choice" | ~$10–15 |
| GPS Module | GY-NEO6MV2 u-blox NEO-6M | AliExpress / DIYmalls: "GY-NEO6MV2 GPS Module" | ~$3–5 |
| LiPo Battery | 3.7V 1100mAh, 1.25mm JST (Model 603443) | Amazon / hobby retailers | ~$5–8 |
| GPS Add-on (optional) | HedgeTech/Elecrow no-solder daughterboard | Tindie / Elecrow: "CYD Marauder Battery GPS Mod" | varies |
| 3D Printed Case (optional) | Snap-fit CYD + battery housing | Thingiverse / MakerWorld: "CYD Portable Battery Case" | free to print |

> ⚠️ Same Shodan Membership requirement applies. The geo: filter is not free tier.

**Why dedicated hardware:** Your phone has your identity on it. Your personal device creates a digital trail. A $15 CYD is purpose-built, carries no personal accounts, and if the situation requires it — it's disposable. That's the operational reason Tier 3 exists.

---

## Pin Connections — CYD CN1 Expansion Bus

```
CYD CN1 Pin 1 (VCC)      ----> GPS VCC
CYD CN1 Pin 2 (GPIO 27)  ----> GPS RX
CYD CN1 Pin 3 (GPIO 22)  <---- GPS TX
CYD CN1 Pin 4 (GND)      ----> GPS GND
```

No breadboard required. The CN1 header on the CYD gives you direct access to UART and power without cutting a single wire.

---

## Firmware Libraries (Tier 3)

| Library | Purpose | Source |
|---------|---------|--------|
| TinyGPS++ v1.0.3+ | Parses NMEA stream from GPS module | [github.com/mikalhart/TinyGPSPlus](https://github.com/mikalhart/TinyGPSPlus) |
| TFT_eSPI v2.5.0+ | Display driver for ILI9341 screen | [github.com/Bodmer/TFT_eSPI](https://github.com/Bodmer/TFT_eSPI) |
| ArduinoJson v6.x/7.x | JSON parsing for Shodan responses | [arduinojson.org](https://arduinojson.org) |
| WiFi.h | ESP32 WiFi — built in | Arduino Library Manager |
| HTTPClient.h | HTTP requests — built in | Arduino Library Manager |

---

*OT-Quest | [github.com/Papaperun/OT-Quest](https://github.com/Papaperun/OT-Quest)*
