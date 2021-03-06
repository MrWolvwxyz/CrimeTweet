#!/usr/bin/python

import os, sys, glob, re, csv

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
	lines = csv.reader(myfile, delimiter=',')
	
	newfile = open('output.csv','w')
	
	aux = next(lines)
	
	i = 0
	for h in aux:
		header[h] = i
		i = i + 1
	
	newfile.write(",".join(str(x) for x in aux) + '\n')
	
	att = header[attribute]
	
	arrest = header['Arrest']
	domestic = header['Domestic']
	beat = header['Beat']
	district = header['District']
	ward = header['Ward']
	area = header['Community Area']
	fbi = header['FBI Code']
	lat = header['Latitude']
	long = header['Longitude']
	xcoor = header['X Coordinate']
	ycoor = header['Y Coordinate']

	index = []
	index.append(att)
	
	index.append(arrest)
	index.append(domestic)
	index.append(beat)
	index.append(district)
	index.append(ward)
	index.append(area)
	index.append(fbi)
	index.append(lat)
	index.append(long)
	index.append(xcoor)
	index.append(ycoor)
	
	for l in lines:
		words = l
		for w in range(0,len(words)):
			if(w not in index):
				sub = re.sub('[\;\,\?\!\(\)\"]',' ', words[w])
				s = sub.split(' ')
				for a in s:
					if(a in dict):
						dict[a] = dict[a] + 1
					else:
						dict[a] = 1
			
						
	myfile.seek(0)
	trash = next(lines)
	
	for l in lines:
		result = []
		words = l
		for w in range(0,len(words)):
			total = 0
			if(w not in index):
				if (words[w] == ''):
					result.append('None')
				else:
					sub = re.sub('[\;\,\?\!\(\)\"]',' ', words[w])
					s = sub.split(' ')
					for a in s:
						total = total + dict[a]
						
					result.append(str(total))
					
			elif(w == arrest or w == domestic):
				if(str(words[w]) == 'false'):
					result.append(str(0))
				else:
					result.append(str(1))
			else:
				if (words[w] == ''):
					result.append('None')
				else:
					result.append(str(words[w]))
				
		newfile.write(",".join(result) + '\n')
			
	