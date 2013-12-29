"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, url_for, redirect, json, jsonify
from application import app
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def home():
	return redirect(url_for('match'))

def match():
	def column(matrix, i):
		return [row[i] for row in matrix]

	exampleOutput = [["Charles Babbage", "Ritchie"],
			["Tim Berners-Lee", "Thompson"],
			["Alan Turing", "Pascal"],
			["Ken Thompson", "Turing"],
			["Blaise Pascal", "Russell"],
			["Bertrand Russell", "Babbage"],
			["Dennis Ritchie", "Berners-Lee"]]
	
	if request.method == "POST":
		submittedData = request.json['data'] # get data from ajax request
		secondColumnDict = {} # this dict has the 2nd column as the key, and the 2nd column and everything after as the value, it's used for keeping the everything beyond the 2nd column intact when outputting the results
		for submittedRow in submittedData:
			'''
			# this doesn't work very well if there are duplicates in the 2nd and 3rd column
			# also requires expanding the grid dynamically
			if secondColumnDict.has_key(submittedRow[1]) and len(submittedRow) > 2: # if there are two items in the second column which are the same
				secondColumnDict[submittedRow[1]] += submittedRow[2:] # add everything after the 2nd column to the duplicate key
				print secondColumnDict[submittedRow[1]]
			'''
			# assumes the user has a unique 2nd column
			if submittedRow[1]:
				secondColumnDict[submittedRow[1]] = submittedRow[1:] # create a dict e
				
		processedData = []
		for firstColumnItem in column(submittedData, 0):
			if firstColumnItem:
				results = process.extract(firstColumnItem, column(submittedData,1), limit=1)
				item = [firstColumnItem]
				item.extend(secondColumnDict[results[0][0]])
				print item
				processedData.append(item)
			else:
				processedData.append(["",""])
		return jsonify(data=processedData)
	return render_template('match.html',exampleOutput=exampleOutput)

def warmup():
	"""App Engine warmup handler
	See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

	"""
	return ''

