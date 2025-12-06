1. ICS-Specific Incident Response Plan (IRP)
Consider developing an ICS-specific IRP tailored to water/wastewater environments.


Could create a draft now and offer a sanitized version to leadership when things slow down.


Should include: roles, communication procedures, escalation paths, containment strategies, and restoration steps unique to OT.



2. CIRP – Cyber Incident Response Plan
Cyber IRP should integrate with or sit alongside the general risk management plan.


Ideally kept in the same binder as the ICS IRP for quick reference.


Sections to include: threat identification, initial triage, log collection, notifications, backups, tabletop exercises.



3. DFIR – Digital Forensics & Incident Response
Focus on log preservation, chain-of-custody, and identifying root cause after an event.


Consider how this fits within a water utility environment: PLC logs, historian data, HMI changes, network activity.


Question to explore:
 Would using a Modbus server simulator/log collector help centralize or retain protocol-level data for DFIR?


It might serve as a passive logging point.


Worth researching: Modbus master/server logging tools for OT forensics.



4. Drills & Exercises
We should be running drills just like fire safety.


Tabletop exercises, communication rehearsals, mock ransomware scenarios, and failover practice.


SOPs and drills should be standardized and follow the same writing rules as incident plans.



5. Red Canary – RACI Matrix
Look up RACI matrices from Red Canary for inspiration.


Useful for defining who is Responsible, Accountable, Consulted, and Informed during IR, maintenance, or security audits.


Helps remove confusion during real-world incidents.



6. Talon’s 7 Common Documentation Mistakes
These apply to IR plans, SOPs, and every drill:
1. Failing to define a clear document hierarchy
No structure = confusion. Use sections and headings.
2. Being too general or vague
Explain how, who, and with what tools.
3. Not defining terms or acronyms
Glossary required — ICS, PLC, TLS, MFA, HMI, etc.
4. Mixing concepts without transitions
Keep flow logical. Don’t jump between topics randomly.
5. Using inconsistent formatting
Pick a format and stick to it — bullets, headings, fonts.
6. Overloading with unnecessary details
Be clear and concise. Not everything needs to be in the main doc.
7. Forgetting the purpose and audience
Write for operators, not lawyers.
 Write for technicians, not executives.

7. Self-Reflection
These rules should apply to all SOPs, drills, plans, and incident documentation.


Treat it the same way we treat fire safety: clear, structured, practiced, and easy to execute under stress.
It ask the question why would this be important , and i would say the same thing 
because it could cause harm or death no brainer 

