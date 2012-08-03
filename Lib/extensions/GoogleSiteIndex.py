from Extension import Extension
from StringIO import StringIO
from burp import IBurpExtenderCallbacks
import re
from java.net import URL
import HttpRequestResponse
from burp import IMenuItemHandler

class GoogleSiteIndex(Extension):
	INFO = {
			'Name'		:	'Google Site Index',
			'Usage'		:	'This Extensions is used to add all items to scope found from a Google site:domain query.\nYou can use it via the right click menu on an item.',
			'Author'	:	'James Lester, Joseph Tartaro'
	}
	def finishedLaunching(self):
		self.getCallBacks().registerMenuItem("Extension: Google Site Index", GetItemsMapped(self))


class GetItemsMapped(IMenuItemHandler):


	def __init__(self, parent):
		self.parent = parent
		for key in ["Name", "Usage", "Author"]:
			self.parent.printLogTab("%s: %s\n" % (key, self.parent.INFO[key]))
		self.parent.printLogTab("---\n\n")
		
	def menuItemClicked(self, menuItemCaption, messageInfo):
		#self.parent.textArea.append("--- Get Items in Map ---\n")
		self.parent.printLogTab("--- Get Items in Map ---\n")
		msglen = len(messageInfo)
		for l in range(0,msglen):
			startIndex = 0
			#print messageInfo[l].getRequest().tostring()
			self.googleSiteIndex(messageInfo[l].getUrl(), self.parent.getCallBacks(), startIndex)
#GROSS.
#Need to implement a way to prompt the user with the new GUI.
#			var = 'y'
#			while var == 'y':
#				var = raw_input("Would you like to try another 100 results? (y/n): ")
#				if var == 'y':
#					startIndex =+ 100
#					self.googleSiteIndex(messageInfo[l].getUrl(), self.parent.getCallBacks(), startIndex)
		self.parent.printLogTab("-- Finished with Google Site Map Menu Click --\n")

	def googleSiteIndex(self, url, mCallBacks, startIndex):
		#print 'Starting Google Site: Index for URL: ' + str(url)
		data = 'Starting Google Site: Index for URL: ' + str(url) + '\n'
		self.parent.printLogTab(str(data))
		googleRequest = self.buildGoogleRequest(url, startIndex)
		googleResponse = mCallBacks.makeHttpRequest('www.google.com', int('80'), False, googleRequest)
		googleStringResponse = googleResponse.tostring()
		for urlInSearch in re.findall(r'''<a href="([^<]+)" class=l''', googleStringResponse):
			uUrl = URL(urlInSearch)
			port = 80
			if str(uUrl.getProtocol()) == "https":
				port = 443
			if mCallBacks.isInScope(uUrl):
				newRequest = self.buildGenericRequest(uUrl)
				newResponse = mCallBacks.makeHttpRequest(str(uUrl.getHost()), port, (str(uUrl.getProtocol()) == "https"), newRequest)
				newResponseString = newResponse.tostring()
				firstWord, statusCode, restResponse = newResponseString.split(" ", 2)
				requestResponse = HttpRequestResponse.HttpRequestResponse(None, uUrl.getHost(), port, uUrl.getProtocol(), newRequest, newResponse, int(statusCode), uUrl)
				mCallBacks.addToSiteMap(requestResponse)
				#print "Adding: " + urlInSearch
				data = "Adding: " + urlInSearch + "\n"
				self.parent.printLogTab(str(data))
			else:
				data = "\n" + urlInSearch + " was not in scope.\n\n"
				self.parent.printLogTab(str(data))

		data = "End of Google Site Indexing for URL " + str(url) + "\n"
		self.parent.printLogTab(str(data))

	def buildGoogleRequest(self, url, startIndex):
		requestString = StringIO()
		requestString.write("GET /search?q=site:" + str(url.getHost()))
		if url.getPath() is not None:
			requestString.write(str(url.getPath()))
		if url.getQuery() is not None:
			requestString.write(str(url.getQuery()))
		requestString.write("&start=" + str(startIndex) + "&num=100&complete=0&filter=0 HTTP/1.1\r\n")
		requestString.write("HOST: www.google.com\r\n")
		requestString.write("User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.28) Gecko/00000000 Firefox/30.0.00\r\n")
		requestString.write('\r\n\r\n')
		Request = map(lambda x: ord(x), requestString.getvalue())
		requestString.close()
		return Request

	def buildGenericRequest(self, url):
		requestString = StringIO()
		requestString.write("GET ")
		if url.getPath() is not None:
			requestString.write(str(url.getPath()))
		if url.getQuery() is not None:
			requestString.write(str(url.getQuery()))
		requestString.write(" HTTP/1.1\r\n")
		requestString.write("HOST: " + str(url.getHost()) + "\r\n")
		requestString.write("User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.28) Gecko/00000000 Firefox/30.0.00\r\n")
		requestString.write("Referer: wwww.google.com/\r\n")
		requestString.write('\r\n\r\n')
		Request = map(lambda x: ord(x), requestString.getvalue())
		requestString.close()
		return Request
