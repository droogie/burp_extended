################################################################################
# Copyright (C) 2011-2012 Joseph Tartaro <droogie[at]burpextensions[dot]com>
# Copyright (C) 2011-2012 James Lester <infodel[at]burpextensions[dot]com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 2 as
# published by the Free Software Foundation.  You may not use, modify or
# distribute this program under any other version of the GNU General
# Public License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
################################################################################

import urllib2
from burp import IBurpExtender
from burp import IHttpRequestResponse
from burp import IBurpExtenderCallbacks
from cStringIO import StringIO


class RequestResponse:
#This is the RequestResponse Class. This contains everyting that is unique to a request or its response.  This class will contain all functions/variables that are common in manipulating or parsing all requests/responses that meet criteria.
	def __init__(self, toolName, messageIsRequest, messageInfo, mCallBacks):
#Initialize all values that require visibilty or modification in order to modify request/response.  
		self.toolName = toolName
		self.messageInfo = messageInfo
		self.mCallBacks = mCallBacks
		self.messageIsRequest = messageIsRequest
		if self.messageIsRequest:
			self.getRequestString = messageInfo.getRequest().tostring()
			self.getResponseString = None
			self.method = self.getRequestString[:self.getRequestString.find(" ")]
			bodyIndex = self.getRequestString.find("\r\n\r\n")
			if bodyIndex != -1:
				self.body = self.getRequestString[bodyIndex +4:]
			else:
				self.body = None
		else:
			self.getResponseString = messageInfo.getResponse().tostring()
			self.getRequestString = None
			self.method = None
			self.body = None
		self.originalParameters = self.mCallBacks.getParameters(messageInfo.getRequest())
		self.originalHeaders = mCallBacks.getHeaders(messageInfo.getRequest())
		self.parsedHeaders = self.ParseHeaders(self.originalHeaders)

		
#RequestResponse GETS
	def GetHeaders(self):
		return self.originalHeaders #string
	def GetHost(self):
		return self.messageInfo.getHost() #string
	def GetMessageInfo(self):
		return self.messageInfo #Class Instance

	def GetOriginalParameters(self):
		return self.originalParameters #string
	def GetOriginalResponse(self):
		return self.originalResponse #byte[]
	def GetRequest(self):
		return self.messageInfo.getRequest() #byte[]
	def GetParsedHeaders(self):
		return self.parsedHeaders #dictionary
	def GetPort(self):
		return self.messageInfo.getPort() #int
	def GetProtocol(self):
		return self.messageInfo.getProtocol() #string
	def GetResponse(self):
		return self.messageInfo.getResponse() #byte[]
	def GetResponseString(self):
		return self.getResponseString #string
	def GetRequestString(self):
		return self.getRequestString #string
	def GetStatusCode(self):
		return self.messageInfo.getStatusCode() #short
	def GetUrl(self):
		return self.messageInfo.getUrl()
	def GetBody(self):
		return self.body
#End GETS

#RequestResponse SETS
#Need to determine what SETS are neccessary. If any.
	def SetRequestHost(self, host):
		self.host = host
	def SetParameters(self, parameters):
		self.parameters = parameters
	def SetPort(self, port):
		self.port = port
	#def SetMessage(self, message):
#End SETS	
		
		
		
	
	def BuildMessageAsString(self):
#Method, URI with Parameters, "HTTP.1/1\n
#Headers
#Body (if Post)
		messageIO = StringIO()
		messageIO.write(self.method + " ")
		messageIO.write(self.url.getPath())
		if self.url.getQuery(): #!= 'None':
			messageIO.write("?" + self.url.getQuery())
		messageIO.write(' HTTP/1.1\r\n')
		for header in self.headers:
			messageIO.write(header + ": " + self.headers[header] + '\r\n')
		messageIO.write('\r\n\r\n')
		if self.body != 'None':
			messageIO.write(self.body)
		value = messageIO.getvalue()
		messageIO.close()
		return value
#Build Headers


#Other Functions
#Create a dictionary of Headers.  Allows for modification/manipulation of Headers
	def ParseHeaders(self, originalHeaders):
		headers = {}
		for header in originalHeaders[1:]:
			headerIndex = header.find(':')
			Name = header[:headerIndex]
			Value = header[headerIndex +1:]
			headers[Name] = Value.strip()
		return headers

		
		
def GetMethodArray(Request):
	if Request[0] == 71:
		return "GET"
	elif Request[0] == 80:
		return "POST"
	else:
		return None
#This is the Get Parameters Class
class GetParameters(object):

	def __init__(self, query=None):
		self.params = {}
		if query:
			self.parseQuery(query)
	
	def parseQuery(self, query):
		for param in query.split("&"):
			index = param.find("=")
			if index == -1:
				self.addParam(param, None)
			else:
				name = param[:index]
				value = param[index+1:]
				self.addParam(name, value)

	def getQueryString(self):
		params = []
		for name, values in self.params.iteritems():
			name = urllib2.quote(name)
			for value in values:
				if value == None:
					params.append(name)
				else:
					value = urllib2.quote(value)
					params.append("%s=%s" % (name, value))
		return "&".join(params)

	def addParam(self, name, value=None):
		name = urllib2.unquote(name)
		if value != None:
			value = str(value)
			value = urllib2.unquote(value)
	
		if name in self.params:
			values = self.params[name]
		else:
			values = []
			self.params[name] = values
		
		values.append(value)
	
	def addParamValues(self, name, values):
		for value in values:
			self.addParam(name, value)
	
	def delParam(self, name):
		del self.params[name]
	
	def delParamValue(self, name, value):
		self.params[name].remove(value)
	
	def getValues(self, name):
		return self.params[name]
	
	def getFirstValue(self, name, defValue=None):
		return self.params[name][0]
	
	def getNames(self):
		return self.params.keys()
	
	def setValue(self, name, value):
		self.delParam(name)
		self.addParam(name, value)
	
	def __getitem__(self, name):
		return self.getFirstValue(name)
	
	def __setitem__(self, name, value):
		return self.setValue(name, value)
	
	def __repr__(self):
		return repr(self.params)
	

	
class BuildRequest:
	def __init__(self, method):
		print 'test'
	def buildRequest(self):
		messageIO = StringIO()
		messageIO.write(self.method + " ")
		messageIO.write(self.url.getPath())
		if self.url.getQuery(): #!= 'None':
			messageIO.write("?" + self.url.getQuery())
		messageIO.write(' HTTP/1.1\r\n')
		for header in self.headers:
			messageIO.write(header + ": " + self.headers[header] + '\r\n')
		messageIO.write('\r\n\r\n')
		if self.body != 'None':
			messageIO.write(self.body)
		value = messageIO.getvalue()
		messageIO.close()
		return value