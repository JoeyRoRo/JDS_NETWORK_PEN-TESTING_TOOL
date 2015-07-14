#!/usr/bin/env python
import subprocess, os, re, sys, time

'''
This section of the program will use a rainbow table to crack a hash. 
'''
short_name = 'Rainbow Tables'
disp_name = 'Crack hash using an existing rainbow table'
otype = 'Routine'
need = ['', 'How do you want to input your hash to crack?\n 1.) Enter hash ' \
		'manually\n 2.) Enter a hash list file\n\n ']
default_path = '/usr/share/rainbowcrack/'
answers = []

# Main definition
def run():
	global answers; answers = []
	subprocess.call('clear', shell=True)
# This section prompts the user for the needed information	
	i = 0
	while i < len(need):
		if i == 0:
# This section saves and prints the rainbow tables saved in the default location		
			rt_tables = subprocess.check_output('ls /usr/share/rainbowcrack/' \
												' | grep "\.rt"', shell=True)
			print('Here is a list of the rainbow tables from the default ' \
					'location...\n ')
			print(rt_tables)
			ans = raw_input('\nWhat rainbow table would you like to use: ')
# This section removes quotes so a user can drag and drop a file
			if ans[0] == "\'": ans = ans[1:]
			if ans.endswith("\' "): ans = ans[:-2]
		if i == 1: ans = input(need[i])
# If the users input is validated, then the answer is added to the answers array		
		if validate(ans, i):
			answers.append(ans)
			i += 1
# This section attempts the crack the hash with the rainbow table
# If the user wanted to crack a single hash, execute the following
	if answers[1] == 1:
		enter_hash = raw_input("What is the hash you would like to crack?\n")
		if not enter_hash == '': 
			wait_timer('Running your rainbow table against your hash..')
			subprocess.call('rcrack '+answers[0]+' -h '+enter_hash, shell=True)
# If the user wanted to crack a list of hashes, execute the following
	if answers[1] == 2:
		hash_file = raw_input('Hash files process by one line = one hash ' \
								'\nWhere is your hash list file: ')
# This section removes quotes so a user can drag and drop a file
		if hash_file[0] == "\'": hash_file = hash_file[1:]
		if hash_file.endswith("\' "): hash_file = hash_file[:-2]
		if os.path.isfile(hash_file): 
			wait_timer('Running your rainbow table against your hash list..')
			subprocess.call('rcrack '+answers[0]+' -l '+hash_file, shell=True)
		
	raw_input('Finished attempting to crack your hash(s). \nPress enter to ' \
				'return to the main menu.')
	return

# Definition to validate user input
def validate(ans, i):
	if i == 0:
		if (os.path.isfile(default_path+ans)) or (os.path.isfile(ans)):
			if ans.endswith('.rt'): return True	
	if i == 1:
		if re.match(r'[1-2]', str(ans)): return True
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