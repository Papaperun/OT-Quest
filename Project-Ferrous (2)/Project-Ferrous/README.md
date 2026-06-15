# Project Ferrous
### GPS-Contextualized OT Field Recon Tool
**OT-Quest | Joshua Brunner | Class A Water Treatment Operator | OT Security Researcher**

---

![Project Ferrous Concept](assets/concept-art.png)

> *"Started my rest week reading about ESP32 aircraft trackers. Four hours later I had a three-tier OT field recon architecture. This is apparently what my brain does on days off."*

---

## What This Is

Project Ferrous is a portable, GPS-aware field reconnaissance tool that correlates your physical position with internet-exposed OT assets via the Shodan API. As you move around a facility or site perimeter, the device builds geo-contextualized queries and surfaces exposed industrial control system assets tied to that location.

**Not a spray-and-pray scanner. One targeted query per position. Location is the data layer.**

---

## The Problem It Solves

A desk analyst can query Shodan from a browser. A field assessor walking a water facility perimeter at 0600 cannot — not without a laptop, a setup ritual, and a conspicuous presence.

This tool closes that gap. Passive, pocket-sized, no laptop required. You walk the perimeter. It tells you what's visible from the internet at your exact position — Modbus, BACnet, DNP3, Tridium Fox, Siemens S7 — before you plug anything in.

---

## Three-Tier Architecture

| Tier | Platform | Friction | Use Case |
|------|----------|----------|----------|
| **Tier 1** | Browser + Maps + Shodan | Zero | Desk-bound preliminary footprinting |
| **Tier 2** | Android + Termux + Python | Minimal | Authorized site compliance reviews |
| **Tier 3** | ESP32 CYD + GPS Hardware | Moderate | High-isolation field audits |

No single tier is universally superior. Match your collection method to your operational risk constraints and assessment requirements.

---

## OT Protocol Port Matrix

| Port | Protocol | Systems |
|------|----------|---------|
| 502 | Modbus TCP | PLCs, RTUs, water/wastewater controllers |
| 47808 | BACnet | Building automation, HVAC |
| 1911 | Tridium Fox | Niagara SCADA/BMS platforms |
| 20000 | DNP3 | Utilities, substations |
| 102 | Siemens S7 | Siemens PLCs |

---

## Repository Structure

```
Project-Ferrous/
├── README.md
├── SOURCES.md
├── /firmware
│   └── firmware.ino      # Tier 3 ESP32 C++ implementation
├── /mobile
│   └── ferrous.py          # Tier 2 Android/Termux Python engine
└── /assets
    └── concept-art.png
```

---

## ⚠️ Shodan Requirement

**This tool requires a Shodan Membership (~$69 one-time) or higher.**

The `geo:` filter used for GPS-contextualized queries is **not available on the free tier.** Free accounts will receive an API error on any geo-filtered search.

| Tier | Cost | Works? |
|------|------|--------|
| Free | $0 | ❌ geo filter not supported |
| Membership | ~$69 one-time | ✅ sufficient for field use |
| API Plan | Monthly | ✅ full commercial use |

Get your key at [account.shodan.io](https://account.shodan.io)

---

## MITRE ATT&CK for ICS

Supports pre-engagement reconnaissance mapping to:
- **T0888** — Remote System Information Discovery
- Scoping phase of ICS assessments prior to active testing

---

## A Note on Intent

I've stood at those fences. I know what's on the other side. I built this because defenders need to see what adversaries already see — and they need to see it from the field, not from a desk.

> *"The bad guys already have something better. This just shines a light."*
> 
> — inspired by *Hacking Exposed: Industrial Control Systems*

Project Ferrous exists to give authorized assessors the same situational awareness that threat actors already have. Shodan is public. The exposure is real. This tool surfaces it with operator context and field precision so defenders can act on it.

If your intent isn't an authorized assessment — this isn't for you.

## Legal & Ethical Use

This tool is designed for **authorized security assessments only**. Always obtain written authorization before conducting reconnaissance against any network or facility. Shodan queries are passive — they surface data Shodan has already indexed — but operational security and chain of custody practices apply.

---
## Development Notes

Architecture, threat model, and operational design by Joshua Brunner.
C++ firmware developed with AI assistance (Gemini).
Python mobile layer by Joshua Brunner with AI assistance.
> ⚠️ Live mode has not been personally field-tested by the author 
> due to Shodan Membership requirement. Simulation mode is fully 
> verified. Live mode architecture is sound — test in an authorized 
> environment before operational use.
---

*Part of the [OT-Quest](https://github.com/Papaperun/OT-Quest) research portfolio.*
*Contact: joshua.berryutility@gmail.com | [LinkedIn](https://linkedin.com/in/joshua-brunner-098195270)*
