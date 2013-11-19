#!/usr/bin/python3

import subprocess


update_aur = "pacaur -Syua"
update_off = "sudo pacman -Syy"
update_off2 = "sudo pacman -Syu"

def cmd(string):
    proc = subprocess.Popen(string.split())
    proc.wait()

cmd("sudo chmod +x news_alert.sh")
cmd("./news_alert.sh") 
var = input("update? [Y/N]")
if var.lower() == "y":
    cmd(update_off)
    cmd(update_off2)
    cmd(update_aur)
else:
    print("update aborted!\n")
