#!/usr/bin/env python
from __future__ import print_function
import subprocess, sys, time, re, thread, os
from multiprocessing import Process

'''
This section of the program will put a network device into monitor mode, and collect network traffic. 
The user provides parameters for collecting traffic, and then the program runs the airodump-ng program.

If there are any questions please email me at joejoejoey13@gmail.com. 
'''

short_name = 'Airodump'
disp_name = 'Start sniffing network'
otype = 'Routine'
options1 = ['Set channel to capture on: ', 'Set AP to capture on: ', 'Set locate to save to: ', 'Set GPS save options: ']
options2 = ['What channel would you like to capture on: ', 'What AP would you like to capture on: ', 'Where would you like to save your capture to: ', 'GPS...\n1.) on \n2.) off']
answers = ['', '', '', 'Off']
if_check = subprocess.check_output('ifconfig -s', shell=True).splitlines()[1:]

def run():
    global answers
    wait_timer('Gathering interface info...')
    if not 'mon' in if_check:
        # imports the airmon options
        import airmon.py
        # runs the airmon options to put a interface in monitor mode
        airmon.run()
    answers = ['', '', '', 'Off']
    subprocess.call('clear')
    while True:
        print("GPS is set to: "+answers[3]+"\n")
        if not answers[0] == "": 
            print("Set to capture on channel "+answers[0]+"\n")
        if not answers[1] == "": 
            print("Set to capture on AP "+answers[1]+"\n")
        if not answers[2] == "":
            print("Set to save capture to "+answers[2]+"\n")
        capture_menu = raw_input('Would you like to...\n' \
                                    '1.) '+options1[0]+'\n' \
                                    '2.) '+options1[1]+'\n' \
                                    '3.) '+options1[2]+'\n' \
                                    '4.) '+options1[3]+'\n' \
                                    '5.) Run Airodump\n' \
                                    '6.) Clear settings\n' \
                                    '7.) Back \n')
        if (capture_menu.isdigit()) and (0 < (int(capture_menu)) < 8):
            if 0 < (int(capture_menu)) < 5:
                next(capture_menu)
            if int(capture_menu) == 5:
                thread.start_new_thread(airodump_thread, ("Airodump thread",))
                raw_input("Airodump starting...\n")
                break
            if int(capture_menu) == 6:
                answers = ['', '', '', 'Off',]
            if int(capture_menu) == 7:
                return
        else: print('Not a valid option')
        subprocess.call('clear')

def aircheck_thread(thread_name):
    subprocess.check_output('xterm -e airodump-ng mon0', shell=True)

def next(i):
    if int(i) == 1:
        thread.start_new_thread( aircheck_thread, ("Scanning", ))
        print()
        ans = raw_input(options2[0])
        if validate(ans, 0): return True
        else: print("Not a valid option")
    if int(i) == 2:
        thread.start_new_thread( aircheck_thread, ("Scanning", ))
        print()
        ans = raw_input(options2[1])
        if validate(ans, 1): return True
        else: print("Not a valid option")
    if int(i) == 3:
        ans = raw_input(options2[2])
        if validate(ans, 2): return True
        else: print("Not a valid option")
    if int(i) == 4:
        ans = raw_input(options2[3])
        if validate(ans, 3): return True
        else: print("Not a valid option")

def validate(ans, i):
    #global answers
    if int(i) == 0:
        if 0 < int(ans) < 13: answers[0] = ans; return True
    if int(i) == 1:
        if re.match("([a-fA-F0-9]{2}[:|\-]?){6}", ans): 
            answers[1] = ans; return True
    if int(i) == 2:
        if not ans.endswith("\/"):
            ans = ans+"/"
        if os.path.isdir(ans):
            write_name = raw_input("What would you like to call your output " \
                    "file?: ")
            ans = ans+write_name
            answers[2] = ans
            return True
    if int(i) == 3:
        if ans == "1":
            answers[3] = "On"
            return True
        if ans == "2":
            answers[3] = "Off"
            return True
        subprocess.call('clear')
        print("Not a valid option.\n")
    return False

def airodump_thread(thread_name):
    global answers
    if not answers[0] == '': answers[0] = ' --channel '+answers[0]
    if not answers[1] == '': answers[1] = ' --bssid '+answers[1]
    if not answers[2] == '': answers[2] = ' -w '+answers[2]
    if answers[3] == 'On': answers[3] = ' --gpsd '
    if answers[3] == 'Off': answers[3] = ''
    print(thread_name+" running. Press enter to return to the main menu.\n")
    subprocess.call("xterm -e airodump-ng%s%s%s%s mon0" % \
            (answers[0], answers[1], answers[2], answers[3]), 
            shell=True)

def wait_timer(on_what):
    sys.stdout.write(on_what)
    s='.'
    timer = 4
    while True:
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.5)
        timer = timer - 1
        if timer == 0: break

