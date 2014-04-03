#!/usr/bin/python

import os, sys, glob, re

def getNgrams(input, n):
	ngrams = []
	
	if(len(input)>n):	
		for i in range(len(input)-n+1):
			ngrams.append(input[i:i+n])
	else:
		ngrams.append(input)
		
	return ngrams
	
def transform():
	myfile = open('chi_crime_10k.csv', 'r')
	lines = myfile.read().splitlines()
	
	newfile = open('output.csv','w')
	
	aux = list(range(0, len(lines[0].split(','))-1))
	newfile.write(",".join(str(x) for x in aux) + '\n')
	
	for l in range(1, len(lines)-1):
		result = []
		words = lines[l].split(',')
		for w in words:
			if(not (re.match(".*\\d.*", w) or w=='false' or w=='true' or w=='')):
				grams = getNgrams(w.lower(),2)
				result.append(str(grams))
			elif (w == ''):
				result.append('None')
			else:
				result.append(str(w))
				
		newfile.write(",".join(result) + '\n')
			
	