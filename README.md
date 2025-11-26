##########################
## JDS PEN-TESTING TOOL ##
##########################

Program was written in and intented for use with python 2.7. The latest version is v1.3 and was last updated on 12 July 2015.

Below is a descripton of the each part of the program...
--------------------------------------------------------
1.) Crack password hashes

	a.) Create a rainbow table
	This section of the program will help a user create a rainbow table. The user is prompted for all the needed information and then the program uses the 'rtgen' program to make the rainbow table.

	b.) Sort a rainbow table
	This part of the program will sort a rainbow table. The user is promted for what rainbow table to sort and then uses 'rtsort' to sort the table.

	c.) Crack hash using an existing rainbow table
	This section of the program will use a rainbow table to crack a password hash.
	The program prompts the user for either a single hash or mutliple hashes, and
	then prompts the user for the hash(s) to crack. The program uses the 'rcrack'
	program to crack the hashes.
--------------------------------------------------------
2.) Start sniffing network
This section of the program will put a network device into monitor mode, and
collect network traffic.  The user provides parameters for collecting traffic,
and then the program runs the airodump-ng program.
--------------------------------------------------------
3.) Prepare to monitor network
This section of the program will set your network adaptor into monitor
mode. 
--------------------------------------------------------
4.) Crack Wi-Fi Passwords

	a.) Crack WPS
	This section of the program uses the kali tool 'Bully'. Bully is a tool to
	crack wireless router passwords through a WPS attack. Please refer to the Bully
	manual for more info on the Bully tool.
	
	b.) Crack WPA/WPA2 (w/dictionary)
	This part of the program will help crack WPA encrypted Wi-Fi network
	passwords. In this section the user is prompted for their .cap file where they
	have captured some of the Wi-Fi packtes. Then they are prompted for their
	dictionary file. Then the program uses the aircrack-ng command to attempt to
	crack the password for the network.
	
	c.) Salt a dictionary file with a WPA/WPA2 SSID
	This section of the program will help create a new dictionary file out of an
	already existing dictionary file. The new dictionary file will be salted with a
	user directed SSID. This is done in order to speed of the cracking of WPA
	encrypted Wi-Fi network passwords.
	
	d.) Crack WPA/WPA2 (w/salted dictionary)
	This section of the program helps crack WPA encrpyted Wi-Fi network passwords
	with the use of a salted dictionary file. The user is prompted for a .cap file
	with the WPA handshake in it, then is prompted for the salted dictionary file.
	The program uses cowpatty in order to run the salted dictionary file agains the
	WPA handshake.

	e.) Crack WEP
	This section of the program will help crack WEP encrypted Wi-Fi network
	passwords. In this section the user is prompted for their .cap file where they
	have captured some of the Wi-Fi packtes. Then the program uses the aircrack-ng
	command to attempt to crack the password for the network.
--------------------------------------------------------
5.) Reset interfaces to default
This section of the program will clear any network adapters settings. It
will bring any adapter out of monitor mode, and reset the MAC addresses that
were changed back to factory settings. 
--------------------------------------------------------
6.) Conduct Man-in-the-Middle attack
This section of the program conducts a mitm attack by arp spoofing. The
program prompts the user for the target device(s), interface to use, how to
mask the MAC, IP of the target and the gateway, and where you would like to
save the output.
--------------------------------------------------------

This program is intended for personal use, or use on your own network and devices. Please refer to all state, federal, and national laws before conducting any network pen-testing.

With this program it is possible to capture network traffic on Wi-Fi, or cabled networks. You must have a network interface that is capable of going into monitor mode (aka permisquous mode). 

To start the program, clone the repository, make the script executable and run it as root (or via `sudo`)

```
$ git clone https://github.com/bboybreeze/JDS_NETWORK_PEN-TESTING_TOOL
$ cd JDS_NETWORK_PEN-TEST_TOOL
$ chmod +x jdstool.py
$ sudo ./jdstool.py
```

The program uses a variety of other programs that are all built into Kali Linux. The program mainly uses the 'Aircrack suite'. But here are a list of dependencies/commands that must be capable of running on your Kali linux OS in order for all of the program to work...

 * ifconfig
 * clear
 * macchanger
 * airodump-ng
 * airmon-ng
 * wash
 * bully
 * arpspoof
 * arp-scan
 * tcpdump
 * ettercap

...When ever the program executes a command in a seperate window, it is opening in order for you to see information before making choices, or to execute the final command and let it run in a seperate window. In order to break these command please press "Ctrl" + "C". 

Thanks goes out to Kevin for making the console menu program, which was the shell for this program. Also Thanks goes out to the makers of Kali, and all the above stated programs in order for this program to work. 

If there are any questions or suggestions regarding htis program please feel free to contact me at joejoejoey13@gmail.com.
