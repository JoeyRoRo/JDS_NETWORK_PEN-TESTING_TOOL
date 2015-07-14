#!/usr/bin/env python
import subprocess, os, sys, time

'''
This part of the program will sort a rainbow table. The user is promted for what
rainbow table to sort and then uses 'rtsort' to sort the table.

If there are any questions please email me at joejoejoey13@gmail.com. 
'''
short_name = 'Rainbow Tables'
disp_name = 'Sort a rainbow table'
otype = 'Routine'
default_path = '/usr/share/rainbowcrack/'
answers = []

# Main definition
def run():
	global answers; answers = []
	subprocess.call('clear', shell=True)
# This section prompts the user for the needed information
	i = 0
	while True:
		print('Here is a list of the rainbow tables from the default ' \
				'location...\n ')
# This section prints the default location for where rainbow tables are stored		
		subprocess.call('ls /usr/share/rainbowcrack/ | grep "\.rt"', \
						shell=True)
		ans = raw_input('\nWhat rainbow table would you like to sort: ')
# This section removes quotes so a user can drag and drop a file
		if ans[0] == "\'": ans = ans[1:]
		if ans.endswith("\' "): ans = ans[:-2]
# If the users input is validated, then it is added to the answers array
		if validate(ans):
			answers.append(ans)
			break
	wait_timer('Sorting your rainbow table..')		
# This section attempts the sorting of the rainbow table command
	try:		
		subprocess.call('rtsort %s' % answers[0], shell=True)
		raw_input('Finsihed sorting rainbow table '+answers[0]+'\nPress ' \
					'enter to return to the main menu.')
		return
	except:
		raw_input('Failed to sort your table. Please check to ensure you ' \
					'are inputing a valid rainbow table.\nPress enter to ' \
					'return to the main menu')

# Definition to validate user input
def validate(ans):
	if (os.path.isfile(default_path+ans)) or (os.path.isfile(ans)):
		if ans.endswith('.rt'): return True
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