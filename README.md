# CS2 Report Tool

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A lightweight tool to automate player reporting in Counter-Strike 2. It uses simple mouse clicks and keyboard inputs — **no overlay, no injection, no memory reading**. Just standard input automation.

Built with Python because it's the simplest cross-setup solution for this kind of project.

## Features

- **Universal calibration system** — works with ANY screen resolution. Calibrate once, report forever.
- **Multi-player reporting** — report one or multiple players in a single run.
- **3 report reasons** — Aimbot, Wallhack, Other Hacking (position-based, works in any language).
- **Failsafe** — move your mouse to the top-left corner of your screen to instantly abort.
- **Auto-install** — `.bat` launchers handle Python dependency installation automatically.

## Requirements

- **Windows** (tested on Windows 10/11)
- **Python 3.8+** — [Download here](https://www.python.org/downloads/) (make sure to check "Add Python to PATH" during install)
- **CS2** running in **Fullscreen Windowed** mode

## Quick Start

### 1. Calibration (one-time setup)

> You only need to redo this if you change your screen resolution.

1. Double-click **`calibrate.bat`**
2. Open CS2 and join a match
3. The script will guide you through **4 phases** (14 total captures):

| Phase | What to capture                                        | Count |
| ----- | ------------------------------------------------------ | ----- |
| 1     | CT player Report buttons (top section of scoreboard)   | 5     |
| 2     | T player Report buttons (bottom section of scoreboard) | 5     |
| 3     | Report reason checkboxes (Aimbot, Wallhack, Other)     | 3     |
| 4     | Submit button                                          | 1     |

**How it works:**

- Open the scoreboard in CS2: press **Tab**, then **right-click** to get a cursor
- Hover your mouse over the target button
- Press **F6** to capture the position
- Repeat for each step

Positions are saved to `data/positions.json` — this project does NOT ship calibrated position files by default. You must run the calibration step for your own machine and resolution. Run `calibrate.bat` to generate `data/positions.json` for your setup.

### 2. Reporting

1. Double-click **`launch.bat`**
2. Follow the prompts:
   - **Team**: CT (top) or T (bottom)
   - **Player(s)**: 1–5 from top to bottom (comma-separated for multiple, e.g. `1,3,5`)
   - **Reason**: Aimbot / Wallhack / Other Hacking
   - **Delay**: seconds before the script starts (default: 5s)
   - **Repeat**: how many times to loop the report sequence (default: 1)
   - **Action gap**: delay in milliseconds between each click (default: 500ms, minimum 120ms — increase to debug, decrease once calibrated)
3. Confirm, then **switch to CS2** during the countdown
4. The script automatically performs: **Tab → Right-click → Click Report → Click Reason → Click Submit**
5. During the countdown you can press `Escape` to cancel the run (requires the script's dependencies to be installed).
6. You'll hear a gentle beep sequence when it's done

## Default Positions (1920x1080 Fullscreen Windowed)

The included `data/positions.json` contains pre-calibrated positions for 1920x1080 as an example. You should recalibrate for your own setup by running `calibrate.bat` if your resolution or UI scale differs — the tool adapts to any resolution.

## Project Structure

```
cs2-report-tool/
├── calibrate.bat       # Launches calibration (auto-installs deps)
├── calibrate.py        # Calibration script — captures mouse positions
├── launch.bat          # Launches the report tool (auto-installs deps)
├── report.py           # Main report automation script
├── requirements.txt    # Python dependencies (pyautogui, pynput)
├── LICENSE             # GNU GPL v3
├── .gitignore
└── data/
    └── positions.json  # Calibrated mouse positions (auto-generated, git-ignored)
```

## Safety & Fair Play

This tool does **not**:

- Inject code into CS2
- Read game memory
- Display any overlay
- Modify game files

It only simulates standard keyboard and mouse inputs, the same way a human would. It's a convenience tool for reporting, not a cheat.

## Contributing

This project is open source. Feel free to:

- Submit a PR to add new features
- Report issues
- Calibrate and share position files for other resolutions

Original repository: [https://github.com/LightZirconite/cs2-report-tool](https://github.com/LightZirconite/cs2-report-tool)

## License

This project is licensed under the **GNU General Public License v3.0**.

You are free to use, modify, and redistribute this project — including for forks and derivative works — **under these conditions**:

- You must keep the same GPL v3 license on any derivative work.
- You must give **visible credit** to the original project: [https://github.com/LightZirconite/cs2-report-tool](https://github.com/LightZirconite/cs2-report-tool)
- You cannot sublicense or relicense it under proprietary terms.

See the [LICENSE](LICENSE) file for the full license text.

## Educational Use & Disclaimer

- **Educational purpose only:** This software is provided for learning and automation experimentation. It is not intended to enable cheating or to bypass any game's security measures.
- **Use at your own risk:** The authors make no guarantees that use of this tool will not result in account penalties, restrictions, or other adverse consequences. You are responsible for complying with the game's Terms of Service and community rules.
- **No liability:** The project authors and contributors disclaim any liability for damages or losses arising from use or misuse of this software. There are no warranties of any kind.
- **Responsible use recommended:** Do not use this tool in competitive, ranked, or online environments where automation could cause harm or violate rules. Prefer using it in safe, local, or educational contexts only.

If you are unsure whether using this tool is appropriate for your situation, do not use it and consult the game's support or terms.
