#!/usr/bin/env python

__version__ = 0.01

#### Script will:
#### display last news update before updating
#### update and upgrade from official repo
#### update AUR packages, if pacaur update displays 'catalyst' in output proceed with safe amd catalyst update, re-execute this upon reboot, as it remembers its state
#### automate safe catalyst update


import subprocess
import os
import sys

BASH_NEWS_SCRIPT_NAME = 'news_alert.sh'

FLAG = '.update_flag.txt'
#0 = start update
#1 = after reboot 

RESOLUTION_WIDTH = '1920'
RESOLUTION_HEIGHT = '1080'

UPDATE = "sudo pacman -Syy"
UPGRADE = "sudo pacman -Syu"

def cmd(c, pipe=None):
	if pipe:
		proc = subprocess.Popen(c.split())
		proc.wait()
	else:
		proc = subprocess.Popen(c.split(), stdout=subprocess.PIPE)
		s, e = proc.communicate()
		return (s, e)

def wflag(filename, num):
	f = open(filename, 'w')
	f.write(str(num))
	f.close()
	
def rflag(filename):
	f = open(filename)
	s = f.readlines()[0]
	f.close()	
	return s

def get_flag():
	if not os.path.exists(FLAG):
		wflag(FLAG, 0)
		return '0'
	else:
		return rflag(FLAG)
		
def last_update():
    pacman_log = '/var/log/pacman.log'
    null_path = '/dev/null'
    null = open(null_path, 'w')
    upgrade_search = 'starting full system upgrade\n'
    rev = []

    with open(pacman_log, encoding="utf-8") as f: 
        for line in f:
            try:
                print(line, file=null) #check for errors
                rev.insert(0, line) #reverse order
            except UnicodeDecodeError:
                continue
            except UnicodeEncodeError:
                continue
    found = None
    for line in rev:
        #print(line)
        if line.endswith(upgrade_search):
            found = line.split()
            
    if found:
        date = found[0][1:]
        time = found[1][:-1]
        return 'Your Last Update was on {} at {}'.format(date, time)
    else:
        return ''


if get_flag() != '0':
	#upon reboot of catalyst update
	cmd('pacaur -Syua', True)
	cmd('sudo aticonfig --initial', True)
	cmd('sudo aticonfig --initial --input=/etc/X11/xorg.conf', True)
	cmd('sudo aticonfig --resolution=0,{}x{}'.format(RESOLUTION_WIDTH, RESOLUTION_HEIGHT), True)
	cmd('sudo systemctl enable gdm.service', True)
	choice = input('reboot? [y/n]')
	if choice.lower() == 'y':
		os.remove(FLAG)
		cmd('reboot', True)
else:
	#if just now starting update
	
	cmd(BASH_NEWS_SCRIPT_NAME,True)
	try:
		print(last_update())
		var = input("update? [Y/N]")
	except KeyboardInterrupt:
		print('\nupdate aborted!')
		sys.exit()
		
	if var.lower() == "y":
		cmd(UPDATE, True)
		cmd(UPGRADE, True)
	else:
		print("update aborted!\n")	
		sys.exit()
	
	print('\nRemember to abort if catalyst update!!!')
	s, e = cmd('pacaur -Syua')
	#script needs user to abort manually if catalyst update
	if 'catalyst' in s.decode():
		#catalyst update, abort update
		print(s.decode())
		if e:
			print(e)
		cmd('sudo systemctl disable gdm.service', True)
		
		wflag(FLAG, 1)
		
		choice = input('reboot? [y/n]')
		if choice.lower() == 'y':
			cmd('reboot', True)
	else:
		#no catalyst update
		print(s.decode())
		if e:
			print(e)
		
	
