import json
import os
import ctypes
from pynput import mouse, keyboard

# Fix DPI scaling on Windows — ensures pixel coordinates are accurate
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
POSITIONS_FILE = os.path.join(DATA_DIR, "positions.json")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_mouse_position():
    """Return the current mouse cursor position as (x, y) integers."""
    controller = mouse.Controller()
    return int(controller.position[0]), int(controller.position[1])


def wait_for_key_capture():
    """Block until F6 (capture) or Escape (cancel). Return position tuple or None."""
    result = {"value": None}

    def on_press(key):
        if key == keyboard.Key.f6:
            result["value"] = get_mouse_position()
            return False
        if key == keyboard.Key.esc:
            result["value"] = None
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return result["value"]


def capture_step(label, step_num, total):
    """Prompt user for one position capture. Return dict or None on cancel."""
    print()
    print(f"  >> Step {step_num} of {total}")
    print(f"     Target: {label}")
    print(f"     Hover over it, then press F6  |  Escape to cancel")
    print(f"     Waiting...", end="", flush=True)

    pos = wait_for_key_capture()
    if pos is None:
        return None

    print(f"  OK! ({pos[0]}, {pos[1]})")
    return {"x": pos[0], "y": pos[1]}


def calibrate():
    clear_screen()
    print("=" * 58)
    print("        CS2 REPORT TOOL  -  CALIBRATION")
    print("=" * 58)
    print()
    print("  Controls:")
    print("    F6      Capture current mouse position")
    print("    Escape  Cancel calibration")
    print()
    print("  The calibration adapts to ANY resolution.")
    print("  Make sure CS2 is running in Fullscreen Windowed.")

    positions = {
        "resolution": [1920, 1080],
        "ct_players": [],
        "t_players": [],
        "report_reasons": {},
        "submit_button": None,
    }

    total_steps = 14  # 5 CT + 5 T + 3 reasons + 1 submit
    step = 0

    # ── Phase 1 : CT player report buttons ──────────────────
    print()
    print("-" * 58)
    print("  PHASE 1/4 — CT Player Report Buttons (top section)")
    print("  Open scoreboard: Tab  +  Right-click for cursor")
    print("-" * 58)

    for i in range(1, 6):
        step += 1
        pos = capture_step(
            f"CT Player {i} — Report button",
            step, total_steps,
        )
        if pos is None:
            print("\n  Calibration cancelled.")
            return
        positions["ct_players"].append(pos)

    # ── Phase 2 : T player report buttons ───────────────────
    print()
    print("-" * 58)
    print("  PHASE 2/4 — T Player Report Buttons (bottom section)")
    print("-" * 58)

    for i in range(1, 6):
        step += 1
        pos = capture_step(
            f"T Player {i} — Report button",
            step, total_steps,
        )
        if pos is None:
            print("\n  Calibration cancelled.")
            return
        positions["t_players"].append(pos)

    # ── Phase 3 : Report reason checkboxes ──────────────────
    print()
    print("-" * 58)
    print("  PHASE 3/4 — Report Reasons")
    print("  Click any player's Report button first to open the")
    print("  report dialog, then calibrate each reason option.")
    print("-" * 58)

    reasons = [
        ("aimbot", "Aimbot / Aim Assistance"),
        ("wallhack", "Wallhack / Vision Assistance"),
        ("other", "Other Hacking"),
    ]

    for key, label in reasons:
        step += 1
        pos = capture_step(label, step, total_steps)
        if pos is None:
            print("\n  Calibration cancelled.")
            return
        positions["report_reasons"][key] = pos

    # ── Phase 4 : Submit button ─────────────────────────────
    print()
    print("-" * 58)
    print("  PHASE 4/4 — Submit Button")
    print("-" * 58)

    step += 1
    pos = capture_step("Submit / Send button", step, total_steps)
    if pos is None:
        print("\n  Calibration cancelled.")
        return
    positions["submit_button"] = pos

    # ── Save ────────────────────────────────────────────────
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(POSITIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(positions, f, indent=2)

    print()
    print("=" * 58)
    print("  Calibration complete!")
    print(f"  Saved to: data/positions.json")
    print("=" * 58)


if __name__ == "__main__":
    try:
        calibrate()
    except KeyboardInterrupt:
        print("\n  Interrupted.")
    input("\n  Press Enter to exit...")
