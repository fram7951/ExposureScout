#!/bin/bash
# Title: Users Information - Users
# Authors: Nathan Amorison
# Last Update: 24-09-2024
# Description: Get all users (name, uid and groups id they are in) as $uid$($name$):$gid$(,$gid$)*

grep '^sudo:.*$' /etc/group | cut -d: -f4 | sed "s/,/\n/" | while read i; do id $i; done 2>/dev/null | sed "s/uid=\([0-9]*\)(.*$/\1/"
#grep '^sudo:.*$' /etc/group | cut -d: -f4 | sed "s/,/\n/" | while read i; do sudo -l -U $i | tail -1; done 2>/dev/null #Needs sudo rights to be executed... not a good thing... But gives info on perms of the given sudoer