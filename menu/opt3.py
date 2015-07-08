#!/usr/bin/env python
from __future__ import print_function
import subprocess, sys, time

''' This section of the program will clear any network adapters settings. It
will bring any adapter out of monitor mode, and reset the MAC addresses that
were changed back to factory settings.  

If there are any questions please email me at joejoejoey13@gmail.com. 
'''

short_name = 'Clear settings'
disp_name = 'Reset interfaces to default'
otype = 'Routine'
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# Main definition
def run():
    wait_timer('Clearing settings...')
    if_check = subprocess.check_output('sudo ifconfig -s', shell=True)
    for x in numbers:
        if 'mon'+x in if_check: subprocess.call('sudo airmon-ng stop mon%s' % x, shell=True)
        if 'wlan'+x in if_check: subprocess.call('sudo macchanger -p wlan%s' % x, shell=True)
    raw_input('Finished clearing settings to default. Press enter to return to main menu.\n')

# This definition prints a wait timer
def wait_timer(on_what):
    sys.stdout.write(on_what)
    s='.'
    timer = 4
    while True:
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.25)
        timer = timer - 1
        if timer == 0: break
