# Sample submission for the Building a Rule-Based AI System in Python project

## Part 1: Initial Project Ideas

1. **Project Idea 1: Restaurant Recommendation Chatbot**  
   **Description:** A chatbot that suggests restaurants based on user preferences (e.g., cuisine, budget, location).  
   **Rule-Based Approach:**  
   - Match keywords to rules (e.g., *IF cuisine = Italian AND budget = low → suggest Pizza Palace*).  
   - Use simple keyword extraction (cuisine/budget/location) to map to predefined options.

2. **Project Idea 2: Medical Symptom Checker (Diagnostic Tool)**  
   **Description:** A simple diagnostic system where a user enters symptoms and the AI suggests possible conditions.  
   **Rule-Based Approach:**  
   - Map symptom combinations to conditions (e.g., *IF fever AND cough AND sore throat → possible flu*).  
   - Rank or list multiple possible matches when rules overlap.

3. **Project Idea 3: Tech Support Troubleshooter**  
   **Description:** A helpdesk-style system that walks users through common computer/software issues.  
   **Rule-Based Approach:**  
   - Decision-tree logic (e.g., *IF no power lights → check outlet/cable; IF screen blank but fans running → check monitor input*).  
   - Ask targeted yes/no questions and advance through branches until a solution or escalation.

**Chosen Idea: Tech Support Troubleshooter**  
**Justification:** I chose the Tech Support Troubleshooter because it has a clear decision-tree structure that demonstrates the essence of rule-based AI. It’s practical and interactive, making it engaging to test with different scenarios while showcasing how rules can simulate intelligent guidance.

---

## Part 2: Rules/Logic for the Chosen System (Tech Support Troubleshooter)

**Keyword Routing (Intent Detection)**  
- **POWER:** “power”, “won’t turn on”, “no lights”, “dead”  
- **BOOT:** “boot”, “startup”, “won’t boot”, “BIOS”, “black screen on boot”  
- **INTERNET:** “internet”, “wifi/wi-fi”, “network”, “online”, “connection”  
- **DISPLAY:** “display”, “screen”, “monitor”, “resolution”, “flicker”, “HDMI”  
- **PERFORMANCE:** “slow”, “lag”, “freeze”, “stutter”, “high cpu”  
- **AUDIO:** “sound”, “audio”, “speakers”, “mic/microphone”, “mute”, “volume”  
- **SOFTWARE:** “install”, “update”, “error code”, “crash”, “application/app”  
- *(Else → UNKNOWN: ask a clarifying question.)*

**IF–THEN Rules (Condensed by Category)**

- **POWER**  
  - IF **no lights/fans** → THEN **check outlet/cable** or try another outlet/power strip.  
  - IF **outlet OK** AND **no charger/PSU light** → THEN **try different cable/charger; possible PSU issue**.  
  - IF **PSU light ON** AND **10+ sec power-button press does nothing** → THEN **escalate (possible hardware)**.

- **BOOT**  
  - IF **powers on but OS doesn’t load** → ask about **beep codes** and try **Safe Mode**.  
  - IF **Safe Mode works** → THEN **startup repair / uninstall recent drivers**.  
  - ELSE ask for **bootable USB**; IF available → **repair/check disk**; ELSE **create media & escalate**.

- **INTERNET**  
  - IF **other devices online** → THEN **device-specific fix** (renew IP, forget/rejoin Wi-Fi).  
  - IF **all devices offline** → THEN **power-cycle modem/router 30–60s**.  
  - IF **Wi-Fi connected but no web** → THEN **ping gateway/DNS, flush DNS, set public DNS (e.g., 8.8.8.8)**.  
  - IF **Ethernet** → THEN **check/replace cable; try another port**.

- **DISPLAY**  
  - IF **external monitor blank** → THEN **verify input source & cable; reseat/replace**.  
  - IF **no brand splash** → THEN **monitor power/cable issue**.  
  - IF **laptop** → THEN **toggle display mode (Win+P / macOS Displays); update GPU driver**.  
  - IF **flicker/low resolution** → THEN **set native resolution; update GPU; try new cable/port**.

- **PERFORMANCE**  
  - IF **one app tops CPU/RAM** → THEN **close/update/reinstall that app**.  
  - IF **low disk space** → THEN **free space / clear temp files**.  
  - THEN **disable heavy startup apps; malware scan; OS/driver updates**.

- **AUDIO**  
  - IF **wrong output device** → THEN **switch to correct device**.  
  - IF **muted/low volume** → THEN **unmute/raise volume (system + app)**.  
  - THEN **reinstall/enable audio driver; test headphones; check mic/app permissions**.

- **SOFTWARE**  
  - IF **install fails with permission error** → THEN **run as admin; allow via OS security; check antivirus**.  
  - IF **dependency missing** → THEN **install the required redistributable/framework/library**.  
  - IF **app crashes** → THEN **clear cache/config; update/reinstall; verify compatibility; review logs**.

- **Fallback / Escalation**  
  - IF no rule matches after 2–3 steps → THEN **request model/OS, recent changes, error messages, and escalate**.

---

## Part 3: Sample Input and Output

**Sample 1 — POWER (no lights, suspected PSU)**  
- **Input:** “My desktop won’t turn on. No lights at all.”  
- **Output:**  
  - ACTION: Check outlet and power cable; try a different outlet or power strip.  
  - ACTION: Do you see an indicator on the charger/PSU?  
  - ACTION: Try a different cable/charger/PSU; possible power supply failure.

**Sample 2 — INTERNET (Wi-Fi connected, no web)**  
- **Input:** “Wi-Fi shows connected but I can’t open any sites.”  
- **Output:**  
  - ACTION: Ping the gateway/DNS; flush DNS cache; set a public DNS (e.g., 8.8.8.8).  
  - ACTION: If other devices are also offline, power-cycle modem/router for 30–60 seconds.  
  - ACTION: If using Ethernet, check/replace the cable and try another port.

**Sample 3 — BOOT (Safe Mode works)**  
- **Input:** “PC turns on but Windows won’t load.”  
- **Output:**  
  - ACTION: Can you access Safe Mode?  
  - ACTION: Run startup repair and uninstall recent drivers/updates.  
  - ACTION: If that fails, boot from a USB installer/recovery drive and run repair utilities.

**Sample 4 — AUDIO (wrong output device)**  
- **Input:** “No sound from speakers.”  
- **Output:**  
  - ACTION: Switch the audio output to the correct speakers/headset.  
  - ACTION: Unmute and raise volume in system and app settings.  
  - ACTION: Reinstall/enable audio driver; test with headphones; verify app/mic permissions.

---

### (Optional) How to Run the Python Script
If included, the script uses `input()` for interaction and plain `if/elif/else` for decision-making.

```bash
python3 main.py        # interactive
python3 main.py --test # scripted demo across categories
```

---

Part 4: Reflection and Submission

How the rule-based system works.
My Tech Support Troubleshooter emulates a classic expert system using plain IF–THEN logic and a simple decision tree. First, it performs keyword routing: the user’s free-text description is scanned for category terms (e.g., “won’t turn on” → POWER, “wifi” → INTERNET). Each category has a handler that asks short yes/no questions and follows deterministic branches. For example, in POWER: IF no lights/fans → check outlet/cable; IF outlet OK but no PSU light → try another charger; IF long power-press has no effect → escalate. The program uses input() for interaction and if/elif/else for decisions, printing actionable steps at each node. There’s also a --test mode with scripted answers so I can exercise multiple branches repeatedly without typing. The code comments mirror the rule set in the README, keeping the design and implementation aligned.

Challenges while prompting the AI (design + code).
The biggest challenge was consistency: I needed the AI’s outputs for Part 1 (ideas/choice), Part 2 (rules), and Part 3 (code) to match exactly, so I kept reiterating constraints like “use the same categories and phrasing.” Another challenge was granularity: human troubleshooting is fuzzy, but rules must be crisp. I asked the AI to convert natural guidance into explicit IF–THEN statements and to separate routing (keywords) from branch logic, which prevented overlap and “rule shadowing.” Choosing keywords required balancing coverage vs. false matches (e.g., “boot” vs. “reboot”), so I requested condensed keyword sets and a fallback UNKNOWN category with a clarifying question.

On the coding side, I asked for commented, minimal Python (no external libraries, no ML), a clear function per category, and a test harness (--test) to quickly validate paths. I also prompted for defensive details—normalizing input, yes/no parsing, and a final escalation path—to avoid infinite loops or dead ends. Finally, I used the AI to cross-check that the code’s questions and actions exactly reflect the README rules. Iterating this way helped keep scope tight, outputs deterministic, and the assignment’s requirements front and center. I also had some major issues with getting things to sync up with git up but for the most part I have fixed the issues with my github and commits.