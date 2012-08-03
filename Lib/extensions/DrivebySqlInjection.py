from burp import IBurpExtenderCallbacks
from burp import IBurpExtender
from burp import IHttpRequestResponse
from Extension import Extension
from BurpCommonClasses import RequestResponse
import BurpCommonClasses
from java.net import URL
from cStringIO import StringIO
import HttpRequestResponse
from burp import IMenuItemHandler
import datetime


class DrivebySQLi(Extension):
	INFO = {
			'Name'		:	'Drive-by SQL Injection Test',
			'Usage'		:	'This Extensions is used to iterate GET/POST methods placing a SQLi payload with a unique incrimenting identification string (6006730++) at each parameter.\nIf the static string is identified in the database, the unique string can be used to identify which request is responsible for the injection.\nThis allows you to test SQLi using non standard (but intrusive) payloads ensuring proper defense.\nNote: The current payload is stored in "Lib/extensions/payloads.txt" and the log will be stored in "Lib/extensions/output/"',
			'Author'	:	'James Lester, Joseph Tartaro'
	}	
	def finishedLaunching(self):
		self.getCallBacks().registerMenuItem("Extension: Drive-by SQLi Test", DrivebySQLiTest(self))

#we should place the request type function into a lib so people can easily use them for their own extensions, other then adding the like 80 lines... 

#too lazy to clean up code currently........ just don't read it :D

#Looking for SQL injection payloads???? Why Not DR. ZOIDBERG?!?!
#(\/)(*;;;;*)(\/) whoop! whoop! whoop! whoop!

class DrivebySQLiTest(IMenuItemHandler):
	
	def __init__(self, parent):
		self.parent = parent
		for key in ["Name", "Usage", "Author"]:
			self.parent.printLogTab("%s: %s\n" % (key, self.parent.INFO[key]))
		self.parent.printLogTab("---\n\n")
	
	def menuItemClicked(self, menuItemCaption, messageInfo):
		self.DrivebySQLiCount = 600673 #unique number to search database for.
		#print "--- Performing Drive-by SQLi Test ---"
		self.parent.printLogTab("--- Performing Drive-by SQLi Test ---\n")
		#print self.parent.DrivebySQLiCount
		#print self.DrivebySQLiCount
		self.parent.printLogTab("Your static number is " + str(self.DrivebySQLiCount) + "0\nIt will increment for every request.\n")
		msglen = len(messageInfo)
		for l in range(0,msglen):
			#print messageInfo[l].getRequest().tostring()
			#self.parent.DrivebySQLiCount = DrivebySqlInjection.DrivebySqlInjection(messageInfo[l], self.parent.DrivebySQLiCount, self.parent.mCallBacks, self.parent.textArea2)
			if messageInfo[l].getRequest() != None:
				self.DrivebySQLiCount = self.drivebySqlInjection(messageInfo[l], self.DrivebySQLiCount, self.parent.getCallBacks())
			else:
				self.parent.printLogTab("There were not parameters or requests populated to itterate.\nPlease validate that both a request has previously been made and that it contains parameters.\n")
		#print "-- Finished with Drive-by SQLi Test --\n"
		self.parent.printLogTab("-- Finished with Drive-by SQLi Test --\n")

	def drivebySqlInjection(self, messageInfo, currentCount, mCallBacks):
		outputFile = "driveby_" + datetime.datetime.now().strftime("%m-%d-%Y") + ".txt"
		requestMethod = BurpCommonClasses.GetMethodArray(messageInfo.getRequest())
		if (requestMethod != "GET") or (requestMethod != "POST"):
			payloadStrings = []
			for line in open('Lib/extensions/drivebysql-payloads.txt', 'r'):
				currentCount = self.makeInjection(messageInfo, currentCount, mCallBacks, line, outputFile)
		return currentCount		
			
	def makeInjection(self, messageInfo, currentCount, mCallBacks, payload, outputFile):
		output = open(outputFile, "ab")
		originalRequestString = messageInfo.getRequest().tostring()
		requestMethod = BurpCommonClasses.GetMethodArray(messageInfo.getRequest())

		if requestMethod == "GET":
			baseRequestString = StringIO()
			baseRequestString.write('GET ')
		elif requestMethod == "POST":
			baseRequestString = StringIO()
			baseRequestString.write('POST ')
		else:
			return baseRequestString.write(messageInfo.getUrl().getPath())

		if messageInfo.getUrl().getQuery() == None:
			newRequestString = StringIO()
			newRequestString.write(baseRequestString.getvalue())
			if (messageInfo.getUrl().getPath()[-1:] != "/") and not messageInfo.getUrl().getPath().count(".",-4):
				newRequestString.write('/')
			## stip() typo???? replaced with strip() for the time being.......
			#newRequestString.write(payload.stip() + str(currentCount) + " HTTP/1.1\r\n")
			newRequestString.write(payload.strip() + str(currentCount) + " HTTP/1.1\r\n")
			###
			newRequestString.write(originalRequestString[originalRequestString.index("\n")+1:])
			currentCount = currentCount + 1
			newResponse = mCallBacks.makeHttpRequest(messageInfo.getHost(), messageInfo.getPort(), messageInfo.getProtocol()=='https', newRequestString.getvalue())
			output.write(newRequestString.getvalue())
			self.parent.printLogTab(newRequestString.getvalue())
			newRequestString.close()
			baseRequestString.write(" HTTP/1.1\r\n")
		else:
			baseRequestString.write("?")
			query = messageInfo.getUrl().getQuery()
			count = query.count("=")
			oldEqualsIndex = 0
			oldAmpIndex = 0
			for c in range(count):
				equalsIndex = query.index("=", oldEqualsIndex)
				if query.count("&", equalsIndex):
					ampIndex = query.index("&", equalsIndex)
				else:
					ampIndex = len(query)
				#f.write(query[oldAmpIndex:equalsIndex] + "\n")
				#f.write(query[equalsIndex+1:ampIndex] + "\n")
				newRequestString = StringIO()
				newRequestString.write(baseRequestString.getvalue())
				currentCount = currentCount + 1
				newRequestString.write(query[:ampIndex])
				newRequestString.write(payload.strip() + str(currentCount) + query[ampIndex:] + " HTTP/1.1\r\n")
				newRequestString.write(originalRequestString[originalRequestString.index("\n")+1:])
				newResponse = mCallBacks.makeHttpRequest(messageInfo.getHost(), messageInfo.getPort(), messageInfo.getProtocol()=='https', newRequestString.getvalue())
				output.write(newRequestString.getvalue())
				self.parent.printLogTab(newRequestString.getvalue())
				newRequestString.close()
				newRequestString = StringIO()
				newRequestString.write(baseRequestString.getvalue())
				currentCount = currentCount + 1
				newRequestString.write(query[:equalsIndex])
				newRequestString.write(payload.strip() + str(currentCount) + query[equalsIndex:] + " HTTP/1.1\r\n")
				newRequestString.write(originalRequestString[originalRequestString.index("\n")+1:])
				newResponse = mCallBacks.makeHttpRequest(messageInfo.getHost(), messageInfo.getPort(), messageInfo.getProtocol()=='https', newRequestString.getvalue())
				output.write(newRequestString.getvalue())
				self.parent.printLogTab(newRequestString.getvalue())
				newRequestString.close()
				oldEqualsIndex = equalsIndex + 1
				oldAmpIndex = ampIndex +1
			baseRequestString.write(messageInfo.getUrl().getQuery() + " HTTP/1.1\r\n")

		if requestMethod == "POST":
			bodyIndex = originalRequestString.find("\r\n\r\n")
			if bodyIndex != -1:
				contentLengthIndex = originalRequestString.index("Content-Length: ")
				contentLengthEnd = originalRequestString.index("\n", contentLengthIndex)
				contentLength = int(originalRequestString[contentLengthIndex+16:+contentLengthEnd])
				contentLength = contentLength + len(payload.strip()) + len(str(currentCount))
				baseRequestString.write(originalRequestString[originalRequestString.index("\n")+1:contentLengthIndex+16] + str(contentLength) + originalRequestString[contentLengthIndex+16+contentLengthEnd:bodyIndex] + "\r\n\r\n")
				originalBody = originalRequestString[bodyIndex +4:]
				count = originalBody.count("=")
				oldEqualsIndex = 0
				oldAmpIndex = 0
				for c in range(count):
					equalsIndex = originalBody.index("=", oldEqualsIndex)
					if originalBody.count("&", equalsIndex):
						ampIndex = originalBody.index("&", equalsIndex)
					else:
						ampIndex = len(originalBody[:originalBody.find("\r")])
					newRequestString = StringIO()
					newRequestString.write(baseRequestString.getvalue())
					currentCount = currentCount + 1
					newRequestString.write(originalBody[:ampIndex])
					newRequestString.write(payload.strip() + str(currentCount) + originalBody[ampIndex:] + "\r\n\r\n")
					newResponse = mCallBacks.makeHttpRequest(messageInfo.getHost(), messageInfo.getPort(), messageInfo.getProtocol()=='https', newRequestString.getvalue())
					output.write(newRequestString.getvalue())
					self.parent.printLogTab(newRequestString.getvalue())
					newRequestString.close()
					newRequestString = StringIO()
					newRequestString.write(baseRequestString.getvalue())
					currentCount = currentCount + 1
					newRequestString.write(originalBody[:equalsIndex])
					newRequestString.write(payload.strip() + str(currentCount) + originalBody[equalsIndex:] + "\r\n\r\n")
					newResponse = mCallBacks.makeHttpRequest(messageInfo.getHost(), messageInfo.getPort(), messageInfo.getProtocol()=='https', newRequestString.getvalue())
					output.write(newRequestString.getvalue())
					self.parent.printLogTab(newRequestString.getvalue())
					newRequestString.close()
					oldEqualsIndex = equalsIndex + 1
					oldAmpIndex = ampIndex +1
			else:
				baseRequestString.write(originalRequestString[originalRequestString.index("\n")+1:] + "\r\n\r\n")
		baseRequestString.close()
		output.close()

		return currentCount