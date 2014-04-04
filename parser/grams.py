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
	
def transform(attribute):
	header = {}
	dict = {}

	myfile = open('chi_crime_10k.csv', 'r')
	lines = myfile.read().splitlines()
	
	newfile = open('output.csv','w')
	
	aux = lines[0].split(',')
	
	aux = aux[:-1]
	
	i = 0
	for h in aux:
		header[h] = i
		i = i + 1
	
	newfile.write(",".join(str(x) for x in aux) + '\n')
	
	index = header[attribute]
	
	for l in range(1, len(lines)):
		words = lines[l].split(',')
		for w in range(0,len(words)-2):
			if(w != index):
				sub = re.sub('[\;\,\?\!\(\)\"]',' ', words[w])
				s = sub.split(' ')
				for a in s:
					if(a in dict):
						dict[a] = dict[a] + 1
					else:
						dict[a] = 1
						
	for l in range(1, len(lines)):
		result = []
		words = lines[l].split(',')
		for w in range(0,len(words)-2):
			total = 0
			if(w != index):
				if (words[w] == ''):
					result.append('None')
				else:
					sub = re.sub('[\;\,\?\!\(\)\"]',' ', words[w])
					s = sub.split(' ')
					for a in s:
						total = total + dict[a]
						
					result.append(str(total))
			else:
				result.append(str(words[w]))
				
		newfile.write(",".join(result) + '\n')
			
	