#!/bin/bash
PYTHON="/home/horazmic/code/weightloss-tracker/env/bin/python3"
SCRIPT="/home/horazmic/code/weightloss-tracker/main.py"
LOG="/home/horazmic/code/weightloss-tracker/cron.log"

$PYTHON $SCRIPT scrape  2>&1 | tee -a $LOG
$PYTHON $SCRIPT  2>&1 | tee -a $LOG
