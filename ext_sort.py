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

parser = argparse.ArgumentParser(
	description='Sort files into folders based on file\'s extension'
)

parser.add_argument(
	'path',
	help='Root folder path to sort'
)

parser.add_argument(
	'-r',
	'--recursive-sorting',
	dest='recursive',
	action='store_true',
	help='Enables recursive sorting for all sub-directories'
)


def s0rt3r(root_path):
	if not str(root_path).endswith('/'):
		root_path += '/'
	
	for file in os.listdir(root_path):
		
		if file.startswith('.'):
			continue
		elif os.path.isfile(root_path + file):
			
			f_path = root_path + file
			name, ext = os.path.splitext(f_path)
			ext = re.sub(r"^\.", '', ext).upper()
			print(ext)
			
			dest_file = root_path + ext + '/' + file
			
			if not os.path.isdir(root_path + ext):
				os.mkdir(root_path + ext)
			try:
				os.rename(f_path, dest_file)
				print("%s --> %s" % (file, dest_file))
			except FileNotFoundError and OSError as e:
				print(e)


def r3curs0r(top_path):
	
	dlist = []
	
	for root, drz, flz in os.walk(top_path, topdown=True):
		
		for d in drz:

			dp = oj(root, d)

			dlist.append(dp)
	
	return dlist


def execution(rgz):
	
	# print(rgz)
	
	if not pid(rgz.path):
		parser.error('path must be a directory')
	
	if rgz.recursive:
		
		for l in r3curs0r(rgz.path):
			s0rt3r(l)
	
	s0rt3r(rgz.path)


execution(parser.parse_args())










