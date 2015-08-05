#Import modules
import json
import datetime
from datetime import date, timedelta
import re
import os
import shutil
from subprocess import Popen
import requests
from requests.auth import HTTPBasicAuth
import collections 
import time
import math
import translateState
import importEmail


#Class for the inquiry objects(applicants)
class Inquiry(object):
	# x is a json http response object containing the field data from wufoo
	def __init__(self,x):

	#Set any hardcoded variables
		self.StartTerm = "2015FF8"
		self.AdmitStatus = "FG"		
		self.ApplStatus = "CPR"
		self.Origin = "WEB"
		self.ProspectStatus = "GRINQ"

	#Set all non-calculated variables
		self.KTAFlag = 0
		self.INTFlag = x["Field1"]
		self.Errors = []
		self.EntryID = x["EntryId"]
		self.FirstName = x["Field4"]
		
		#This checks to see if the user did not submit a first name. This would happen if they selected
		#a KTA program and was redirected to their application. We do not want to import these individuals
		if self.FirstName == "":
			self.KTAFlag = 1

		self.LastName = x["Field5"]
		self.Email = x["Field7"]
		self.Addr1 = x["Field10"]
		self.Addr2 = x["Field11"]
		self.City = x["Field12"]

		#This converts the state text into a state code by using the translateState module
		self.State = translateState.translate(x["Field13"])
		self.Zip = x["Field14"]

	#Set any calculated Variables/non-source variables/create error messages
		self.Catalog = self.setCatalog(self.StartTerm)

		#Field37 = Program; Field25 = MAT Specialization; Field36 = MSC specialization
		self.AcadProgram, self.StudentType = self.setAcadProgram(x["Field37"],x["Field25"],x["Field26"])

		#Send over program to determine location (online/on-campus)
		self.Location = self.setLocation(x["Field37"])
		self.Gender = self.setGender(x["Field18"])
		self.Ethnicity = self.setEthnicity(x["Field16"])
		self.Race = self.setRace(x["Field17"])

		#Reorder the year and m/d characters in the birth date
		self.BirthDate = x["Field6"][5:10]+"-"+x["Field6"][0:4]

		#Strip dashes out of SSN
		self.SSN = ''.join(x["Field30"].split("-"))

		#Set up address and contact information
		if self.Addr1 == '' and self.Addr2 == '' and self.City == '' and self.State == '' and self.Zip == '':
			self.Errors.append(self.error_div("Incomplete address"))
			self.HomePhone = ''
			self.CellPhone = ''
		else:
			self.HomePhone = x["Field8"]
			self.CellPhone = x["Field9"]
		if self.Email != '':
			self.EmailType = "P"
		else:
			self.Errors.append(self.error_div("No email address was found"))
			self.EmailType = ''
		if self.HomePhone != '':
			self.PhoneType1 = "HOME"
		else:
			self.Errors.append(self.error_div("No home phone found"))
			self.PhoneType1 = ''
		if self.CellPhone != '':
			self.PhoneType2 = "CELL"
		else:
			self.Errors.append(self.error_div("No cell phone found"))
			self.PhoneType2 = ''

		#Build log string for logging
		self.logString = self.buildLogString()


	#Function to set the gender code
	def setGender(self, genderString):
		if genderString != "":
			if genderString == "Male":
				gender = "M"
			elif genderString == "Female":
				gender = "F"
		else:
			self.Errors.append(self.error_div("No gender found"))
			gender = ''
		return gender

	#Function to set the ethnicity code
	def setEthnicity(self, ethnicString):
		if ethnicString != "":
			if ethnicString == "Non-Hispanic / Latino":
				ethnic = "NHS"
			elif ethnicString == "Hispanic / Latino":
				ethnic = "HS"
			elif ethnicString == "I prefer not to answer":
				ethnic = ""
		else:
			self.Errors.append(self.error_div("No ethnicity found"))
			ethnic = ""
		return ethnic

	#Function to set the race code
	def setRace(self, raceString):
		if raceString != "":
			if raceString == "White / Caucasian":
				race = "WH"
			elif raceString == "American/Alaska Native":
				race = "AN"
			elif raceString == "Asian":
				race = "AS"
			elif raceString == "Black / African American":
				race = "BL"
			elif raceString == "Hawaiian / Pacific Islander":
				race = "HP"
			elif raceString == "I prefer not to answer":
				race = ""
		else:
			self.Errors.append(self.error_div("No race found"))
			race = ""
		return race
	
	#Function to set the acad program based on the combination of program selections they made in Wufoo
	def setAcadProgram(self, prog, MAT, MSC):
		acadProgram = ""
		studentType = ""
		if prog != "":
			if prog == "Bachelor of Science in Nursing (RN-BSN) (Online)":
				acadProgram = "NURS.RNBSN.BSN"
				studentType = "URNBS"
			elif prog == "Bachelor of Business Administration (Online)":
				acadProgram = "BAD.BBA"
				studentType = "UBBA"
			elif prog == "Bachelor of Science in Organizational Leadership (Online)":
				acadProgram = "OLDC.BS"
				studentType = "UOLDC"
			elif prog == "Master of Business Administration (Strawberry Plains Campus)":
				acadProgram = "BUSGN.MBA"
				studentType = "GMBA"
			elif prog == "Master of Business Administration (Online)":
				acadProgram = "BUSGN.MBA"
				studentType = "GMBA"
			elif prog == "Master of Science in Nursing: Family Nurse Practitioner (On Campus - Main)":
				acadProgram = "NURS.MSN"
				studentType = "GN"
			elif prog == "Master of Science in Nursing: Nurse Educator (On-Campus - Main)":
				acadProgram = "NRSED.MSN"
				studentType = "GNC"
			elif prog == "Master of Science in Nursing: Nurse Educator (Hybrid)":
				acadProgram = "NRSED.MSN"
				studentType = "GNC"
			elif prog == "Master of Science in Counseling (On-Campus - Main)":
				studentType = "GMSC"
				if MSC == "Master of Science in Clinical Mental Health Counseling":
					acadProgram = "COUN.CMHC.MSC"
				elif MSC == "Master of Science in Counseling, School Counseling Track":
					acadProgram = "COUN.SC.MSC"
				elif MSC == "Dual Degree-Master of Science in Counseling (MSC)/Educational Specialist in Counseling (EDS)":
					acadProgram = "COUN.CMPHS.EDS"
				else:
					acadProgram = "UNDCL"
			elif prog == "Master of Science in Social Entrepreneurship (Online)":
				acadProgram = "ASJ.MA"
				studentType = "GASJ"
			elif prog == "Master of Arts in Applied Theology (Main)":
				acadProgram = "APTH.MA"
				studentType = "GAPTH"
			elif prog == "Master of Arts in Teaching: C&I or ESL (On-Campus - Main)":
				studentType = "GED"
				if MAT == "MAT in C & I-Special Education Licensure (K-12)":
					acadProgram = "CI.SPED.TCHK2.MAT"
				elif MAT == "MAT in C & I Middle Grades Licensure 4-8":
					acadProgram = "CI.TCH48.MAT"
				elif MAT == "MAT in C & I - K12 Licensure":
					acadProgram = "CI.TCHK2.MAT"
				elif MAT == "MAT in C & I - Elementary Education Licensure (K-6)":
					acadProgram = "CI.TCHK6.MAT"
				elif MAT == "MAT in C & I - Secondary Licensure (7-12)":
					acadProgram = "CI.TCHSC.MAT"
				elif MAT == "MAT English as a Second Language":
					acadProgram = "ESL.MAT"
				elif MAT == "MAT English as a Second Language (K-12)":
					acadProgram = "ESL.TCHK2.MAT"
				else:
					acadProgram = "UNDCL"
			else:
				acadProgram = "UNDCL"
		else:
			acadProgram = "UNDCL"
		return (acadProgram, studentType)	

	#Function to set the location based on the program type (online/on-campus)
	def setLocation(self, prog):
		prog = prog.lower()
		if "online" in prog:
			location = "ONLN"
		elif "main" in prog:
			location = "MC"
		elif "straw" in prog:
			location = "STRAW"
		elif "hybrid" in prog:
			location = "HYB"
		return location

	#Function to set the catalog based on the start term year
	def setCatalog(self, startTerm):
		year = int(startTerm[2:4])
		catalog = str(year)+"-"+str(year+1)
		return catalog

	#Function to build the record string that will be written to a file
	def buildRecord(self):
		record = ( self.FirstName+"|"+
					self.LastName + "|" +
					self.BirthDate + "|" +
					self.Email + "|" +
					self.EmailType + "|" +
					self.HomePhone + "|" +
					self.PhoneType1 + "|" +
					self.CellPhone + "|" +
					self.PhoneType2 + "|" +
					self.Addr1 + "|" +
					self.Addr2 + "|" +
					self.City + "|" +
					self.State + "|" +
					self.Zip + "|" +
					self.Gender + "|" +
					self.Ethnicity + "|" +
					self.Race + "|" +
					self.SSN + "|" +
					self.AdmitStatus + "|" +
					self.ProspectStatus + "|" +
					self.ApplStatus + "|" +
					self.StartTerm + "|" +
					self.StudentType + "|" +
					self.AcadProgram + "|" +
					self.Catalog + "|" + 
					self.Location + "|" +
					self.Origin)
		return record

	#Function to build a logging string (not yet implemented)
	def buildLogString(self):
		logString = ((self.LastName + ", " + self.FirstName + ", " + self.BirthDate + "<br>").encode("utf8"))
		return logString

	#Function to check for possible duplication (Not yet implemented)
	def is_possible_duplicate(logString):
		log = []
		with open('logFile.txt', 'r') as f:
			for line in f:
				log.append(line)
		if (logString + "\n") in log:
			return LogString

	#Function that encapsulates a string in a div to make the text red for error messages
	def error_div(self, string):
		return '<div style = "color:red">'+string+'</div>'



#Class for the actual import process
class Import(object):
	#Initialize file object with name of wufoo form
	def __init__(self, formName):
		self.formName = formName
		self.ImportedRecords = []
		#self.PossibleDuplicates = []
		self.Errors = []

	#Function to create a timestamp for use in the filename
	#Returns a timestamp string
	def getTimeStamp(self):
		now = datetime.datetime.now()
		timestamp = str(now.month) + "-" + str(now.day) + "-" + str(now.year) + "[" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + "]"
		return timestamp

	#Function that makes the HTTP call. Accepts the name of your wufoo form
	#and a URL string. Returns a JSON response object 
	#Replace 'youraccount' with your wufoo account name
	#Replace APIKey with your API Key
	def getData(self,formName,url):
		ec = requests.get('https://ACCOUNT.wufoo.com/api/v3/forms/'+formName+url,
		auth=('API KEY', 'ACCOUNT'), verify = True)
		return ec.json()

	#Wufoo is limited in the number of entries in can return in one call.
	#This function determines the total number of entries and decides how many 
	#calls (pages) will need to be made. Accepts JSON  response object
	#Returns a number of pages integer
	def setPages(self,entries):
		entryCount = entries["EntryCount"]
		pagesBuffer = int(entryCount) / 100
		pagesBuffer = math.floor(pagesBuffer)
		pages = int(pagesBuffer) + 2
		return pages

	#Function to create a file on the users desktop with a timestamp and the form name
	#Returns a file object
	def createFile(self,timestamp,formName):
		outfile = open(os.path.expanduser("~/desktop/"+formName+"-"+timestamp + ".txt"), "w")
		return outfile


	#Function that writes the form entries to a .txt file 
	def writeEntries(self, formName, lastEntry):
		outfile = self.createFile(self.getTimeStamp(),formName)
		entryCount = self.getData(formName, "/entries/count.json")
		pages = self.setPages(entryCount)

		#These two lines are used to keep track of the last record number that has been 'imported'
		#When the program runs next, it will read this number from lastEntryFile.txt and use it as a filter in the URL string 
		#so that we only pull in new records
		recordFile = open("lastEntryFile.txt", 'w')
		finalEntry = 0

		#For every page of entries, create an entries object. For every entry in the entries object, create a new Inquiry object called 'record'
		#Then, build an entry string from the record object attributes and write it to the outfile
		for index in range(0,pages):
			entries = self.getData(formName, "/entries.json?pageStart="+str(index)+"00&pageSize=99"+"&Filter1=EntryId+Is_greater_than+"+str(lastEntry))
			for x in entries["Entries"]:
				try:
					entry = Inquiry(x)
					finalEntry = entry.EntryID
					#Checking the KTA flag to make sure we don't import KTA applicants (blank records)
					if entry.KTAFlag == 0 and entry.INTFlag == "No":
						print entry.LastName + ", " + entry.FirstName
						record = entry.buildRecord()
						outfile.write(record.encode("utf8") + "\n")
						
						#Modifying the actual instance variables instead of returning values to 
						#create an imported record list, duplicate list, and error list
						self.ImportedRecords.append(entry.logString)
						if entry.Errors != []:
							self.ImportedRecords.append("Errors:")
							self.ImportedRecords.append(entry.Errors)
						self.ImportedRecords.append("")
						#self.PossibleDuplicates.append(entry.possibleDuplicates)

				except ValueError:
					continue

		#Record the final value of 'finalEntry' as this will be the EntryID of the last record 
		#imported to be used in the next run to know where to start importing
		recordFile.write(str(finalEntry))			
		recordFile.close()			
		outfile.close()

	#Driver function with basic user output
	def run_import(self):
		lastEntry = open('lastEntryFile.txt', 'r').readline()
		print "Starting from " + lastEntry
		self.writeEntries(self.formName, lastEntry)
		importEmail.send_mail(self.ImportedRecords, self.formName)


graduate_application_import = Import("adult-graduate-studies-application")
graduate_application_import.run_import()


