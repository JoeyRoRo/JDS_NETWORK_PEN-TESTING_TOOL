#!/usr/bin/env python2
from __future__ import print_function
import subprocess, sys, time

''' 
This section of the program will set your network adaptor into monitor
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
    # This section checks if there is a network device is already in monitor
    # mode
    if_check = subprocess.check_output(
            'ifconfig -s | awk -v col=1 \'{print $col}\'',
            shell=True).splitlines()[1:]
    if 'mon' in ('\n'.join(if_check)):
        raw_input('You already have a interface in monitor mode.\n' \
                   'Press [ENTER] to continue...\n')
        return
    # This section prompts the user for the interface they'd like to use
    while True:
        subprocess.call('clear', shell=True)
        i = 0
        print('{}\n## Select an interface ##\n{}\n'.format('#'*25, '#'*25))
        while True:
            print('\n'.join(if_check))
            print()
            ans = raw_input('Type the interface you would like to use: ')
            if validate(ans, if_check):
                answers.append(ans)
                break
        wait_timer('Configuring interface for monitoring...')
        # This section tries the command of putting the selected network device
        # into monitor mode       
        try: 
            subprocess.call('airmon-ng start %s' % answers[0], shell=True)
            raw_input('You now have a interface in monitor mode.\n' \
                      'Press [ENTER] to return to the previous menu...')
        except: 
            raw_input('Device did not go into monitor mode.\n' \
                      'Please check your network device to ensure it is ' \
                      'capable of going into monitor mode.')
        return

# Definition to validate the user input
def validate(ans, if_check):
    if (ans in if_check): 
        return True
    subprocess.call("clear")
    print('Not a valid interface, please double check that there are no ' \
           'typos\n')
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
    sys.stdout.write('\n')
