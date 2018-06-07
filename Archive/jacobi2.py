#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Topmenu and the submenus are based of the example found at this location http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/
# The rest of the work was done by Matthew Bennett and he requests you keep these two mentions when you reuse the code :-)
# Basic code refactoring by Andrew Scheller
# Established for purposes of using with Moloch by Thomas Blauvelt

# Known Bugs
# If the command window is smaller than the number of options listed (i.e. you have a small cmd prompt for 20+ options, the command will crash

# Imports
from __future__ import print_function
from time import sleep
import curses, os, traceback, sys #curses is the interface for capturing key presses on the menu, os launches the files
import pdb #for debugging
import logging #for logging, duh

# Tried implementing logging, but doesn't work in current state. Need to research more.
# log = logging.getLogger(__name__)
# log.addHandler(logging.FileHandler('test.log'))
# log.setLevel(logging.DEBUG)

screen = curses.initscr() #initializes a new window for capturing key presses
curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
curses.start_color() # Lets you use colors when highlighting selected menu option
screen.keypad(1) # Capture input from keypad

# Change this to use different colors when highlighting
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"
PYTHON = "python"


menu_data = {
  'title': "Jacobi Viewer for Moloch", 'type': MENU, 'subtitle': "Below you will see predetermined queries for network analysis \n    Please select a query and give the appropriate input to open a Google Chrome session with the selected view",
  'options':[
    { 'title': "Find Common File Strings from URIs", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
        { 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },
        { 'title': "Open View", 'type': PYTHON, 'python': 'find_file_uri()' },
        ]
        },
    { 'title': "Characterization of Network Bandwidth Usage", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "Input IP Address", 'type': PYTHON, 'python': 'iplist()' },
        { 'title': "Input targets file", 'type': PYTHON, 'python': 'ipfile()' },
        { 'title': "Clear IPs for this session", 'type': PYTHON, 'python': 'clear_ip()' },
        ]
        },
    { 'title': "Highest Amount of Traffic", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'echo this is a test && sleep 10' },
        ]
        },
    { 'title': "Least Amount of Traffic", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Inbound Connections", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Outbound Connections", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "KT-C -> KT-C Connections", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "KT-C -> DAL Connections", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "DAL -> DAL Connections", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Most Common Ports", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Least Common Ports", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Common and Uncommon Websites", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Scheduled Traffic (Patching/Updates)", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Non-military Connections", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Amounts of data transferred (DNS/Ping)", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
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
    { 'title': "Workstation -> Workstation Connections", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Malformed Packets", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Direct IP Connection Without DNS Query (HTTP/S)", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "Server -> Server Traffic", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "DC/ TACACS/ AUTH Svs. Servers", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
    { 'title': "OWTs + Flow Data", 'type': MENU, 'subtitle': "Please select an option...",
      'options': [
        { 'title': "No title", 'type': COMMAND, 'command': 'firefox localhost &' },
        ]
        },
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
}

###########################################Query Functions###########################################
# This function will accept user input for IP addresses
def iplist():
#  pdb.set_trace() # inline debugging
  global ip_range
  ip_range = raw_input('Place an input here: ').split(' ')
  print (ip_range[0])
  os.system("sleep 3")
  return

# This function will accept user input for targets file
def ipfile():
  global ip_targets
  ip_target_file = raw_input('Place target file location here: ')
  ip_holder = open(ip_target_file,'r')
  ip_targets = ip_holder.readlines()
  for ip in range(len(ip_targets)):
    print (ip_targets[ip])
  os.system('sleep 3')

def clear_ip():
  global ip_range
  global ip_target_file
  ip_range = ''
  ip_target_file = ''

def find_file_uri():
  global ip_range
  global ip_target_file

  try: ip_range[0]
  except NameError:
    print ('The IP input has been cleared')
  else:
    for i in (ip_range):
      print (i)

  try: ip_target_file[0]
  except NameError:
    print ('The IP input has been cleared')
  else:
    for i in (ip_targets):
      print(i)

  os.system('sleep 3')
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
        screen.addstr(7+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
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

curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
os.system('clear')\
