#!/usr/bin/env python
import subprocess, re, sys, time

'''
This section of the program will help a user create a rainbow table. The user is
prompted for all the needed information and then the program uses the 'rtgen'
program to make the rainbow table.

If there are any questions please email me at joejoejoey13@gmail.com. 
'''
short_name = 'Rainbow Tables'
disp_name = 'Create a rainbow table'
otype = 'Routine'
need = ['What kind of algorithm would you like to use: ', 'What character ' \
		'set would you like to use: ', 'What is the minimum length for the' \
		' password: ', 'What is the maximum length for the password: ', \
		'What table index would you like to use: ', 'What chain length would' \
		' you like to use: ', 'What chain number would you like to use: ', \
		'What part index would you like to use: ']
algos = {'1':'lm', '2':'ntlm', '3':'md5', '4':'sha1', '5':'mysqlsha1', \
		'6':'ntlmchall', '7':'oracle', '8':'md5-half'}
char_sets = {'1':'numeric', '2':'alpha', '3':'alpha-numeric', \
			'4':'loweralpha', '5':'loweralpha-numeric', '6':'mixalpha', \
			'7':'mixalpha', '8':'ascii-32-95', '9':'ascii-32-65-123-4', \
			'10':'alpha-numeric-symbol32-space'}
answers = []

# Main definition
def run():
	global answers; answers = []
# This section prompts the user for all needed information
	i = 0
	while i < len(need):
		subprocess.call('clear', shell=True)
		if i == 0:
			print('1.) lm \n2.) ntlm \n3.) md5 \n4.) sha1 \n5.) mysqlsha1' \
				' \n6.) ntlmchall \n7.) oracle-SYSTEM \n8.)' \
				' md5-half \n')
			print('Refer to Readme.txt for common uses of these algorithms\n')
		if i == 1: print('1.) Numbers only \n2.) Upper case characters' \
						' \n3.) Upper case characters and numbers \n4.)' \
						' Lowercase characters \n5.) Lower case ' \
						'characters and numbers \n6.) Upper and lower ' \
						'case characters \n7.) Upper and lower case ' \
						'characters and numbers \n8.) Upper and lower ' \
						'case characters, number, and symbols \n9.) ' \
						'Upper case characters, numbers, and symbols ' \
						'\n10.) Lower case character, numbers, and symbols\n')
		if i == 2: print('Most passwords are a minimum of 8 characters.\n')
		if i == 3: print('Most password are a maximum of 64 characters.\n')
		if re.match('[4-7]', str(i)): print('For more information on ' \
							'this item, please refer to the Readme.txt\n')

		ans = input(need[i])
# If the users answer is validated, then it is added to the answers array
		if validate(ans, i):
			answers.append(ans)
			i += 1
# This section sets the algorithm and charater types to usable data before running the commands
	algo_type = str(answers[0])
	answers[0] = algos[algo_type]
	answers[1] = char_sets[str(answers[1])]
# This section prints all the settings before going through with creating the table
	subprocess.call('clear', shell=True)
	print "Rainbow table settings...\n"
	print "Algorithm type: "+answers[0]
	print "Character set: "+answers[1]
	print "Password minimum characters: "+str(answers[2])
	print "Password maximum characters: "+str(answers[3])
	print "Table index: "+str(answers[4])
	print "Chain length: "+str(answers[5])
	print "Chain number: "+str(answers[6])
	print "Part index: "+str(answers[7])	
	raw_input('\nIf your rainbow table does not create with the above' \
			' settings, please reference the rtgen --help file for ' \
			'algorithm type and settings. \nPress enter to create a' \
			' rainbow table with the above settings.')
	wait_timer('Starting to create your rainbow table..')
# This section attempts to create the rainbow table from the users given info
	subprocess.call('rtgen %s %s %s %s %s %s %s %s' % (answers[0], \
					answers[1], answers[2], answers[3], answers[4], \
					answers[5], answers[6], answers[7]), shell=True)

	raw_input('Finshed making rainbow table. You can find your table ' \
				'save in...\n     /usr/share/rainbowcrack/ \nPress enter' \
				' to return to the main menu.')
	return

# Definition to validate the users input
def validate(ans, i):
	if i == 0:
		if re.match('[1-8]', str(ans)): return True
	if i == 1:
		if re.match('[0-9]', str(ans)) or re.match('10', ans): return True
	if re.match('[2-7]', str(i)):
		if int(ans): 
			return True
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