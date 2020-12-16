#!/bin/bash

# Supposed to run on rsync-host01, change rsync-host02 to rsync-host01 to make a script that is meant to run on rsync-host02.

rsync --exclude=.git --exclude=.idea -avz -e "ssh -o StrictHostKeyChecking=no" -chavzP --rsync-path="sudo rsync" ./ ec2:/shopwareapi

while true; do
  inotifywait -r -e modify,attrib,close_write,move,create,delete ./
  rsync --exclude=.git --exclude=.idea -avz -e "ssh -o StrictHostKeyChecking=no" -chavzP --rsync-path="sudo rsync" ./ ec2:/shopwareapi
done
