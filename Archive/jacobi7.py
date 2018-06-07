#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Topmenu and the submenus are based of the example found at this location http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/
# The rest of the work was done by Matthew Bennett and he requests you keep these two mentions when you reuse the code :-)
# Basic code refactoring by Andrew Scheller
# Established for purposes of using with Moloch by Thomas Blauvelt

# Known Bugs
# If the command window is smaller than the number of options listed (i.e. you have a small cmd prompt for 20+ options, the command will crash

# Bloove Notes
# Changed to set tab width to 4 instead of 2, not sure if that's standard for python, but it was getting to be annoying
# Tried implementing logging, but doesn't work in current state. Need to research more.
	# log = logging.getLogger(__name__)
	# log.addHandler(logging.FileHandler('test.log'))
	# log.setLevel(logging.DEBUG)

# Imports
from __future__ import print_function
from time import sleep
import time
import curses, os, traceback, sys #curses is the interface for capturing key presses on the menu, os launches the files
import pdb #for debugging
import logging #for logging, duh
import datetime

screen = curses.initscr() #initializes a new window for capturing key presses
curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
curses.start_color() # Lets you use colors when highlighting selected menu option
screen.keypad(1) # Capture input from keypad

# Change this to use different colors when highlighting
curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option


MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"
PYTHON = "python"


menu_data = {
# I've commented out the queries I either don't know how to make, or need more research into Moloch to get to function properly
# Start Main Menu
	'title': "Jacobi Viewer for Moloch", 'type': MENU, 'subtitle': "Below you will see predetermined queries for network analysis \n    Please select a query and give the appropriate input to open a Google Chrome session with the selected view",
	'options':[
# Start Global Variable Menu
		{ 'title': "Define Global Variables (date/time/IP)", 'type': MENU, 'subtitle': "Please select an option...",
		'options': [
			{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
			{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },
			{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
			{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
			{ 'title': "Clear IPs for this session", 'type': PYTHON, 'python': 'clear_ip()' },
			{ 'title': "Clear time for this session", 'type': PYTHON, 'python': 'clear_time()' },
			{ 'title': "Set browser to use Google Chrome", 'type': PYTHON, 'python': 'set_browser(google)' },
			{ 'title': "Set browser to use Firefox", 'type': PYTHON, 'python': 'set_browser(firefox)' },
			{ 'title': "Set the Moloch Server location", 'type': PYTHON, 'python': 'set_moloch()' },			
        	]
			},
# End Global Variable Menu
# Start Query Menu
		{ 'title': "Select Moloch Queries", 'type': MENU, 'subtitle': "Please select an option...",
		'options': [
# Not really sure what this query is yet
#	    { 'title': "Characterization of Network Bandwidth Usage", 'type': MENU, 'subtitle': "Please select an option...",
#	      'options': [
#		{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
#		{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },
#		{ 'title': "Clear IPs for this session", 'type': PYTHON, 'python': 'clear_ip()' },
#		{ 'title': "Clear time for this session", 'type': PYTHON, 'python': 'clear_time()' },
#		{ 'title': "Open View", 'type': PYTHON, 'python': 'find_file_uri()' },
#		]
#		},
# Can't get stats page to work at home, must depend on Moloch configuration
#			{ 'title': "Amount of Traffic", 'type': MENU, 'subtitle': "Please select an option...",
#			'options': [
#				{ 'title': "No title", 'type': COMMAND, 'command': 'echo this is a test && sleep 10' },
#				]
#				},
# The need to find highest amount of traffic and least amount was accomplished in the same view, will delete in future versions
#	    { 'title': "Highest Amount of Traffic", 'type': MENU, 'subtitle': "Please select an option...",
#	      'options': [
#		{ 'title': "No title", 'type': COMMAND, 'command': 'echo this is a test && sleep 10' },
#		]
#		},
#	    { 'title': "Least Amount of Traffic", 'type': MENU, 'subtitle': "Please select an option...",
#	      'options': [
#		{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#		]
#		},
			{ 'title': "Inbound Connections", 'type': MENU, 'subtitle': "For this query you need to input your Defended Assets or where you want see traffic going TO \n    You can leave time blank to see the last 6 hours",
			'options': [
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Clear time for this session", 'type': PYTHON, 'python': 'clear_time()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'inbound_connections()' },
				]
				},
			{ 'title': "Outbound Connections", 'type': MENU, 'subtitle': "For this query you need to input your Defended Assets or where you want to see traffic going FROM \n    You can leave time blank to see the last 6 hours",
			'options': [
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Clear time for this session", 'type': PYTHON, 'python': 'clear_time()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'outbound_connections()' },
				]
				},
			{ 'title': "KT-C -> KT-C Connections", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
				{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },			
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'same_connections()' },
				]
				},
			{ 'title': "KT-C -> DAL Connections", 'type': MENU, 'subtitle': "Please select an option... \n    You\'re inputting the Destination IP's when you enter \'Open View\' \n    You still need to set the source IPs in global variables, or in the option on this screen!",
			'options': [
				{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
				{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },			
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'diff_connections()' },
				]
				},
			{ 'title': "DAL -> DAL Connections", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
				{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },			
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'same_connections()' },
				]
				},
			{ 'title': "Server -> Server Traffic", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
				{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },			
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'same_connections()' },
				]
				},					
			{ 'title': "Workstation -> Workstation Connections", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
				{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },			
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'same_connections()' },
				]
				},
# Not sure how to get this to work without compound Moloch views									
#			{ 'title': "Ports/Protocols/Services View", 'type': MENU, 'subtitle': "Please select an option...",
#			'options': [
#				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#				]
#				},
# Changing Most/Least common ports to PPS view, since it appears the query would be the same, just a matter of sorting					
#	    { 'title': "Most Common Ports", 'type': MENU, 'subtitle': "Please select an option...",
#	      'options': [
#					{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#					]
#					},
#	    { 'title': "Least Common Ports", 'type': MENU, 'subtitle': "Please select an option...",
#	      'options': [
#					{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#					]
#					},
			{ 'title': "Find Uncommon Websites", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'uncommon_websites()' },
				]
				},
# Renamed from Scheduled Traffic -> Administrative Traffic, also need to do research to determine all types of normal admin traffic
#			{ 'title': "Administrative Traffic (Patching/Updates)", 'type': MENU, 'subtitle': "Please select an option...",
#			'options': [
#				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#				]
#				},
			{ 'title': "Non-military Connections (Unidentified IPs)", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
				{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },			
				{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
				{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
				{ 'title': "Open View", 'type': PYTHON, 'python': 'nonmil_connections()' },
				]
				},
# Another I need to find the URI for, I think it's unique.txt?counts=1&exp=packets.src&expression=ip.protocol&port=1, but I can't seem to find a way to do compound unique searches
#			{ 'title': "Amounts of data transferred (DNS/Ping)", 'type': MENU, 'subtitle': "Please select an option...",
#			'options': [
#				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#				]
#				},
			{ 'title': "Port/Protocol Mismatch", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
				]
				},
			{ 'title': "Non-standard TLS/SSL", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
				]
				},
			{ 'title': "Encrypted Traffic", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
				]
				},
# No idea how to query this				
#			{ 'title': "Malformed Packets", 'type': MENU, 'subtitle': "Please select an option...",
#			'options': [
#				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#				]
#				},
			{ 'title': "Direct IP Connection Without DNS Query (HTTP/S)", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
				]
				},
# Not really sure what this query is yet
#	    { 'title': "DC/ TACACS/ AUTH Svs. Servers", 'type': MENU, 'subtitle': "Please select an option...",
#	      'options': [
#					{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#					]
#					},
# Not really sure what this query is yet
#	    { 'title': "OWTs + Flow Data", 'type': MENU, 'subtitle': "Please select an option...",
#	      'options': [
#					{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
#					]
#					},
			{ 'title': "Administrative traffic", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
				]
				},
			{ 'title': "Ingress/Egress Points Monitoring", 'type': MENU, 'subtitle': "Please select an option...",
			'options': [
				{ 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
				]
				},
			]
			},
# End Query Menu
# Start Help Menu
		{ 'title': "Help", 'type': MENU, 'subtitle': "Please select a topic to get more information...",
		'options': [
			{ 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
			{ 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },
			{ 'title': "Input Start Time", 'type': PYTHON, 'python': 'starttimeinput()' },
			{ 'title': "Input End Time", 'type': PYTHON, 'python': 'endtimeinput()' },
			{ 'title': "Clear IPs for this session", 'type': PYTHON, 'python': 'clear_ip()' },
			{ 'title': "Clear time for this session", 'type': PYTHON, 'python': 'clear_time()' },
		]
		},
# End Help Menu
	]
}
# End Main Menu

###########################################Query Functions###########################################
######################################Global Variable Functions######################################
# Start browser selection functions
firefox = "nohup firefox '"
google = "nohup google-chrome '"
browser_default = google
moloch_default = 'http://192.168.108.136:8005'

def set_browser(user_browser):
	if user_browser[6:13] == firefox[6:13]:
		global browser
		browser = firefox
	elif user_browser[6:12] == google[6:12]:
		global browser
		browser = google
	else:
		print('There\'s something wrong with the browser you selected')
		os.system('sleep 3')

def set_moloch():
	moloch = 'http://192.168.108.136:8005'
	global moloch
	global call_moloch
	try: moloch
	except NameError:
		print('There was an error using this Moloch Server')
	else:
		print ('There\'s no error checking for this part, what you enter is what you get\n')
		moloch = raw_input('Type the Moloch IP:Port Number (but don\'t use quotes!) \nExample "127.0.0.1:8005": ')
#	call_moloch = browser + moloch
	
# End browser selection functions

# Start insert target file function
# This function will accept user input for IP addresses	 
def iplist():
	global ip_range
	ip_range = raw_input('Place an input here: ').split(' ')
	return
#End insert target file location

# Start insert ips to console function
# This function will accept user input for targets file
def ipfile():
	global ip_targets
	ip_target_file = raw_input('Place target file location here: ')
	try: ip_holder = open(ip_target_file,'r')
	except IOError:
		os.system('clear')
		print('Either I can\'t read that file, or it\'s not a file')
		os.system('sleep 3')
		return
	ip_targets = ip_holder.readlines()
#How you specify individual IPs in the target file input is below
#print (ip_targets[ip])
# End insert ips to console function

# Start starttime function
def starttimeinput():
	global starttime #Define starttime as a global variable to use in other functions of the program
	inputstartyear = raw_input('Input start year: ') #Have user input each piece of "datetime.datetime" to calculate epoch offset
	inputstartmonth = raw_input('Input start month: ')
	inputstartdate = raw_input('Input start day: ')
	inputstarthour = raw_input('Input start hour: ')
	inputstartmin = raw_input('Input start minute: ')
	#Cast each input as an int to properly pass to datetime.datetime
	try: int(inputstartyear),int(inputstartmonth),int(inputstartdate),int(inputstarthour),int(inputstartmin)
	except ValueError:
		os.system('clear')
		print('You didn\'t enter anything or entered a funky date \nGo back and try again')
		os.system('sleep 3')
		return
	else:
		startdatetime_input = (int(inputstartyear),int(inputstartmonth),int(inputstartdate),int(inputstarthour),int(inputstartmin))
	#Set startdatetime_input to seconds to calculate offset
	try: timeoffset = datetime.datetime(int(inputstartyear),int(inputstartmonth),int(inputstartdate),int(inputstarthour),int(inputstartmin)) - datetime.timedelta(seconds = time.timezone)
	except OverflowError:
		os.system('clear')
		print('What number did you even enter?\nTry and input a date in this century')
		os.system('sleep 3')
		return
	except ValueError:
		os.system('clear')
		print('There\'s only 12 months in a year\nThere\'s no data on Marchtember Oneteenth')
		os.system('sleep 3')
		return		
	else:
	#Calculate offset based off Moloch's epoch start time which is 12/31/1969 18:00 and add 5 hours to timeoffset to calculate difference between UTC and Central
		starttime = ((timeoffset + datetime.timedelta(hours=5)) - datetime.datetime(1969,12,31,18)).total_seconds() 
#In the future, try to manipulate timeoffset to be based off timezone, so the 5 doesn't need to be hardcoded
# End starttime function

# Start endtime function
def endtimeinput():
#Define endtime as a global variable to use in other functions of the program
#Comments are the same as starttimeinput()
	global endtime
	inputendyear = raw_input('Input end year: ')
	inputendmonth = raw_input('Input end month: ')
	inputenddate = raw_input('Input end day: ')
	inputendhour = raw_input('Input end hour: ')
	inputendmin = raw_input('Input end minute: ')
	try: int(inputendyear),int(inputendmonth),int(inputenddate),int(inputendhour),int(inputendmin)
	except ValueError:
		os.system('clear')
		print('You didn\'t enter anything or entered a funky date \nGo back and try again')
		os.system('sleep 3')
		return		
	else:
		enddatetime_input = (int(inputendyear),int(inputendmonth),int(inputenddate),int(inputendhour),int(inputendmin))
	try: timeoffset = datetime.datetime(int(inputendyear),int(inputendmonth),int(inputenddate),int(inputendhour),int(inputendmin)) - datetime.timedelta(seconds = time.timezone)
	except OverflowError:
		os.system('clear')
		print('What number did you even enter?\nTry and input a date in this century')
		os.system('sleep 3')
		return
	except ValueError:
		os.system('clear')
		print('There\'s only 12 months in a year\nThere\'s no data on Marchtember Oneteenth')
		os.system('sleep 3')
		return
	else:		
		endtime = ((timeoffset + datetime.timedelta(hours=5)) - datetime.datetime(1969,12,31,18)).total_seconds()
# End endtime function

# Start clear functions
def clear_ip():
	global ip_range
	global ip_target_file
	ip_range = ''
	ip_target_file = ''

def clear_time():
	global endtime
	global starttime
	endtime = ''
	starttime = ''
# End clear functions

###############################################Moloch Query Functions###############################################
# Start inbound connections query function
def inbound_connections():
#Added browser selection to each function that needs to open the browser
	try: browser
	except NameError:
		try: moloch
		except NameError:
			call_moloch = browser_default + moloch_default
		else:
			call_moloch = browser_default + moloch
	else:
		try: moloch
		except NameError:		
			call_moloch = browser + moloch_default
		else:
			call_moloch = browser + moloch

	global endtime
	global starttime

	try: starttime,endtime
	except NameError:
		print ('You did not input a start and/or end time')
		print ('So check out the last 6 hours of inbound connections')
		os.system (call_moloch + "/unique.txt?counts=1&exp=ip.dst&date=6' 2>/dev/null &")
		os.system ('sleep 3')
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Inbound Connections " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=ip.dst&date=6' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()		
	else:
		timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
		os.system (call_moloch + "/unique.txt?counts=1&exp=ip.dst" + timestamp + "' 2>/dev/null &")
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Inbound Connections " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=ip.dst" + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()		
# End inbound connections query function

# Start outbound connections query function
def outbound_connections():
#Added browser selection to each function that needs to open the browser
	try: browser
	except NameError:
		try: moloch
		except NameError:
			call_moloch = browser_default + moloch_default
		else:
			call_moloch = browser_default + moloch
	else:
		try: moloch
		except NameError:		
			call_moloch = browser + moloch_default
		else:
			call_moloch = browser + moloch

	global endtime
	global starttime

	try: starttime,endtime
	except NameError:
		print ('You did not input a start and/or end time')
		print ('So check out the last 6 hours of outbound connections')
		os.system (call_moloch + "/unique.txt?counts=1&exp=ip.src&date=6' 2>/dev/null &")
		os.system ('sleep 3')
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Outbound Connections " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=ip.src&date=6' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()
	else:
		timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
		os.system (call_moloch + "/unique.txt?counts=1&exp=ip.src" + timestamp + "' 2>/dev/null &")
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Outbound Connections " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=ip.src" + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()
# End outbound connections query function

# Start same -> same connections function
def same_connections():
#Added browser selection to each function that needs to open the browser
	try: browser
	except NameError:
		try: moloch
		except NameError:
			call_moloch = browser_default + moloch_default
		else:
			call_moloch = browser_default + moloch
	else:
		try: moloch
		except NameError:		
			call_moloch = browser + moloch_default
		else:
			call_moloch = browser + moloch

	try: ip_range
	except NameError:		
		try: ip_targets
		except NameError:
			print ('You need to set your targets for this query to work')
			os.system ('sleep 3')
		else:
			try: starttime,endtime
			except NameError:
				print ('You did not input a start and/or end time')
				print ('So we\'ll just use the last 6 hours')
				timestamp = '&date=6'
				os.system ('sleep 3')
			else:
				timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
			i = 0
			uri_ip_src = ''
			uri_ip_dst = ''
			while i < (len(ip_targets)):
				map(str.strip, ip_targets)
				uri_ip_src_repeater = ('ip.src%3D%3D' + ip_targets[i])
				uri_ip_src = uri_ip_src + '||' + uri_ip_src_repeater
				uri_ip_dst_repeater = ('ip.dst%3D%3D' + ip_targets[i])
				uri_ip_dst = uri_ip_dst + '||' + uri_ip_dst_repeater
				i += 1
			url = '&expression=' + "(" + (uri_ip_src[2:]) + ")" + "%26(" + (uri_ip_dst[2:]) + ")"
			os.system (call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
			#Write output to file functions
			os.system('sleep 1')
			outfile=open("jacobi_queries.txt","a")
			outfile.write("Same -> Same Connections " + str(datetime.datetime.now())[:16])
			outfile.write("\n")
			outfile.write(call_moloch + "/sessions?" + url + timestamp + "' 2>/dev/null &")
			outfile.write("\n")
			outfile.close()		
	else:
		try: starttime,endtime
		except NameError:
			print ('You did not input a start and/or end time')
			print ('So we\'ll just use the last 6 hours')
			timestamp = '&date=6'
			os.system ('sleep 3')
		else:
			timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
		i = 0
		uri_ip_src = ''
		uri_ip_dst = ''
		while i < (len(ip_range)):
			uri_ip_src_repeater = ('ip.src%3D%3D' + ip_range[i])
			uri_ip_src = uri_ip_src + '||' + uri_ip_src_repeater
			uri_ip_dst_repeater = ('ip.dst%3D%3D' + ip_range[i])
			uri_ip_dst = uri_ip_dst + '||' + uri_ip_dst_repeater
			i += 1			
		url = '&expression=' + "(" + (uri_ip_src[2:]) + ")" + "%26(" + (uri_ip_dst[2:]) + ")"
		os.system (call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Same -> Same Connections " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()
#		os.system (call_moloch + "/unique.txt?" + timestamp + "counts=1&exp=ip.dst' 2>/dev/null &") # not sure why this was here, might be beneficial to view this in a unique page though
# End same -> same connections function

# Start same -> diff connections function
def diff_connections():
#Added browser selection to each function that needs to open the browser
	try: browser
	except NameError:
		try: moloch
		except NameError:
			call_moloch = browser_default + moloch_default
		else:
			call_moloch = browser_default + moloch
	else:
		try: moloch
		except NameError:		
			call_moloch = browser + moloch_default
		else:
			call_moloch = browser + moloch

	try: ip_range
	except NameError:		
		try: ip_targets
		except NameError:
			print ('You need to set your targets for this query to work')
			os.system ('sleep 3')
		else:
			try: starttime,endtime
			except NameError:
				print ('You did not input a start and/or end time')
				print ('So we\'ll just use the last 6 hours')
				timestamp = '&date=6'
				os.system ('sleep 3')
			else:
				timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
			os.system('clear')
			print('Don\'t forget this your DESTINATION IPs')
			ip_target_dst_file = raw_input('Place target file location here: ')
			try: ip_holder = open(ip_target_dst_file,'r')
			except IOError:
				os.system('clear')
				print('Either I can\'t read that file, or it\'s not a file')
				os.system('sleep 3')
				return
			ip_dst_targets = ip_holder.readlines()
			i = 0
			uri_ip_src = ''
			uri_ip_dst = ''
			while i < (len(ip_targets)):
				uri_ip_src_repeater = ('ip.src%3D%3D' + ip_targets[i])
				uri_ip_src = uri_ip_src + '||' + uri_ip_src_repeater
				i += 1
			i = 0
			while i < (len(ip_dst_targets)):
				uri_ip_dst_repeater = ('ip.dst%3D%3D' + ip_targets[i])
				uri_ip_dst = uri_ip_dst + '||' + uri_ip_dst_repeater
				i += 1			
			url = '&expression=' + "(" + (uri_ip_src[2:]) + ")" + "%26(" + (uri_ip_dst[2:]) + ")"
			os.system (call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
			#Write output to file functions
			outfile=open("jacobi_queries.txt","a")
			outfile.write("Same -> Diff Connections " + str(datetime.datetime.now())[:16])
			outfile.write("\n")
			outfile.write(call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
			outfile.write("\n")
			outfile.close()
	else:
		try: starttime,endtime
		except NameError:
			print ('You did not input a start and/or end time')
			print ('So we\'ll just use the last 6 hours')
			timestamp = '&date=6'
			os.system ('sleep 3')
		else:
			timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
		ip_target_dst_file = raw_input('Place target file location here: ')
		ip_holder = open(ip_target_dst_file,'r')
		ip_dst_targets = ip_holder.readlines()
		i = 0
		uri_ip_src = ''
		uri_ip_dst = ''
		while i < (len(ip_targets)):
			uri_ip_src_repeater = ('ip.src%3D%3D' + ip_targets[i])
			uri_ip_src = uri_ip_src + '||' + uri_ip_src_repeater
			i += 1
		while i < (len(ip_dst_targets)):
			uri_ip_dst_repeater = ('ip.dst%3D%3D' + ip_dst_targets[i])
			uri_ip_dst = uri_ip_dst + '||' + uri_ip_dst_repeater
			i += 1			
		url = '&expression=' + "(" + (uri_ip_src[2:]) + ")" + "%26(" + (uri_ip_dst[2:]) + ")"
		os.system (call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Same -> Diff Connections " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()
#		os.system (call_moloch + "/unique.txt?" + timestamp + "counts=1&exp=ip.dst' 2>/dev/null &") # not sure why this was here, might be beneficial to view this in a unique page though
# End same -> diff connections function

# Start nonmil connections function
def nonmil_connections():
#Added browser selection to each function that needs to open the browser
	try: browser
	except NameError:
		try: moloch
		except NameError:
			call_moloch = browser_default + moloch_default
		else:
			call_moloch = browser_default + moloch
	else:
		try: moloch
		except NameError:		
			call_moloch = browser + moloch_default
		else:
			call_moloch = browser + moloch

	try: ip_range
	except NameError:		
		try: ip_targets
		except NameError:
			print ('You need to set your targets for this query to work')
			os.system ('sleep 3')
		else:
			try: starttime,endtime
			except NameError:
				print ('You did not input a start and/or end time')
				print ('So we\'ll just use the last 6 hours')
				timestamp = '&date=6'
				os.system ('sleep 3')
			else:
				timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
			os.system('clear')
			print('Don\'t forget this your DESTINATION IPs')
			ip_target_dst_file = raw_input('Place target file location here: ')
			ip_holder = open(ip_target_dst_file,'r')
			ip_dst_targets = ip_holder.readlines()
			i = 0
			uri_ip_src = ''
			uri_ip_dst = ''
			while i < (len(ip_targets)):
				uri_ip_src_repeater = ('ip.src!%3D' + ip_targets[i])
				uri_ip_src = uri_ip_src + '%26' + uri_ip_src_repeater
				i += 1
			i = 0
			while i < (len(ip_dst_targets)):
				uri_ip_dst_repeater = ('ip.dst!%3D' + ip_targets[i])
				uri_ip_dst = uri_ip_dst + '%26' + uri_ip_dst_repeater
				i += 1			
			url = '&expression=' + "(" + (uri_ip_src[3:]) + ")" + "%26(" + (uri_ip_dst[3:]) + ")"
			os.system (call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
			#Write output to file functions
			outfile=open("jacobi_queries.txt","a")
			outfile.write("Non Military Connections " + str(datetime.datetime.now())[:16])
			outfile.write("\n")
			outfile.write(call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
			outfile.write("\n")
			outfile.close()
	else:
		try: starttime,endtime
		except NameError:
			print ('You did not input a start and/or end time')
			print ('So we\'ll just use the last 6 hours')
			timestamp = '&date=6'
			os.system ('sleep 3')
		else:
			timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
		ip_target_dst_file = raw_input('Place target file location here: ')
		ip_holder = open(ip_target_dst_file,'r')
		ip_dst_targets = ip_holder.readlines()
		i = 0
		uri_ip_src = ''
		uri_ip_dst = ''
		while i < (len(ip_targets)):
			uri_ip_src_repeater = ('ip.src%3D%3D' + ip_targets[i])
			uri_ip_src = uri_ip_src + '||' + uri_ip_src_repeater
			i += 1
		while i < (len(ip_dst_targets)):
			uri_ip_dst_repeater = ('ip.dst%3D%3D' + ip_dst_targets[i])
			uri_ip_dst = uri_ip_dst + '||' + uri_ip_dst_repeater
			i += 1			
		url = '&expression=' + "(" + (uri_ip_src[2:]) + ")" + "%26%26(" + (uri_ip_dst[2:]) + ")"
		os.system (call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Non Military Connections " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/sessions?" + timestamp + url + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()		
#		os.system (call_moloch + "/unique.txt?" + timestamp + "counts=1&exp=ip.dst' 2>/dev/null &") # not sure why this was here, might be beneficial to view this in a unique page though
# End same -> diff connections function

# Start uncommon websites
# Searches by negation of the following:
# .com, .org, .net, .edu, .biz, .gov, .mil, .info, .tv, .us
def uncommon_websites():
#Added browser selection to each function that needs to open the browser
	try: browser
	except NameError:
		try: moloch
		except NameError:
			call_moloch = browser_default + moloch_default
		else:
			call_moloch = browser_default + moloch
	else:
		try: moloch
		except NameError:		
			call_moloch = browser + moloch_default
		else:
			call_moloch = browser + moloch

	global endtime
	global starttime

	def_sites = ('.com','.org','.net','.edu','.biz','.gov','.mil','.info','.tv','.us')
	i=0
	http_sites = ''
	dns_sites = ''
	while i < (len(def_sites)):
		http_sites_repeater = ('host.http!%3D*' + def_sites[i])
		dns_sites_repeater = ('host.dns!%3D*' + def_sites[i])
		http_sites = http_sites + "%26" + http_sites_repeater
		dns_sites = dns_sites + "%26" + dns_sites_repeater
		i+=1
	url = '&expression=' + http_sites[3:] + "%26" + dns_sites[3:]
	try: starttime,endtime
	except NameError:
		timestamp = '&date=6'
		print ('You did not input a start and/or end time')
		print ('So check out the last 6 hours of outbound connections')
		os.system (call_moloch + "/unique.txt?counts=1&exp=host.http" + url + timestamp + "' 2>/dev/null &")
		os.system (call_moloch + "/unique.txt?counts=1&exp=host.dns" + url + timestamp + "' 2>/dev/null &")
		os.system (call_moloch + "/sessions?" + url + timestamp + "' 2>/dev/null &")
		os.system ('sleep 3')
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Uncommon Websites Visited " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=host.http" + url + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=host.dns" + url + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.write(call_moloch + "/sessions?" + url + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()
	else:
		timestamp = str('&stopTime='+str(int(endtime))+'&startTime='+str(int(starttime)))
		os.system (call_moloch + "/unique.txt?counts=1&exp=host.http" + url + timestamp + "' 2>/dev/null &")
		os.system (call_moloch + "/unique.txt?counts=1&exp=host.dns" + url + timestamp + "' 2>/dev/null &")
		os.system (call_moloch + "/sessions?" + url + timestamp + "' 2>/dev/null &")
		#Write output to file functions
		outfile=open("jacobi_queries.txt","a")
		outfile.write("Uncommon Websites Visited " + str(datetime.datetime.now())[:16])
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=host.http" + url + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.write(call_moloch + "/unique.txt?counts=1&exp=host.dns" + url + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.write(call_moloch + "/sessions?" + url + timestamp + "' 2>/dev/null &")
		outfile.write("\n")
		outfile.close()
# End uncommon websites
# Used this query to test inputting targets list at first, leaving in for nostalgia
# Start test query function
#def find_file_uri():
#	global ip_range
#	global ip_target_file
#	try: ip_range[0]
#	except NameError:
#		print ('You did not list IPs')
#	else:
#		i = 0
#		uri_ip2 = ''
#		while i < (len(ip_range)):
#			uri_ip1 = ('ip%3D%3D' + ip_range[i])
#			uri_ip2 = uri_ip2 + '||' + uri_ip1
#			i += 1
#		url = '&expression=' + (uri_ip2[2:])
#		timestamp = 'stopTime=1525698272&startTime=1524225872'
#		os.system ("google-chrome '192.168.108.136:8005/sessions?" + timestamp + url + "' &")
#	try: ip_targets[0]
#	except NameError:
#		print ('You did not input a target list')
#	else:
#		i = 0
#		uri_ip2 = ''
#		while i < (len(ip_targets)):
#			uri_ip1 = ('ip%3D%3D' + ip_targets[i])
#			uri_ip2 = uri_ip2 + '||' + uri_ip1
#			i += 1
#		url = '&expression=' + (uri_ip2[2:])
#		timestamp = 'stopTime=1525698272&startTime=1524225872'
#		os.system ("google-chrome '192.168.108.136:8005/sessions?" + timestamp + url + "' 2>/dev/null &")
#	os.system('sleep 10')
# End test query function

###########################################END Query Functions###########################################

# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):

  # work out what text to display as the last menu option
	if parent is None:
		lastoption = "Exit"
	else:
		lastoption = "Return to %s menu" % parent['title']
	optioncount = len(menu['options']) # how many options in this menu

	pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
	oldpos=None # used to prevent the screen being redrawn every time
	x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program

  # Loop until return key is pressed
	while x !=ord('\n'):
		if pos != oldpos:
			oldpos = pos
			screen.border(0)
			screen.addstr(2,2, menu['title'], curses.A_STANDOUT) # Title for this menu
			screen.addstr(4,4, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu

      # Display all the menu items, showing the 'pos' item highlighted
			for index in range(optioncount):
				textstyle = n
				if pos==index:
					textstyle = h
				try: screen.addstr(7+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
				except Exception:
					curses.endwin()
					os.system('clear')
					print('You need to make the terminal window bigger for this script to work')
					os.system('sleep 3')
					exit(0)
      # Now display Exit/Return at bottom of menu
			textstyle = n
			if pos==optioncount:
				textstyle = h
			screen.addstr(7+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
			screen.refresh()
      # finished updating screen

		x = screen.getch() # Gets user input

    # What is user input?
		if x >= unichr(1) and x <= unichr(int(optioncount+1)):
			pos = x - unichr(0) - 1 # convert keypress back to a number, then subtract 1 to get index
		elif x == 258: # down arrow
			if pos < optioncount:
				pos += 1
			else: pos = 0
		elif x == 259: # up arrow
			if pos > 0:
				pos += -1
			else: pos = optioncount

  # return index of the selected item
	return pos

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
	optioncount = len(menu['options'])
	exitmenu = False
	while not exitmenu: #Loop until the user exits the menu
		getin = runmenu(menu, parent)
		if getin == optioncount:
			exitmenu = True
		elif menu['options'][getin]['type'] == COMMAND:
			curses.def_prog_mode()    # save curent curses environment
			os.system('reset')
			screen.clear() #clears previous screen
			os.system(menu['options'][getin]['command']) # run the command
			screen.clear() #clears previous screen on key press and updates display based on pos
			curses.reset_prog_mode()   # reset to 'current' curses environment
			curses.curs_set(1)         # reset doesn't do this right
			curses.curs_set(0)
			os.system('amixer cset numid=3 2') # Sets audio output on the pi back to HDMI
		elif menu['options'][getin]['type'] == MENU:
			screen.clear() #clears previous screen on key press and updates display based on pos
			processmenu(menu['options'][getin], menu) # display the submenu
			screen.clear() #clears previous screen on key press and updates display based on pos
		elif menu['options'][getin]['type'] == EXITMENU:
			exitmenu = True
		elif menu['options'][getin]['type'] == PYTHON:
			curses.def_prog_mode()    # save curent curses environment
			os.system('reset')
			screen.clear() #clears previous screen
			exec menu['options'][getin]['python']
			screen.clear() #clears previous screen on key press and updates display based on pos
			curses.reset_prog_mode()   # reset to 'current' curses environment
			curses.curs_set(1)         # reset doesn't do this right
			curses.curs_set(0)
			#continue

# Main program

# Exception Handler
try: 
	processmenu(menu_data)
except Exception as exception:
	curses.endwin()
	os.system('clear')
	traceback.print_exc()
	sys.exit(1)
	screen.keypad(0)

curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
os.system('clear')
