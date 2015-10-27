#!/usr/bin/env python2

import ConfigParser
import argparse
import pdb
import tempfile
import os
import urllib
import re
import sqlite3


def configure_parser():
	parser = argparse.ArgumentParser(description='''Simple DNS sinkhole script, for use with dnsmasqd.  Meant to be lightweight and fast.''')
	parser.add_argument('-c', '--config', help='Config file')
	parser.add_argument('-l', '--listsfolder', help='List config folder')
	parser.add_argument('-i', '--sinkholeip', help='Destination IP address')
	parser.add_argument('-f', '--hostsfile', help='Hosts file')
	parser.add_argument('-d', '--database', help="Database file")
	parser.add_argument('-o', '--hostsbase', help="Base host file (will be at top of new hosts file)")

	return parser


def create_database(file_db):
	conn = sqlite3.connect(file_db)

	try:
		conn.execute('''CREATE TABLE list_data (domain text, url text)''')
	except:
		pass

	return conn





if __name__ == "__main__":

	parser = configure_parser()

	args = parser.parse_args()


	if not args.config:
		print("Error: You must at least specify a config file.")
		parser.print_help()
		exit(1)

	config = ConfigParser.ConfigParser()
	
	try:
		config.read(args.config)
	except:
		print("Config file invalid.  Please specify a valid config file")
		parser.print_help()
		exit(1)

	if not config.sections():
		print("Config file invalid.  Please specify a valid config file")
		parser.print_help()
		exit(1)		

	config_options = {}
	

	

	for o in vars(args).keys():
		if o != 'config':

			if vars(args).get(o, None):
				config_options[o] = vars(args).get(o, None)
			elif o in config.options('MainConfig'):
				config_options[o] = config.get('MainConfig', o)
			else:
				print("Missing option %s.  Please specify a valid config file or specify on command line" % o)
				parser.print_help()
				exit(1)				

	
	conn = create_database('domains.db')
	cur = conn.cursor()


	for f in os.listdir(config_options['listsfolder']):
		if f.endswith(".conf"):
			cur.execute('delete from list_data where domain = ?', (f,))
			listfile = open(os.path.join(config_options['listsfolder'], f), 'r')
			list_options = eval(listfile.read())
			

			if not list_options.get('source', False):
				print("Missing source in %f.  Skipping")
				pass

			starting_line = list_options.get('prelines', 0)
			if list_options.get('pre', False):
				started = False
				pre = list_options.get('pre')
			else:
				started = True
				pre = None

			post = list_options.get('post', False)
			regex = list_options.get('regex', False)

			
			u = urllib.urlopen(list_options['source'])

			for i, line in enumerate(u):
				if i < starting_line:
					pass
				elif started == False:
					if line.rstrip() == pre:
						started = True
				elif post and post == line.rstrip():
					break
				else:
					# pdb.set_trace()
					m = re.search(regex, line.rstrip())
					try:
						cur.execute("insert into list_data (domain, url) values (?, ?)", (f, m.group(1)))
					except:
						print("Error inserting line %s: %s" % (i, line))

			conn.commit()



	cur.execute('select distinct url from list_data')
	urls = cur.fetchall()

	hosts = open(config_options['hostsfile'], 'w')
	hosts_b = open(config_options['hostsbase'], 'r')

	hosts_base = hosts_b.read()
	hosts_b.close()

	hosts.write(hosts_base)


	for u in urls:
		hosts.write('%s\t%s\n' % (config_options['sinkholeip'], u[0]))

	hosts.close()

