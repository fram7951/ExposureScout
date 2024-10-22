#!/bin/bash
# Title: Users Information - Groups
# Authors: Nathan Amorison
# Last Update: 24-09-2024
# Description: Get all groups (name, gid) as $name$:$gid$

cat /etc/group | sed "s/:[0-9A-Za-z]*:/#/1" | sed "s/:.*//g" | sed "s/#/:/"

# output example: user:1000