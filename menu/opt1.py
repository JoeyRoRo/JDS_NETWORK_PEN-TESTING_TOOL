#!/usr/bin/env python
from __future__ import print_function
import subprocess, sys, time

''' This section of the program will set your network adaptor into monitor
mode. 

If there are any questions please email me at joejoejoey13@gmail.com. 
'''

short_name = 'Airmon'
disp_name = 'Prepare to monitor network'
otype = 'Routine'
answers = []

# Main definition
def run():
    global answers
    subprocess.call('clear', shell=True)
    wait_timer('Gathering interface info...')
# This section checks if there is a network device is already in monitor mode
    if_check = subprocess.check_output('sudo ifconfig -s', shell=True)
    if 'mon' in if_check:
        raw_input('You already have a interface in monitor mode. Press enter to return to the main menu.\n')
        return
# This section prompts the user for 
    while True:
        subprocess.call('clear', shell=True)
        i = 0
        while True:
            print(if_check)
            ans = raw_input('Which interface would you like to use: ')

            if validate(ans, if_check):
                answers.append(ans)
                break
        wait_timer('Configuring interface for monitoring...')
# This section tries the command of putting the selected network device into monitor mode       
        try: 
            subprocess.call('sudo airmon-ng start %s' % answers[0], shell=True)
            raw_input('\nYou now have a interface in monitor mode. Press enter to return to the previous menu.')
        except: raw_input('Device did not go into monitor mode. Please check your network device to ensure it is capable of going into monitor mode.')
        return

# Definition to validate the user input
def validate(ans, if_check):
    eth = ['eth' + ifnum.__str__() for ifnum in range(0, 9)]
    wlan = ['wlan' + ifnum.__str__() for ifnum in range(0, 9)]
    if (ans in if_check) and ((ans in eth) or (ans in wlan)):
        return True
    subprocess.call("clear")
    print('\nNot a valid interface\n')
    return False

# Definition to print a wait timer
def wait_timer(on_what):
    sys.stdout.write(on_what)
    timer = 4
    while timer > 0:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.25)
        timer = timer - 1
