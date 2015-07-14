#!/usr/bin/env python
from __future__ import print_function
import subprocess, os, re, sys, time
from scapy.all import *

''' This section of the program will help crack WEP encrypted Wi-Fi network
passwords. In this section the user is prompted for their .cap file where they
have captured some of the Wi-Fi packtes. Then the program uses the aircrack-ng
command to attempt to crack the password for the network.

If there are any questions please email me at joejoejoey13@gmail.com. 
'''

short_name = 'WEP'
disp_name = 'Crack WEP'
otype = 'Routine'
need = ['Where is your .cap file located: ', '\nWhat is the BSSID of the' \
		' AP you are going after: ']
answers = []

# Main definition
def run():          
	global answers; answers=[]
	nets = []     
	subprocess.call('clear', shell=True)         
# This section prompts the user for the needed information	
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
		if i == 0:                                  
			if ans[0] == "\'": ans = ans[1:]
			if ans.endswith("\' "): ans = ans[:-2]             
			bssid_check = ''
# If the answers is valid, the answers is added to the answers array
		if validate(ans, i, nets):                 
			answers.append(ans)
			i += 1

	wait_timer('Cracking WEP..')
# This section attempts the aircrack command to crack the WEP password	
	subprocess.call("aircrack-ng -b "+answers[1]+" "+answers[0] \
					, shell=True)
	raw_input('Finished cracking WEP.\n Press [Enter] to return to the '\
															'main menu')
	return

# This definition validates users input
def validate(ans, i, nets):
	if i == 0:
		if os.path.isfile(ans) and ans.endswith(".cap"): return True
	if i == 1:
		if (re.match("([a-fA-F0-9]{2}[:|\-]?){6}", ans)):
			for x in nets: 
				if ans in x: return True
	return False

# This definition prints a wait timer
def wait_timer(on_what):
    sys.stdout.write(on_what)
    timer = 4
    while timer > 0:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.25)
        timer -= 1