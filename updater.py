#!/usr/bin/python3

import subprocess
import sys

update_aur = "pacaur -Syua"
update_off = "sudo pacman -Syy"
update_off2 = "sudo pacman -Syu"

def cmd(string):
    proc = subprocess.Popen(string.split())
    proc.wait()

cmd("./news_alert.sh") #assuming news_alert.sh is in /usr/bin
try:
    var = input("update? [Y/N]")
except KeyboardInterrupt:
    print('\nupdate aborted!')
    sys.exit()
if var.lower() == "y":
    cmd(update_off)
    cmd(update_off2)
    cmd(update_aur)
else:
    print("update aborted!\n")
