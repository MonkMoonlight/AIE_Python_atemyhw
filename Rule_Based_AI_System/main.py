#!/usr/bin/env python3
"""
Tech Support Troubleshooter — Rule-Based AI (Pre-ML Expert System Style)

This script implements the rule set from the README using plain IF–ELIF–ELSE logic.
It demonstrates:
- User input via input()
- Rule-based decision making via conditionals
- Text outputs (recommendations) based on rules
- Clear comments showing how rules map to code branches
- A simple test mode (--test) to exercise multiple branches without interactive input

Run (interactive):
    python main.py

Run (scripted tests):
    python main.py --test
"""

import sys
from typing import List, Callable, Optional

# ------------------------
# Helpers
# ------------------------

def normalize(text: str) -> str:
    """Lowercase/trim user input for matching."""
    return (text or "").strip().lower()

def contains_any(haystack: str, needles: List[str]) -> bool:
    """Check if any keyword from needles exists in haystack."""
    h = normalize(haystack)
    return any(n in h for n in needles)

def ask(prompt: str, input_fn: Callable[[str], str] = input) -> str:
    """Ask a free-form question."""
    return input_fn(prompt + " ").strip()

def ask_yes_no(prompt: str, input_fn: Callable[[str], str] = input) -> bool:
    """
    Ask a yes/no question. Returns True for yes-like answers.
    Accepts: y/yes/sure/true/1  (False otherwise)
    """
    ans = input_fn(prompt + " (y/n) ").strip().lower()
    return ans in {"y", "yes", "sure", "true", "1"}

def advise(message: str):
    """Print a recommendation/action step."""
    print(f"- ACTION: {message}")

def escalate(reason: Optional[str] = None):
    """Fallback escalation."""
    if reason:
        print(f"- ESCALATE: {reason}")
    else:
        print("- ESCALATE: Unable to resolve; provide device model/OS, recent changes, error text, and escalate to human support.")

# ------------------------
# Routing by Keywords (Intent Detection) — mirrors README
# ------------------------

KEYWORDS = {
    "POWER": ["power", "won’t turn on", "wont turn on", "no lights", "dead"],
    "BOOT": ["boot", "startup", "won’t boot", "wont boot", "bios", "black screen on boot"],
    "INTERNET": ["internet", "wifi", "wi-fi", "network", "online", "connection"],
    "DISPLAY": ["display", "screen", "monitor", "resolution", "flicker", "hdmi"],
    "PERFORMANCE": ["slow", "lag", "performance", "freeze", "stutter", "high cpu"],
    "AUDIO": ["sound", "audio", "speakers", "mic", "microphone", "mute", "volume"],
    "SOFTWARE": ["install", "update", "error code", "crash", "application", "app"],
}

def route_by_keywords(user_text: str) -> str:
    """
    Return the first category whose keywords appear in user_text.
    If no match, return 'UNKNOWN'.
    """
    for category, words in KEYWORDS.items():
        if contains_any(user_text, words):
            return category
    return "UNKNOWN"

# ------------------------
# Category Handlers — each encodes IF–THEN rules from README
# ------------------------

def handle_power(input_fn: Callable[[str], str] = input):
    # POWER rules
    # IF no lights/fans -> check outlet/cable/power strip
    has_lights = ask_yes_no("Do you see ANY lights or hear fans when you press power?", input_fn)
    if not has_lights:
        advise("Check outlet and power cable; try a different outlet or power strip.")
        psu_light = ask_yes_no("Do you see any indicator light on the charger/PSU?", input_fn)
        if not psu_light:
            advise("Try a different cable/charger/PSU; potential power supply failure.")
            return
        long_press_effect = ask_yes_no("Does a 10+ second power-button press do anything?", input_fn)
        if long_press_effect:
            advise("Perform a force shutdown, then power on again.")
            return
        escalate("Possible hardware failure in power circuitry.")
        return
    # If we DO have lights/fans, check for beep codes or other indicators
    beeps = ask_yes_no("Do you hear any beep codes or see an error on screen?", input_fn)
    if beeps:
        advise("Consult the motherboard/computer manual for beep codes; likely RAM/GPU/other hardware.")
    else:
        advise("Try disconnecting peripherals and power-cycling. If issue persists, escalate.")

def handle_boot(input_fn: Callable[[str], str] = input):
    # BOOT rules
    powers_on = ask_yes_no("Does the device power on (lights/fans) but the OS doesn't load?", input_fn)
    if powers_on:
        beeps_or_text = ask_yes_no("Do you see error text or hear beep codes?", input_fn)
        if beeps_or_text:
            advise("Look up the specific error/beep code for your model; likely hardware (e.g., RAM/GPU).")
        safe_mode = ask_yes_no("Can you access Safe Mode?", input_fn)
        if safe_mode:
            advise("Run startup repair or uninstall recent drivers/updates.")
            return
        bootable_usb = ask_yes_no("Do you have a bootable USB installer/recovery drive?", input_fn)
        if bootable_usb:
            advise("Boot from USB, run repair utilities, and check disk health.")
            return
        escalate("Create boot media; if OS still won't load after repairs, escalate.")
        return
    else:
        advise("If it does not power on at all, re-check POWER category steps.")
        escalate("No power to boot; likely POWER category root cause.")

def handle_internet(input_fn: Callable[[str], str] = input):
    # INTERNET rules
    others_online = ask_yes_no("Are other devices on your network able to go online?", input_fn)
    if others_online:
        advise("This device-specific: renew IP, forget & rejoin Wi‑Fi, or reset the network adapter.")
    else:
        advise("Router/modem issue likely: power-cycle modem/router for 30–60 seconds.")
    wifi_connected = ask_yes_no("Does this device show Wi‑Fi as 'connected'?", input_fn)
    if not wifi_connected:
        advise("Reconnect to the correct SSID and verify password.")
        return
    has_web = ask_yes_no("Even when connected, can you browse the web?", input_fn)
    if not has_web:
        advise("Ping the gateway/DNS, flush DNS cache, and set a public DNS (e.g., 8.8.8.8).")
    ethernet = ask_yes_no("Are you using Ethernet on this device?", input_fn)
    if ethernet:
        advise("Check/replace Ethernet cable; try a different router/switch port.")

def handle_display(input_fn: Callable[[str], str] = input):
    # DISPLAY rules
    external = ask_yes_no("Are you using an external monitor?", input_fn)
    if external:
        input_correct = ask_yes_no("Is the monitor input (HDMI/DP) set correctly and cable seated?", input_fn)
        if not input_correct:
            advise("Set correct input source and reseat/replace the cable.")
            return
        brand_splash = ask_yes_no("On power-up, do you see the monitor's brand splash/logo?", input_fn)
        if not brand_splash:
            advise("Monitor power issue or bad cable; test with another cable/port/device.")
            return
    laptop = ask_yes_no("Is this a laptop?", input_fn)
    if laptop:
        advise("Toggle display mode (Win+P / macOS Displays) and update GPU drivers.")
    flicker = ask_yes_no("Do you see flicker or wrong/low resolution?", input_fn)
    if flicker:
        advise("Set native resolution/refresh rate; update GPU driver; try another cable/port.")

def handle_performance(input_fn: Callable[[str], str] = input):
    # PERFORMANCE rules
    app_tops = ask_yes_no("Does one specific app top CPU/RAM in Task Manager/Activity Monitor?", input_fn)
    if app_tops:
        advise("Close/update/reinstall that app; check for known issues or patches.")
    low_disk = ask_yes_no("Is disk space low on the system drive?", input_fn)
    if low_disk:
        advise("Free up space: remove temp files, uninstall unused apps, clear caches.")
    advise("Disable heavy startup apps, scan for malware, and apply OS/driver updates.")

def handle_audio(input_fn: Callable[[str], str] = input):
    # AUDIO rules
    correct_output = ask_yes_no("Is the correct audio output device selected?", input_fn)
    if not correct_output:
        advise("Switch to the intended speakers/headset in system audio settings.")
        return
    muted = ask_yes_no("Is the system/app muted or volume set very low?", input_fn)
    if muted:
        advise("Unmute and raise volume in both system and app settings.")
    advise("Reinstall/enable audio driver if needed; test with headphones; verify mic/app permissions.")

def handle_software(input_fn: Callable[[str], str] = input):
    # SOFTWARE rules
    install_fail = ask_yes_no("Are you troubleshooting an installation failure?", input_fn)
    if install_fail:
        perm = ask_yes_no("Is it a permission/security warning?", input_fn)
        if perm:
            advise("Run as admin; allow via OS security (Gatekeeper/SmartScreen); check antivirus.")
        dep = ask_yes_no("Does the error mention a missing dependency/framework?", input_fn)
        if dep:
            advise("Install the required redistributable/framework/library and retry.")
    crash = ask_yes_no("Is an app crashing on launch/use?", input_fn)
    if crash:
        advise("Clear app cache/config, update/reinstall, and check version compatibility with your OS.")
        advise("Review app/system logs for specific error messages.")

# ------------------------
# Session Control
# ------------------------

def handle_unknown(input_fn: Callable[[str], str] = input):
    desc = ask("Please briefly describe your issue (include device model/OS and recent changes):", input_fn)
    category = route_by_keywords(desc)
    if category == "UNKNOWN":
        escalate("No matching rule category for the description provided.")
        return
    dispatch(category, input_fn)

def dispatch(category: str, input_fn: Callable[[str], str] = input):
    """Call the handler for a given category."""
    print(f"\nCategory detected: {category}")
    if category == "POWER":
        handle_power(input_fn)
    elif category == "BOOT":
        handle_boot(input_fn)
    elif category == "INTERNET":
        handle_internet(input_fn)
    elif category == "DISPLAY":
        handle_display(input_fn)
    elif category == "PERFORMANCE":
        handle_performance(input_fn)
    elif category == "AUDIO":
        handle_audio(input_fn)
    elif category == "SOFTWARE":
        handle_software(input_fn)
    else:
        handle_unknown(input_fn)

def interactive_session():
    """Interactive loop using input()."""
    print("=== Tech Support Troubleshooter (Rule-Based) ===")
    while True:
        user_text = ask("Describe your issue in one sentence:", input)
        category = route_by_keywords(user_text)
        if category == "UNKNOWN":
            print("I couldn't detect a category from that description.")
            handle_unknown(input)
        else:
            dispatch(category, input)

        again = ask_yes_no("\nWould you like to troubleshoot another issue?", input)
        if not again:
            print("Goodbye!")
            break

# ------------------------
# Scripted Test Utilities
# ------------------------

class ScriptedInput:
    """
    Provide a deterministic input() replacement from a preset list of answers.
    Useful for automated tests to walk through branches without typing.
    """
    def __init__(self, answers: List[str]):
        self.answers = answers[:]
        self.idx = 0

    def __call__(self, prompt: str = "") -> str:
        if self.idx >= len(self.answers):
            # If tests run out of answers, default to 'n' to avoid hanging
            print(prompt + " [auto-default: n]")
            return "n"
        ans = self.answers[self.idx]
        print(f"{prompt} {ans}")
        self.idx += 1
        return ans

def run_scripted_demo():
    """
    Exercise multiple branches across categories.
    Each scenario provides answers that drive the decision tree.
    """
    print("\n--- TEST 1: POWER (no lights, no PSU light) ---")
    scripted = ScriptedInput([
        # route_by_keywords: we pass description mentioning 'no lights' -> POWER
        # Handler POWER:
        # Q1 has_lights?
        "n",              # no lights/fans
        # Q2 psu light?
        "n",              # no PSU light
    ])
    dispatch("POWER", scripted)

    print("\n--- TEST 2: INTERNET (others offline, wifi connected no web) ---")
    scripted = ScriptedInput([
        "n",  # Are other devices online? -> No (router issue)
        "y",  # Wi‑Fi shows connected? -> Yes
        "n",  # Can you browse the web? -> No
        "n",  # Using Ethernet? -> No
    ])
    dispatch("INTERNET", scripted)

    print("\n--- TEST 3: AUDIO (wrong device then fix) ---")
    scripted = ScriptedInput([
        "n",  # Correct output device selected? -> No
    ])
    dispatch("AUDIO", scripted)

    print("\n--- TEST 4: BOOT (safe mode works) ---")
    scripted = ScriptedInput([
        "y",  # Device powers on but OS doesn't load?
        "n",  # Beeps or error text?
        "y",  # Can access Safe Mode?
    ])
    dispatch("BOOT", scripted)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_scripted_demo()
    else:
        interactive_session()

if __name__ == "__main__":
    main()
