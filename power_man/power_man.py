#!/usr/bin/env python2
"""
- Inform user when battery is running low while discharging.
- Will shutdown system if battery reaches a specified critical level.
- Also suspend system if no user input (via X) after a specified period.
- Requires xprintidle, libnotify-bin and a notification daemon (eg. notify-osd)
"""

import re
from subprocess import Popen, PIPE, call, check_call, CalledProcessError
from shlex import split as sh_split
from time import sleep

# Interval between checking (seconds)
INTERVAL = 60

# System will not be suspended if these apps are running
IMPORTANT_APPS = ("apt-get", "aptitude", "dpkg", "dselect")

# Suspend system after this duration of inactivity while
# system is discharging (seconds)
INACTIVITY = 600

# Battery threshold levels (%)
LOW_THRESHOLD = 15
CRIT_THRESHOLD = 8

# Notification sound (filepath)
WAV_FILE = "/usr/share/sounds/speech-dispatcher/test.wav"


def important_apps_running():
    '''Don't want PC to be suspended if important apps are running eg. system
    updates'''
    for app in IMPORTANT_APPS:
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
    p = Popen(["acpi", "-b"], stdout=PIPE)
    output = p.communicate()[0]
    if "Discharging" in output:
        return True
    else:
        return False


def get_bat_val():
    p = Popen(["acpi", "-b"], stdout=PIPE)
    output = p.communicate()
    bat_left = output[0]
    bat_left = re.search(r"(\d+)\%", bat_left).group(1)
    bat_left = int(bat_left)
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
    warning_message = "Warning: Battery is at %d%%!" % bat_value
    cmd = 'notify-send -u normal "%s"' % warning_message
    call(sh_split(cmd))


def notify_shutdown():
    '''Replaces previous Xmessage shutdown notifications'''
    warning_message = ("Battery power is critically low!\n"
                       "Shutting down system in 1 minute...")
    cmd = 'notify-send -u critical "%s"' % warning_message
    call(sh_split(cmd))


def play_audio_clip():
    cmd = sh_split("aplay -q %s" % WAV_FILE)
    call(cmd)


def shutdown_system():
    cmd = sh_split("systemctl poweroff")
    call(cmd)


def suspend_system():
    cmd = sh_split("systemctl suspend")
    call(cmd)


def main():
    while True:
        if is_discharging():
            curr_bat = get_bat_val()

            if curr_bat < CRIT_THRESHOLD:
                notify_shutdown()
                sleep(60)
                shutdown_system()
            elif curr_bat < LOW_THRESHOLD:
                play_audio_clip()
                notify_bat(curr_bat)

            if (user_inactive_time() > INACTIVITY and not
                    important_apps_running()):
                suspend_system()

        sleep(INTERVAL)


if __name__ == "__main__":
    main()
