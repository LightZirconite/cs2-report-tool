import json
import os
import time
import ctypes
import pyautogui

# Fix DPI scaling on Windows — ensures clicks land at the correct position
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
POSITIONS_FILE = os.path.join(DATA_DIR, "positions.json")

# PyAutoGUI safety: move mouse to top-left corner to abort at any time
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# Default delay between each click action (seconds)
DEFAULT_ACTION_DELAY = 1.0


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_positions():
    """Load calibrated positions from JSON. Return dict or None on failure."""
    if not os.path.exists(POSITIONS_FILE):
        return None
    with open(POSITIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def click_at(pos, action_delay):
    """Move mouse to position and click with a configurable delay."""
    pyautogui.click(pos["x"], pos["y"])
    time.sleep(action_delay)


def report_single_player(positions, side, player_num, reason, action_delay):
    """Execute the full report sequence for one player (assumes scoreboard is open)."""
    player_list = positions["ct_players"] if side == "ct" else positions["t_players"]
    player_pos = player_list[player_num - 1]
    reason_pos = positions["report_reasons"][reason]
    submit_pos = positions["submit_button"]

    # 1. Click the player's Report button
    click_at(player_pos, action_delay)

    # 2. Click the report reason checkbox
    click_at(reason_pos, action_delay)

    # 3. Click Submit
    click_at(submit_pos, action_delay)


def execute_report(positions, side, players, reason, delay, repeat, action_delay):
    """Countdown, open scoreboard, report all selected players, close scoreboard."""
    # Countdown
    print()
    print("  >>> Switch to CS2 now! <<<")
    for i in range(delay, 0, -1):
        print(f"  Starting in {i}...   ", end="\r")
        time.sleep(1)
    print("  Executing...             ")

    side_label = "CT" if side == "ct" else "T"

    for run in range(1, repeat + 1):
        if repeat > 1:
            print(f"  --- Round {run}/{repeat} ---")

        # Open scoreboard
        pyautogui.keyDown("tab")
        time.sleep(action_delay)

        # Right-click to activate cursor on scoreboard
        pyautogui.rightClick()
        time.sleep(action_delay)

        # Report each selected player
        for player_num in players:
            print(f"  -> Reporting {side_label} Player {player_num}...")
            report_single_player(positions, side, player_num, reason, action_delay)
            time.sleep(action_delay)

        # Release Tab to close scoreboard
        pyautogui.keyUp("tab")

        # Small pause between rounds
        if run < repeat:
            time.sleep(action_delay)

    # Audible beep to signal completion
    print("\a", end="")
    print()
    print("  Done!")


def prompt_side():
    """Prompt user for team side. Return 'ct'/'t' or None on invalid input."""
    print("  Team:")
    print("    1. Counter-Terrorist (CT)  [top]")
    print("    2. Terrorist (T)           [bottom]")
    choice = input("\n  Choice [1/2]: ").strip()
    if choice == "1":
        return "ct"
    if choice == "2":
        return "t"
    return None


def prompt_players():
    """Prompt user for player numbers. Return list of ints or None on error."""
    print("  Player number(s), top to bottom (1-5)")
    print("  Multiple players: separate with commas  e.g. 1,3,5")
    raw = input("  Player(s): ").strip()
    try:
        players = [int(p.strip()) for p in raw.split(",")]
        if not players or any(p < 1 or p > 5 for p in players):
            raise ValueError
        return players
    except ValueError:
        return None


def prompt_reason():
    """Prompt user for report reason. Return key string or None on error."""
    print("  Report reason:")
    print("    1. Aimbot")
    print("    2. Wallhack")
    print("    3. Other Hacking")
    choice = input("\n  Choice [1/2/3]: ").strip()
    reason_map = {"1": "aimbot", "2": "wallhack", "3": "other"}
    return reason_map.get(choice)


def prompt_delay():
    """Prompt user for countdown delay. Return int or None on error."""
    raw = input("  Delay before starting (seconds) [5]: ").strip()
    try:
        delay = int(raw) if raw else 5
        if delay < 0:
            raise ValueError
        return delay
    except ValueError:
        return None


def prompt_repeat():
    """Prompt user for number of report repetitions. Return int or None on error."""
    raw = input("  How many times to report? [1]: ").strip()
    try:
        repeat = int(raw) if raw else 1
        if repeat < 1:
            raise ValueError
        return repeat
    except ValueError:
        return None


def prompt_action_delay():
    """Prompt user for delay between each click action (ms). Return float seconds or None."""
    raw = input("  Delay between actions (ms) [1000]: ").strip()
    try:
        ms = int(raw) if raw else 1000
        if ms < 100:
            raise ValueError
        return ms / 1000.0
    except ValueError:
        return None


def main_menu(positions):
    """Main interactive loop."""
    while True:
        print("-" * 58)
        print("  REPORT CONFIGURATION")
        print("-" * 58)
        print()

        # Side
        side = prompt_side()
        if side is None:
            print("  Invalid choice.\n")
            continue
        print()

        # Players
        players = prompt_players()
        if players is None:
            print("  Invalid player number(s).\n")
            continue
        print()

        # Reason
        reason = prompt_reason()
        if reason is None:
            print("  Invalid choice.\n")
            continue
        print()

        # Delay
        delay = prompt_delay()
        if delay is None:
            print("  Invalid delay.\n")
            continue
        print()

        # Repeat count
        repeat = prompt_repeat()
        if repeat is None:
            print("  Invalid number.\n")
            continue
        print()

        # Action delay
        action_delay = prompt_action_delay()
        if action_delay is None:
            print("  Invalid delay (min 100ms).\n")
            continue

        # Summary
        side_name = "CT" if side == "ct" else "T"
        reason_name = {"aimbot": "Aimbot", "wallhack": "Wallhack", "other": "Other Hacking"}[reason]
        players_str = ", ".join(str(p) for p in players)

        print()
        print("-" * 58)
        print(f"  Team      : {side_name}")
        print(f"  Player(s) : {players_str}")
        print(f"  Reason    : {reason_name}")
        print(f"  Delay     : {delay}s")
        print(f"  Repeat    : {repeat}x")
        print(f"  Action gap: {int(action_delay * 1000)}ms")
        print("-" * 58)
        print()

        confirm = input("  Start? [Y/n]: ").strip().lower()
        if confirm not in ("", "y", "yes", "o", "oui"):
            print("  Cancelled.\n")
            continue

        # Execute
        try:
            execute_report(positions, side, players, reason, delay, repeat, action_delay)
        except pyautogui.FailSafeException:
            print("\n  ABORTED — Mouse moved to corner (failsafe).")
            # Make sure Tab key is released
            try:
                pyautogui.keyUp("tab")
            except Exception:
                pass

        print()
        again = input("  Report again? [Y/n]: ").strip().lower()
        if again in ("n", "no", "non"):
            break

        clear_screen()
        print("=" * 58)
        print("            CS2 REPORT TOOL")
        print("=" * 58)
        print()


def main():
    clear_screen()
    print("=" * 58)
    print("            CS2 REPORT TOOL")
    print("=" * 58)
    print()

    positions = load_positions()
    if positions is None:
        print("  ERROR: No calibration data found!")
        print("  Run calibrate.bat first to set up positions.")
        input("\n  Press Enter to exit...")
        return

    res = positions.get("resolution", [0, 0])
    print(f"  Calibration loaded ({res[0]}x{res[1]})")
    print(f"  Failsafe: move mouse to top-left corner to abort")
    print()

    main_menu(positions)

    print("\n  Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Interrupted.")
        # Ensure Tab is released if interrupted during execution
        try:
            pyautogui.keyUp("tab")
        except Exception:
            pass
