# Lab Report: MicroLogix 1100 Hardware Autopsy
**Date:** 2026-05-02  
**Hardware:** Allen Bradley MicroLogix 1100 — CAT 1763-L16AWA, Series B, FW 14  
**Lab:** OT-Quest Home Lab  
**Status:** PSU Board — Condemned | CPU Board — Intact | Relay Board — Intact

---

## Background

Acquired a decommissioned Allen Bradley MicroLogix 1100 (1763-L16AWA) for home lab use. Unit had been stored in conditions that allowed a snake to nest inside the enclosure. Biological contamination (waste) was present internally prior to acquisition. Unit was non-operational on receipt.

This session documents full disassembly, damage assessment, and forensic analysis of the hardware, with conclusions on repair viability and alternative lab strategy.

---

## Hardware Inventory

| Module | Description | Condition |
|--------|-------------|-----------|
| CPU Board | 1763-L16AWA processor/comms board | **Intact — no visible damage** |
| Relay Output Board | Omron relay array, orange terminal blocks | **Intact — minor surface residue** |
| PSU Board | AC input 100-240VAC, 50-60Hz, 46VA max | **Condemned — biological corrosion** |

---

## Disassembly Process

Unit was opened for internal inspection. Three primary boards were separated for individual assessment:

- Relay output board (top module) with Omron 24VDC relays and orange screw terminal blocks
- CPU/processor board with main logic ICs and communications hardware
- PSU board — AC mains input, internal switching power supply

> 📷 *Image: `img_overview_boards.jpg` — All three boards separated on workbench*

---

## Damage Assessment

### PSU Board — Primary Damage Zone

The PSU board sustained the majority of biological contamination damage. Snake waste is acidic and acts as an electrolytic corrosive agent on copper traces and solder joints over time.

**Findings:**

**Component PC1 (Optocoupler):**
- Biological residue concentrated directly at PC1 location
- Significant corrosion on PCB traces feeding PC1
- Solder joints compromised
- PCB substrate discoloration indicating acid penetration
- Adjacent component U1 (voltage regulator — KA75/VG33A marking) showed corrosion spread to solder joints

> 📷 *Image: `img_pc1_damage_topside.jpg` — PC1 corrosion, trace damage visible*

**Trace Damage:**
- Copper traces below PC1 visibly eaten through
- Corrosion tracked along trace paths from biological acid wicking
- Bottom side of board confirmed trace destruction in same region
- Multiple through-hole pads identified as potential jumper anchor points for repair attempt

> 📷 *Image: `img_trace_damage_underside.jpg` — Underside trace destruction confirmed*

**Heatsink Channel:**
- Biological material accumulated in confined space between heatsink fins and mains transformer
- Material hardened in place — cleaning access severely restricted
- Oxidation visible on heatsink aluminum in affected zone
- Hidden damage beneath heatsink cannot be fully assessed without full heatsink removal

> 📷 *Image: `img_heatsink_contamination.jpg` — Heatsink channel contamination*

**PSU Internal Components (Initial Assessment):**
- Large filter capacitor — intact
- Toroidal inductor (copper coil) — intact
- Mains transformer (yellow enclosure) — intact
- White blobs throughout — confirmed as factory potting compound and conformal coating, NOT contamination
- Actual biological residue concentrated at PC1 zone and heatsink channel

> 📷 *Image: `img_psu_interior.jpg` — PSU board interior overview*

---

### CPU Board — Clean

The processor board showed no significant contamination. Surface residue present but no trace damage or corrosion identified. Board is considered serviceable.

> 📷 *Image: `img_cpu_board.jpg` — CPU board topside*

---

### Relay Output Board — Clean

Omron relay array and terminal blocks showed minor surface residue only. All relay bodies intact. Terminal block screws showed no significant corrosion. Board considered serviceable.

> 📷 *Image: `img_relay_board.jpg` — Relay output board*

---

## Repair Viability Analysis

### Attempted Diagnostics

- Multimeter diode test performed on accessible components
- Visual trace mapping on underside of PSU board
- Through-hole pad identification for potential jumper points

### Repair Path Assessment

| Repair Option | Viability | Notes |
|---------------|-----------|-------|
| PC1 optocoupler replacement | Possible | Component likely PC817 or 4N25 — $2 part |
| Trace jumper repair | Possible | Through-hole pads identified as anchor points |
| Full PSU board repair | Low | Hidden damage under heatsink unknown scope |
| PSU board replacement | Recommended | 1763-L16AWA parts units available on eBay $50-80 |

### Decision

PSU board repair deferred. Scope of hidden damage beneath heatsink cannot be confirmed without full teardown. Risk of undetected shorts on mains-side circuitry is unacceptable for first repair attempt.

**Unit shelved pending future PSU board acquisition or repair skill development.**

---

## Key Technical Observations

1. **Biological waste as corrosive agent** — Snake waste created localized acidic environment sufficient to destroy copper PCB traces over time. Damage was concentrated where waste pooled rather than distributed across the board.

2. **Conformal coating identification** — White silicone potting compound on high-voltage components (capacitors, transformer leads) was initially misidentified as contamination. Important distinction — factory protection measure, not damage indicator.

3. **PCB slot identification** — Linear slots cut into PSU board substrate correctly identified as intentional isolation/ventilation features (creepage distance for mains isolation), not physical damage.

4. **Optocoupler location significance** — PC1 position on PSU board sits at the primary/secondary isolation boundary. Damage at this location is particularly impactful as optocouplers handle feedback control for output voltage regulation.

5. **Damage containment** — Contamination remained largely contained to PSU board. CPU and relay boards survived intact, suggesting the PSU enclosure acted as a partial barrier.

---

## Alternative Lab Strategy

Given the intact CPU board and relay board, and the availability of the official user manual, the following approach was adopted:

**Reference document:** Rockwell Automation Publication 1763-UM001 (MicroLogix 1100 User Manual) — publicly available via Rockwell literature library.

**Lab implementation:**
- Use Raspberry Pi 5 with pymodbus to simulate MicroLogix 1100 behavior
- Calibrate simulation against documented register maps and protocol specs in user manual
- Capture and analyze Modbus TCP traffic in Wireshark
- Document attack scenarios mapped to actual 1763-L16AWA documented behavior

This approach provides equivalent protocol-level learning without dependency on functional hardware, while producing more accurate and documentable results than generic PLC simulation.

---

## MITRE ATT&CK ICS Mapping

| Technique | ID | Relevance to This Unit |
|-----------|-----|----------------------|
| Exploitation of Remote Services | T0866 | DF1/Modbus TCP exposed on 1763-L16AWA |
| Modify Parameter | T0836 | Output coil manipulation via Modbus |
| Unauthorized Command Message | T0855 | Force I/O without HMI authentication |
| Loss of Control | T0827 | PSU failure as availability attack analog |

---

## Lessons Learned

- Always inspect acquired hardware before powering up — biological contamination can cause shorts on first power application
- Conformal coating and potting compound are normal on PSU boards — do not mistake for contamination
- Localized damage assessment requires IPA cleaning before accurate diagnosis
- User manual + Pi simulation is a viable and arguably superior alternative to damaged hardware for protocol-level OT security research
- Real hardware teardown produces documented institutional knowledge regardless of repair outcome

---

## Repository References

- [`turbidity_sim.py`](../turbidity_sim.py) — existing Modbus simulation for cross-reference
- [`scada_lab_v2.py`](../scada_lab_v2.py) — existing SCADA lab Flask application
- Future: `micrologix_sim.py` — 1763-L16AWA accurate simulation based on user manual

---

## Hardware Disposition

| Component | Status | Action |
|-----------|--------|--------|
| PSU Board (1763-L16AWA) | Condemned | Shelved — future repair attempt |
| CPU Board | Intact | Retained — future use if PSU sourced |
| Relay Output Board | Intact | Retained — future use if PSU sourced |
| Unit Label/Documentation | Photographed | Archived in this report |

---

*Lab report generated: 2026-05-02*  
*OT-Quest Home Lab — Joshua Brunner*  
*github.com/Papaperun/OT-Quest*
