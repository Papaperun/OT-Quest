# SecOT+ Drill Console

A single-file, offline-capable study tool for CompTIA's upcoming SecOT+ exam. Open it in any browser — phone, tablet, or desktop — and it just works. No install, no server, no account.

## What's in here

- **110 review questions** covering all six SecOT+ exam domains:
  1. OT Systems and Safety Foundations
  2. OT Risk Management
  3. OT Threat Intelligence
  4. OT Cybersecurity Architecture, Design, and Engineering
  5. OT Security Operations
  6. OT Incident Management
- Answer choices shuffle automatically on every question, so you can't just memorize "the answer is C"
- A manual **shuffle deck** button to reshuffle the order of remaining questions mid-run
- Score tracking that persists across sessions (saved locally in your browser, on your device only — nothing leaves your phone)
- A live session score vs. an all-time score, so you can see both "how am I doing right now" and "how am I doing overall"

## How to use it

1. Save `secot-plus-drill-console.html` somewhere you can get to from your phone — Dropbox, Google Drive, email to yourself, whatever's easiest.
2. Open the file directly in your phone's browser (tap it from the Dropbox/Drive app, or use "Open in browser").
3. Answer questions. Tap **next** to move on, **shuffle deck** anytime to mix up what's coming.
4. When you finish all 110, you'll get a session score and the option to run the deck again (it reshuffles automatically for the new run).

### Resetting your progress

The **reset all progress** link at the bottom needs two taps as a safety check — first tap arms it and the label changes to "tap again to confirm reset," second tap (within 4 seconds) wipes your all-time score and deck order back to zero. This is permanent and can't be undone.

## A few notes on how it works

- All data lives in your browser's local storage on your device. There's no backend, no analytics, no tracking. If you clear your browser data or switch browsers/devices, your saved progress won't carry over.
- It's a static HTML file — you can rename it, move it, back it up, whatever. It doesn't need internet access to run once it's loaded.
- Built for phone-sized screens first, but works fine on a laptop too.

## Attribution

- **Questions** are the work of [Mike Holcomb](https://mikeholcomb.com) — follow him for more OT/ICS cybersecurity content. These are reproduced here for personal study use with credit.
- **Drill console** (the shuffling, scoring, and UI) was built by Joshua Brunner / OT-Quest using Claude (Anthropic).

## Disclaimer

This is an **unofficial, community-made study tool**. It is not affiliated with, endorsed by, or produced by CompTIA. The official SecOT+ exam has not launched yet (beta exam expected early summer 2026, full release expected November 2026), so exam content, question style, and weighting may differ from what's reflected here by the time the real exam ships. Treat this as a way to drill foundational OT/ICS security concepts, not as a guaranteed predictor of exam content.

## Sharing this

You're welcome to share this file with others studying for SecOT+. If you do, please keep the credit section intact so Mike Holcomb's questions stay attributed to him.
