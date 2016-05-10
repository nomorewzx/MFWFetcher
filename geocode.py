# -*- coding: utf-8 -*-
import csv

GEOCODE = {}

def genGeoCodeDict():
	with open('geocode/geocoding-spot.csv') as csvfile:
		spotGeocodeReader = csv.reader(csvfile)
		for row in spotGeocodeReader:
			GEOCODE[row[0]] = (row[1],row[2])
	with open('geocode/geocoding.csv') as csvfile:
		geocodeReader = csv.reader(csvfile)
		for row in geocodeReader:
			GEOCODE[row[0]] = (row[1],row[2])

def convertGeoCode():
	pass

if __name__ == '__main__':
	main()