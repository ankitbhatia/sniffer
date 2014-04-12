#!/bin/bash
if [ "$(whoami)" != "root" ]; then
  echo "Sorry, you are not root."
  exit 1
fi
if [ -f output-01.csv ]
then
  rm output-01.csv
fi
if [[ $(airmon-ng | grep -q mon0) ]]
then
  airmon-ng start wlan0
fi

airodump-ng mon0 -w output --output-format csv --berlin 60
