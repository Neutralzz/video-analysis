#!/bin/bash
ps -aux | grep run.py | awk '{ print $2 }' | xargs kill -9
ps -aux | grep view.py | awk '{ print $2 }' | xargs kill -9
nohup python3 run.py > ../log/run.log 2>&1 &
nohup python3 view.py > ../log/view.log 2>&1 &
