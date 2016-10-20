import urllib.request
import requests
from PIL import Image
import pytesseract
import copy
import os
import json
import time
import sys

#words defining the position on left - right scale
LEFT = []
RIGHT = []

def sentiment_analysis(text):
	url = 'http://text-processing.com/api/sentiment/'
	payload = {'text': text}
	r = requests.post(url, data=payload)
	n = r.json()['probability']['neg']
	p = r.json()['probability']['pos']
	m = r.json()['probability']['neutral']
	l = r.json()['label']

	return n,p,m,l

#NEED FIX
def extract_sentence(text,idx):
	# Finding leading and lagging period

	if idx > len(text) or idx < 0:
		return -1

	sent_str = ''
	sent_end = ''
	sentence = ''
	eidx = sidx = idx
	while text[eidx] != '.' and eidx < len(text)-1:
		sent_end += text[eidx]
		eidx += 1

	while text[sidx] != '.':
		sidx -= 1

	for i in range(sidx + 1, idx):
		sent_str += text[i]

	sentence += sent_str
	sentence += sent_end

	return sentence

def clean_files():
	files = ['result/left_analysis.csv','result/right_analysis.csv']
	for f in files:
		fileExist = os.path.isfile(f)
		if fileExist == True:
			os.remove(f)

def write_2_file(filename, data, running = False): 
	fileExist = os.path.isfile(filename)
	if fileExist == True and running:
		fd = open(filename,'a')
	else:
		fd = open(filename,'w')
	fd.write(data)
	fd.close()


def word_freq(line, word):
	count = 0
	found = False
	index = []

	idx = line.find(word)

	while not found:
		
		if idx > -1:
			index.append(idx)
			count += 1
			idx += len(word)
			idx = line.find(word, idx)
			if idx >= len(line):
				found = True
				return count
		else:
			return count, index

def extract_ref(pos, file, filetype):
	if filetype == 'IMAGE':
		source = pytesseract.image_to_string(Image.open(file)).lower()
	elif filetype == 'TXT':
		source = open(file,'r').read()
	for char in source:
		if not ord(char) in range(97, 123) and (not ord(char) == 32 and not ord(char) == 10):
			source = source.replace(char, "")

	source = source.splitlines()
	while '' in source: source.remove('')  
	return source

# MAIN PART OF PROGRAM

message = ['Sending request to the data server...', 'Writing data to file...', 'Cleaning temp files...', 'Extracting reference files...', 'Performing Left Analysis...', 'Performing Right Analysis...', 'Extracting sentence...', 'Performing sentiment analyis...', 'Writing data to csv']
stopwords = ['and', 'of' ,'what','who','is','a','at','is','he']

def main():

	# Getting Data from the following url:
	print(message[0])
	url = 'https://d3n8a8pro7vhmx.cloudfront.net/libdems/pages/8907/attachments/original/1429203979/Liberal_Democrat_General_Election_2015_Manifesto_-_Plain_Text.txt?1429203979'	
	ref_left = 'left.png'
	ref_right = 'right.png'

	resp = urllib.request.urlopen(url)
	url_data = resp.read()
	url_data = str(url_data)
	url_data = url_data.lower()

	print(message[2])
	clean_files()

	print(message[1])
	write_2_file('manifesto_data.txt', url_data)

	print(message[3])
	LEFT = [] + extract_ref('left', 'reference/left_ref.txt','TXT')
	RIGHT = [] + extract_ref('right', 'reference/right_ref.txt','TXT')

	for i in range(2):
		for w in stopwords:
			if w in LEFT:
				LEFT.remove(w)
			if w in RIGHT:
				RIGHT.remove(w)

	# Left Analysis
	print(message[4])
	w_idx = []
	write_2_file('result/left_analysis.csv', '------LEFT------' + '\n'+'Word, Frequency, Negative, Positive, Neutral\n', True)
	for word in LEFT:
		expression = ''
		freq, w_idx = word_freq(url_data, word)
		_n = _p = _m = 0
		_l = ''
		for t in range(freq):
			expression = extract_sentence(url_data, w_idx[t])
			n,p,m,l = sentiment_analysis(expression)
			_n += n
			_p += p
			_m += m
		if (freq > 0):
			_n = _n/freq
			_p = _p/freq
			_m = _m/freq
		response = str(_n) + ',' + str(+p) + ',' + str(_m) + '\n'
		write_2_file('result/left_analysis.csv', word+','+str(freq)+ ','+ response,  True)
		

	# Right Analysis
	print(message[5])
	w_idx = []
	write_2_file('result/right_analysis.csv', '------RIGHT------' + '\n'+'Word, Frequency, Negative, Positive, Neutral\n', True)
	for word in RIGHT:
		expression = ''
		freq, w_idx = word_freq(url_data, word)
		_n = _p = _m = 0
		_l = ''
		for t in range(freq):
			expression = extract_sentence(url_data, w_idx[t])
			n,p,m,l = sentiment_analysis(expression)
			_n += n
			_p += p
			_m += m
		if (freq > 0):
			_n = _n/freq
			_p = _p/freq
			_m = _m/freq
		response = str(_n) + ',' + str(+p) + ',' + str(_m) + '\n'
		write_2_file('result/right_analysis.csv', word+','+str(freq)+ ','+ response,  True)


main()

