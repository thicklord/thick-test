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
import taglib
from collections import OrderedDict as od
from operator import itemgetter as ig
import argparse
import eyed3


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


def build_up(some_src, order_type):
	album_set = set()
	
	# tracks_data = {}
	
	tracks_data = []
	
	for root, drz, flz in os.walk(some_src, topdown=True):
		
		for f in flz:
			
			if f.startswith('.'):
				continue
			
			fp = oj(root, f)
			
			track = taglib.File(fp)
			
			tags = track.tags
			
			# print(tags)
			
			album_set.add(tags['ALBUM'][0])
			
			album_date = str(tags['DATE'][0])
			
			# takes date and splits it to just the year
			if len(album_date) > 4:
				save_year = album_date.split('-')[0]
				del tags['DATE']
				track.save()
				
				tags['DATE'] = [save_year]
				track.save()
			
			track_yr = tags['DATE'][0]
			track_num = tags['TRACKNUMBER'][0]
			track_alb = tags['ALBUM'][0]
			track_tot = int(tags['TRACKTOTAL'][0])
			
			track_num = int(str(track_num).split("/")[0])
			
			# by_year.append([tags['DATE'][0], fp])
			
			# tracks_data[fp] = [track_yr, track_alb, track_num, track_tot]
			
			trck = [fp, track_yr, track_alb, track_num, track_tot]
			
			tracks_data.append(trck)
	
	"""
	>>> from operator import itemgetter
	>>> L=[[0, 1, 'f'], [4, 2, 't'], [9, 4, 'afsd']]
	>>> sorted(L, key=itemgetter(2))

	[[9, 4, 'afsd'], [0, 1, 'f'], [4, 2, 't']]
	"""
	
	order_type = str(order_type).lower()
	
	if order_type.startswith('a'):
		srtt = sorted(tracks_data, key=ig(1))
		
		return srtt
	
	elif order_type.startswith('d'):
		srtt = sorted(tracks_data, key=ig(1), reverse=True)
		
		return srtt


def worker(src_lst, src_dir, rgz):
	
	pl_len = len(src_lst)
	
	for counter, track in enumerate(src_lst):
		
		# trck = [fp, track_yr, track_alb, track_num, track_tot]
		
		tr = track[0]
		
		if piff(tr):
			t = taglib.File(tr)
			tg = t.tags
			
			new_track_num = "%d/%d" % (counter + 1, pl_len)
			
			tg['TRACKNUMBER'] = [new_track_num]
			tg['TRACKTOTAL'] = [str(pl_len)]
			
			try:
				t.save()
			
			except AttributeError as AE:
				eprint("couldn't save %s" % k)
				eprint(str(AE))
				continue
			
			bn = os.path.basename(tr)
			
			base_dir = os.path.dirname(tr)
			
			if re.match(r"^\d+", bn):
				
				nu = re.sub(r"^\d+", str(counter + 1), bn)
				
				if rgz.rename:
					new_file = oj(base_dir, nu)
					
					shutil.move(tr, new_file)
				
				elif not rgz.rename:
					print(Fore.RED + bn + Style.RESET_ALL, Fore.BLUE + nu + Style.RESET_ALL, sep=" -> ")
	
	if rgz.move:
		for root, drz, flz in os.walk(src_dir, topdown=True):
			for f in flz:
				
				if f.startswith('.'):
					continue
				
				fp = oj(root, f)
				
				shutil.move(fp, src_dir)
				
				print("moved: %s -> %s" % (f, src_dir))
	
	if rgz.clear and rgz.move:
		for root, drz, flz in os.walk(src_dir, topdown=True):
			
			for d in drz:
				dpath = oj(root, d)
				
				send2trash(dpath)
				
				print("deleted folder: %s" % d)
	

def rrgprsr():
	parser = argparse.ArgumentParser(
		description="Script to build a chronological playlist based on a given folder. Will only work if the given audio files have the proper release date within its tags",
		epilog="pychrono '/path/to/playlist/folder'"
	)

	# required

	parser.add_argument(
		oj("path"),
		# required=True,
		# type=path,  # metavar='P',
		help='Path to folder that contains music files',
	)

	parser.add_argument(
		'-o', '--order-type',
		# required=True,
		# type=str,  # metavar='O',
		default='a',
		help="Organize playlist in either ascending or descending order by year.\nAscending by default",
	)

	# optional

	parser.add_argument(
		'-r',
		'--rename-files',
		# required=False,
		# type=bool,
		dest='rename',
		action='store_true',
		default=True,
		help="Renames files with new track number prepending the file name",
	)

	parser.add_argument(
		'-m',
		'--move-files',
		# required=False,
		# type=bool,
		dest='move',
		action='store_true',
		default=True,
		help="Moves files to root of passed directory",
	)

	parser.add_argument(
		'-C',
		'--clear-folders',
		dest='clear',
		action='store_true',
		default=True,
		help="Clears empty folders after files are moved. "
		     "Will not work unless '-m' is passed as well"
	)
	
	parser.add_argument(
		'-e',
		'--export-playlist-file',
		dest='export',
		action='store_true',
		help="Save playlist as an M3U file"
	)

	# parser.add_argument(
	# 	'-n', '--normalize', required=False,
	# 	type=bool, dest='nrm',
	# 	help="Normalizes all files for approximate balanced playback"
	# )

	return parser.parse_args()


audio_exts = [
	"aac",
	"aif",
	"aifc",
	"aiff",
	"ape",
	"flac",
	"m4a",
	"m4p",
	"mp3",
	"mp4",
	"wav",
	"wma"
]


def m3u_generator(src_dir):
	src_name = os.path.basename(src_dir)
	
	playlist_name = "%s.m3u" % src_name
	
	pl_path = oj(src_dir, playlist_name)
	
	file_meta_list = []
	
	for root, dirz, files in os.walk(src_dir, topdown=True):
		
		for f in files:
			if f.startswith('.'):
				continue
			
			head, tail = os.path.splitext(f)
			
			print(head, tail, sep=": ")
			
			if str(tail)[1:] not in audio_exts:
				print("skipping %s" % f)
				continue
			
			f_path = oj(root, f)
			
			track_tags = taglib.File(f_path).tags
			
			meta_info = {
				'filename': f_path,
				'length': int(eyed3.load(f_path).info.time_secs),
				'track_num': track_tags['TRACKNUMBER'][0].split('/')[0],
				'track_name': track_tags['TITLE'][0]
			}
			
			file_meta_list.append(meta_info)
	
	if len(file_meta_list) > 0:
		
		with open(pl_path, "w") as pl_write:
			pl_write.write("#EXTM3U\n")
			
			for tr in sorted(file_meta_list, key=lambda tr: int(tr['track_num'])):
				pl_write.write("#EXTINF:%s,%s\n" % (tr['length'], tr['track_name']))
				pl_write.write("file://%s\n" % tr['filename'])
		pl_write.close()
	
	else:
		print("no files found")
	
	"""
		for mp3 in sorted(mp3s, key=lambda mp3: int(mp3['tracknumber'])):
			of.write("#EXTINF:%s,%s\n" % (mp3['length'], mp3['filename']))
			of.write(mp3['filename'] + "\n")
	"""
	
	pass


argz = rrgprsr()

path_val = argz.path

ot = argz.order_type

if not path_val or not pid(path_val):
	parser.error("Please enter a valid directory path")

if str(ot).startswith('a') or str(ot).startswith('d'):
	ddd = build_up(path_val, str(ot))
	
	worker(ddd, path_val, argz)

else:
	eprint("order type \"%s\" currently not supported" % ot)

if argz.export:
	m3u_generator(path_val)




