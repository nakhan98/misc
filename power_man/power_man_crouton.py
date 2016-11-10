#!/usr/bin/env python2
"""
### POWERMAN ###
- Chromeos/Crouton (Debian Jessie) version
- Inform user when battery is running low/critical levels while discharging.
- Lock screen after a specified period of inactivity
- Requires xprintidle, libnotify-bin and i3lock
"""

# import re
from subprocess import Popen, PIPE, call, check_call, CalledProcessError
from shlex import split as sh_split
from time import sleep

# Interval between checking (seconds)
INTERVAL = 60

# xlock inactivity
XLOCK_INACTIVITY = 300

# Suspend system after this duration of inactivity while
# system is discharging (seconds)
# (NO SUSPEND IN THIS VERSION)
INACTIVITY = 600

# System will not be suspended if these apps are running
# (NO SUSPEND IN THIS VERSION)
IMPORTANT_APPS = ("apt-get", "aptitude", "dpkg", "dselect")

# X Lock app
X_LOCK_APP = "i3lock"

# Battery threshold levels (%)
LOW_THRESHOLD = 20
CRIT_THRESHOLD = 10

# Notification sound (filepath)
# DOES NOT EXIST ON CROUTON VERSION OF DEBIAN
WAV_FILE = "/usr/share/sounds/speech-dispatcher/test.wav"

# Battery capacity info file
BAT_CAP_FILE = "/sys/class/power_supply/BAT0/capacity"

# Batter discharging info file
BAT_DISCHARGE_FILE = "/sys/class/power_supply/BAT0/status"
DISCHARGING = "Discharging"

# Warning messages
LOW_WARNING_MSG = "Battery is at %d%%!"
CRIT_BAT_MSG = "BATTERY POWER IS CRITICALLY LOW!!!"


def important_apps_running(apps=IMPORTANT_APPS):
    '''Don't want PC to be suspended if important apps are running eg. system
    updates'''
    for app in apps:
        try:
            check_call(["pidof", app])
        except CalledProcessError:
            pass
        else:
            return True

    return False


def user_inactive_time():
    p = Popen("xprintidle", stdout=PIPE)
    idle_time = p.communicate()[0]
    idle_time = float(idle_time)/1000
    return idle_time


def is_discharging():
    with open(BAT_DISCHARGE_FILE) as bdf:
        charging_status = bdf.read().strip()
        if charging_status == DISCHARGING:
            return True
        else:
            return False


def get_bat_val():
    with open(BAT_CAP_FILE) as bcf:
        bat_left = int(bcf.read().strip())
    return bat_left


def send_xmessage_bat(bat_value):
    warning_message = "Warning: Battery is at %d%%" % bat_value
    cmd = 'xmessage -button ok -center "%s" -timeout 10' % warning_message
    cmd = sh_split(cmd)
    call(cmd)


def send_xmessage_shutdown():
    cmd = ('xmessage -button ok -center "Shutting down in 1 minute...'
           ' (Click OK or close window to shutdown now)" -timeout 60')
    cmd = sh_split(cmd)
    call(cmd)


def notify_bat(bat_value):
    '''Replaces previous Xmessage battery notifications'''
    warning_message = LOW_WARNING_MSG % bat_value
    cmd = 'notify-send -u normal "%s"' % warning_message
    call(sh_split(cmd))


def notify_shutdown():
    '''Replaces previous Xmessage shutdown notifications'''
    cmd = 'notify-send -u critical "%s"' % CRIT_BAT_MSG
    call(sh_split(cmd))


def play_audio_clip():
    cmd = sh_split("aplay -q %s" % WAV_FILE)
    call(cmd)


def shutdown_system():
    print("Please turn off or charge immediately!")


def suspend_system():
    print("Crouton version... Chromeos handles suspension")


def lock_screen():
    """
    Try to lock screen using designated screen lock app if not already running
    """
    xlock_app_running = important_apps_running([X_LOCK_APP])
    if not xlock_app_running:
        call(X_LOCK_APP)
    else:
        print("%s is already running" % X_LOCK_APP)


def main():
    while True:
        if user_inactive_time() > XLOCK_INACTIVITY:
            lock_screen()

        if is_discharging():
            curr_bat = get_bat_val()

            if curr_bat < CRIT_THRESHOLD:
                notify_shutdown()
                sleep(60)
                shutdown_system()
            elif curr_bat < LOW_THRESHOLD:
                # play_audio_clip()
                notify_bat(curr_bat)

            if (user_inactive_time() > INACTIVITY and not
                    important_apps_running()):
                suspend_system()

        print("Sleeping...")
        sleep(INTERVAL)


if __name__ == "__main__":
    main()
