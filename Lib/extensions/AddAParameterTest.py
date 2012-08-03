import Extension
from StringIO import StringIO
from burp import IBurpExtenderCallbacks
from java.net import URL
import HttpRequestResponse
from burp import IMenuItemHandler
import BurpCommonClasses

class AddParameterTest(Extension.ProcessHTTPRequests):
	INFO = {
			'Name'		:	'Add Parameter Tests',
			'Usage'		:	'This Extensions is used to add various parameters such as, admin, debug, etc',
			'Author'	:	'James Lester, Joseph Tartaro'
	}

	def finishedLaunching(self):
		for key in ["Name", "Usage", "Author"]:
			self.printLogTab("%s: %s\n" % (key, self.INFO[key]))
		self.printLogTab("---\n\n")

	def processHttpMessage(self, toolName, messageIsRequest, messageInfo):
		print self.addAParameterTest(messageInfo)
		
	def addAParameterTest(self, messageInfo):
		#list of added params here... would like to have it so the user can enter them into the GUI.... weeeeee
		newParameters = ["test=1", "debug=1", "debug=true"]
		requestString = messageInfo.getRequest().tostring()
		for parameter in newParameters:
			if parameter not in requestString:
				startMethod = BurpCommonClasses.GetMethodArray(messageInfo.getRequest())
				if messageInfo.getUrl().getQuery() != None:
					query = messageInfo.getUrl().getQuery()
					for parameter in newParameters:
						count = query.count(parameter)
						if count == 0:
							requestString = requestString.replace(" HTTP/", "&" + str(parameter) + " HTTP/", 1)
				if startMethod == "POST":
					bodyIndex = requestString.find("\r\n\r\n")
					if bodyIndex != -1:
						body = requestString[bodyIndex +4:]
					else:
						body = None
					if body != None:
						for parameter in newParameters:
							if body.count(parameter) == 0:
								contentLengthIndex = requestString.index("Content-Length: ")
								contentLengthEnd = requestString.index("\n", contentLengthIndex)
								contentLength = int(requestString[contentLengthIndex+16:+contentLengthEnd])
								requestString = requestString.replace(str("Content-Length: "  + str(contentLength)), str("Content-Length: "	 + str(contentLength + len(parameter) + 1)), 1)
								body = body[:body.find("\r\n\r\n")] + "&" + str(parameter) + "\r\n\r\n"
								requestString = requestString[:bodyIndex] + "\r\n\r\n" + body
		return requestString