# Project Ferrous — Origin Story
**OT-Quest | Joshua Brunner**

---

I was on break.

That's genuinely how this started. I was scrolling Google News the way you do when you've got ten minutes and nowhere to be — the algorithm knows I like tech, knows I mess with ESP32 stuff, so it fed me an article about someone tracking aircraft with a cheap microcontroller and a small display. Cool project. Not really my hobby. But I looked at it anyway.

And then my brain did the thing it does.

Within a few minutes I wasn't thinking about aircraft anymore. I was thinking about what happens when you take that same concept — small device, live data, real-time display — and point it at something that actually matters to me. I've spent 23 years walking facility perimeters. I know what it looks like to stand at a fence at 0600 trying to figure out what you're dealing with before you touch anything. A laptop is conspicuous. A phone is your personal device with your identity attached to it. What if the device in your hand already knew what was exposed at your exact location?

That was the seed.

Over the next few days it evolved fast. Started with an ESP32 and an OLED — same form factor as the aircraft tracker, just pointed at Shodan instead of the sky. Then I thought about the display and priced out the CYD — better graphics, built-in screen, same price range. Then I had the thought that stopped me: if you've got a phone in your pocket anyway, you can run this in Termux with Python and use the phone's own GPS. No hardware required at all.

And then the obvious one: if you just need to check a location manually, you can pull your GPS coordinates and feed them to Shodan in a browser. Zero hardware, zero setup.

That's when I realized this wasn't one tool. It was three. Each one solving the same problem at a different operational risk level — browser for desk work, phone for standard assessments, dedicated hardware for when you need something that can't be traced back to you.

The aircraft tracker was just the spark. The 23 years of knowing what a field assessor actually needs — that's where Project Ferrous came from.

---

*OT-Quest | [github.com/Papaperun/OT-Quest](https://github.com/Papaperun/OT-Quest)*
