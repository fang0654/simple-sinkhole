# simple-sinkhole
A python script for updating lists for a simple sinkhole DNS server

I was tasked with setting up a sinkhole DNS server for my office, that can query various lists.  I figured I would make something useful and simple.  This is designed to work with dnsmasq, but can probably work with bind with some minor modification.

usage: simple-sinkhole.py [-h] [-c CONFIG] [-l LISTSFOLDER] [-i SINKHOLEIP]
                          [-f HOSTSFILE] [-d DATABASE] [-o HOSTSBASE]

Simple DNS sinkhole script, for use with dnsmasqd. Meant to be lightweight and
fast.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file
  -l LISTSFOLDER, --listsfolder LISTSFOLDER
                        List config folder
  -i SINKHOLEIP, --sinkholeip SINKHOLEIP
                        Destination IP address
  -f HOSTSFILE, --hostsfile HOSTSFILE
                        Hosts file
  -d DATABASE, --database DATABASE
                        Database file
  -o HOSTSBASE, --hostsbase HOSTSBASE
                        Base host file (will be at top of new hosts file)



# Installation

