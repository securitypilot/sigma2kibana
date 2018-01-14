#!/usr/bin/env python3

# sudo apt install python3-pip
# sudo -H pip3 install sigmatools gitpython


import os, shutil, glob, subprocess

SIGMA_URL = "https://github.com/Neo23x0/sigma.git"
SIGMA_ROOT = "/opt/sigma"
SIGMA_CONFIG = SIGMA_ROOT+"/tools/config/elk-windows.yml"
SIGMA_QUERIES = SIGMA_ROOT+"/queries/"


if __name__ == '__main__':
	if not os.geteuid() == 0:
		exit('[!] This script must be run as root!')
	
	# Start with clean directory
	if os.path.exists(SIGMA_ROOT):
		shutil.rmtree(SIGMA_ROOT)
	print('[+] Delete successful')

	# Clone git repo
	from git import Repo
	Repo.clone_from(SIGMA_URL, SIGMA_ROOT)
	print('[+] Clone succesful')

	if not os.path.exists(SIGMA_QUERIES):
		os.makedirs(SIGMA_QUERIES)
	
	# Crawl and return rule files
	apt = glob.glob(SIGMA_ROOT+"/rules/apt/*.yml")
	windows = glob.glob(SIGMA_ROOT+"/rules/windows/*/*.yml")
	##linux = glob.glob(SIGMA_ROOT+"/rules/linux/*.yml")
	##proxy = glob.glob(SIGMA_ROOT+"/rules/proxy/*.yml")
	##network = glob.glob(SIGMA_ROOT+"/rules/network/*.yml")
	##web = glob.glob(SIGMA_ROOT+"/rules/web/*.yml")

	# Converting to Kibana queries
	for rule in apt:
		print("[*] Converting APT rule: {}".format(rule))
		subprocess.call(['sigmac', '-c', SIGMA_CONFIG, '-t', 'kibana', rule, '-o', SIGMA_QUERIES+rule.split("/")[5]+'.kibana'], stdout=subprocess.PIPE)

	for rule in windows:
		print("[*] Converting WINDOWS rule: {}".format(rule))
		subprocess.call(['sigmac', '-c', SIGMA_CONFIG, '-t', 'kibana', rule, '-o', SIGMA_QUERIES+rule.split("/")[6]+'.kibana'], stdout=subprocess.PIPE)