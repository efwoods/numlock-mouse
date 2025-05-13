# [numlock-mouse](https://chatgpt.com/share/681e05a6-bb84-8011-ba20-9dbc7aa64f10)

[Mouse Movement Reference](https://pynput.readthedocs.io/en/latest/mouse.html#monitoring-the-mouse)
[Keyboard Movement Reference](https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard)

This software enables mouseclicks from the numpad on a keyboard when the numlock is not enabled

✅ Complete Proof-of-Concept (PoC)
Step 1: Install Dependencies

sudo apt update
sudo apt install xbindkeys xdotool

Step 2: Create Configuration File for xbindkeys

If it doesn't exist yet:

xbindkeys --defaults > ~/.xbindkeysrc

Step 3: Edit ~/.xbindkeysrc to Bind / to Left Click

Add this block to the end of your ~/.xbindkeysrc file:

# Send left click on '/' key (only when Num Lock is off)

"bash -c 'if [[$(xset q | grep "Num Lock" | awk \"{print \\$8}\") == \"off\"]]; then xdotool click 1; fi'"
KP_Divide

Explanation:

    KP_Divide is the key symbol for the numeric keypad /.

    xset q | grep "Num Lock" checks the Num Lock state.

    xdotool click 1 simulates a left click.

    The command only executes if Num Lock is off.

Step 4: Start xbindkeys

xbindkeys

To run it automatically at startup, you can add xbindkeys to your .xinitrc or desktop environment’s autostart applications.
Step 5: Optional: Make a Systemd Service (Headless Startup)

Create this file:

nano ~/.config/systemd/user/xbindkeys.service

Paste this content:

[Unit]
Description=Start xbindkeys

[Service]
ExecStart=/usr/bin/xbindkeys
Restart=on-failure

[Install]
WantedBy=default.target

Then enable it:

systemctl --user enable --now xbindkeys

Would you like to map this to a different key or make the mouse move too?
