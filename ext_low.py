import os
import re
import requests
import pandas as pd
import time
import shutil
from send2trash import send2trash
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from colorama import Fore, Back, Style
from os.path import join as oj
from os import getcwd as og
from os import listdir as ld
from os.path import isdir as pid
from os.path import isfile as piff
from os.path import abspath as pabs
import urllib.request
from os import path
from os import makedirs
from walkdir import filtered_walk as wdfw
from walkdir import all_paths as wdap
from walkdir import limit_depth as wdld
import argparse


def gprint(st):
	print(Fore.BLUE + st + Style.RESET_ALL)


def tprint(st):
	print("TEST PRINT: ", end="")
	print(Fore.GREEN + st + Style.RESET_ALL)


def eprint(st):
	print(Fore.RED + Back.WHITE + st + Style.RESET_ALL)


def dir_mkr(specified_path):
	if not path.isdir(specified_path):
		makedirs(specified_path)



def rgz():
	parser = argparse.ArgumentParser(
		description="Recursively converts all file's extensions in a given path to lower case"
	)
	
	parser.add_argument(
		oj('path'),
		help='Path to directory containing files'
	)
	
	parser.add_argument(
		'-d', '--dry-run',
		action="store_true",
		dest='dry',
		default=False,
		help="No files renamed, only a printed simulation"
	)
	
	parser.add_argument(
		'-u',
		dest='upper',
		action='store_true',
		default=False,
		help='Toggles upper case extension conversion'
	)
	
	return parser.parse_args()


dsh = "\n------------------------------------------------\n"


def walker(mydir, argz):
	
	counter = 0
	
	for root, dirs, files in os.walk(mydir):
		
		for f in files:
			
			if f.startswith("."):
				continue
			
			f_path = oj(root, f)
			
			file_name, extension = os.path.splitext(f)
			
			if not extension:
				continue
			
			if argz.upper:
				
				if extension == extension.upper() and not argz.dry:
					continue
				
				new_name = "%s%s" % (file_name, extension.upper())
				
			else:
				
				if extension == extension.lower() and not argz.dry:
					continue
				
				new_name = "%s%s" % (file_name, extension.lower())
			
			new_path = oj(root, new_name)
			
			if argz.dry:
				
				print(Fore.BLUE + f + Fore.WHITE + " >dry_run< " + Fore.RED + new_name + Style.RESET_ALL)
				
			else:
				try:
					shutil.move(f_path, new_path)
	
					print(Fore.BLUE + f + Fore.WHITE + " > " + Fore.RED + new_name + Style.RESET_ALL)
					
					counter += 1
					
	
				except Exception as e:
					print("couldn't rename file")
					print(Fore.RED + Back.BLACK + "EXCPTN: %s" % str(e) + Style.RESET_ALL)
	
	if not argz.dry:
		print("%s%sRenamed %d files%s" % (dsh, str('\t' * 2), counter, dsh))
	

parsed_args = rgz()


if not parsed_args.path or not pid(parsed_args.path):
	print("bad path !\nquitting")
	quit()

else:
	walker(parsed_args.path, parsed_args)





















