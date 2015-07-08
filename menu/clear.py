#!/usr/bin/env python
from __future__ import print_function
import subprocess, sys, time

'''
This section of the program will clear any network adapters settings. It
will bring any adapter out of monitor mode, and reset the MAC addresses that
were changed back to factory settings.  

If there are any questions please email me at joejoejoey13@gmail.com. 
'''

short_name = 'Clear settings'
disp_name = 'Reset interfaces to default'
otype = 'Routine'

# Main definition
def run():
    wait_timer('Clearing settings...')
    if_check = subprocess.check_output('ifconfig -s', shell=True) \
                         .splitlines()[1:]
    for x in [i for i in if_check if i.startswith('mon')]:
        subprocess.call('sudo airmon-ng stop %s' % x, shell=True)
    # Not all distros start wlan interfaces with wlan + number
    for x in [i for i in if_check if i.startswith('wl')]:
        subprocess.call('sudo macchanger -p %s' % x, shell=True)
    raw_input('Finished clearing settings to default.\n' \
              'Press [ENTER] to return to main menu...')

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
