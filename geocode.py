# -*- coding: utf-8 -*-
import csv

def genGeoCodeDict():
	geocodeBuffer = {}
	with open('geocode/geocoding-spot.csv') as csvfile:
		spotGeocodeReader = csv.reader(csvfile)
		for row in spotGeocodeReader:
			geocodeBuffer[row[0]] = (float(row[1]),float(row[2]))
	with open('geocode/geocoding.csv') as csvfile:
		geocodeReader = csv.reader(csvfile)
		for row in geocodeReader:
			geocodeBuffer[row[0]] = (float(row[1]),float(row[2]))
	return geocodeBuffer


