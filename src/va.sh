#!/bin/bash
ps -aux | grep va_run.py | awk '{ print $2 }' | xargs kill -9
ps -aux | grep va_view.py | awk '{ print $2 }' | xargs kill -9
nohup python3 va_run.py > ../log/run.log 2>&1 &
nohup python3 va_view.py > ../log/view.log 2>&1 &
