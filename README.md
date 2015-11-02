# simple-sinkhole
A python script for updating lists for a simple sinkhole DNS server

I was tasked with setting up a sinkhole DNS server for my office, that can query various lists.  I figured I would make something useful and simple.  This is designed to work with dnsmasq, but can probably work with bind with some minor modification.

## Usage

```
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
```


## Installation

In order to run, the script just needs a valid config file set up, some lists to download, and write access to a database and your hosts file (or a link to it).  Following is a sample installation on a vanilla Ubuntu 14.04 Server installation (only installed base and openssh)

First, just get everything up to date:
```
sudo apt-get update && sudo apt-get dist-upgrade -y
sudo apt-get install dnsmasq git -y
sudo reboot
```

After it finishes rebooting, log in again, and:

```
sudo useradd -s /bin/false -r sinkhole
cd /opt
sudo git clone https://github.com/fang0654/simple-sinkhole.git
sudo mv simple-sinkhole.conf.sample /etc/simple-sinkhole.conf
sudo chown sinkhole /opt/simple-sinkhole
sudo mv /etc/hosts /etc/hosts.orig
sudo ln -s /opt/simple-sinkhole/hosts.new /etc/hosts
sudo crontab -l | { cat; echo "0 0 * * * sudo -u sinkhole /usr/bin/env python2 /opt/simple-sinkhole/simple-sinkhole.py \
-c /etc/simple-sinkhole.conf \
&& /etc/init.d/dnsmasq restart"; } | sudo crontab -
sudo -u sinkhole /usr/bin/env python2 /opt/simple-sinkhole/simple-sinkhole.py -c /etc/simple-sinkhole.conf
sudo dnsmasq restart
```

That should be it.  It should have done an initial download, set up the hosts file, and scheduled the crontab to run every night at midnight.


## Lists config

The lists.d conf files are meant to be pretty simple.  They are just a python dictionary, with the following possible attributes:

* source: <b>Required</b> - string, the source URL of the list
* regex: <b>Required</b> - string, A python regex that'll match the domain in the list.  If you need help, check out pythex.org
* prelines: int, number of lines to skip at the beginning
* pre: string, A line of text denoting the start of the domain entries
* post: string, A line of text denoting the end of the domain entries

You can look in the couple of conf files I built under lists.d to see how they are used.
