from struct import *
from java.net import URL
from burp import IHttpRequestResponse


class HttpRequestResponse(IHttpRequestResponse):

	def __init__(self, comment, host, port, protocol, request, response, statusCode, url):
		self._comment = comment
		self._host = host
		self._port = port
		self._protocol = protocol
		self._request = request
		self._response = response
		self._statusCode = statusCode
		self._url = url
		

	def getComment(self):
		return str(self._comment)
	def getHost(self):
		return str(self._host)
	def getPort(self):
		return int(self._port)
	def getProtocol(self):
		return str(self._protocol)
	def getRequest(self):
		return self._request
	def getResponse(self):
		return self._response
	def getStatusCode(self):
		return self._statusCode
	def getUrl(self):
		return self._url

	def setComment(self, comment):
		self._comment = comment
	def setHost(self, host):
		self._host = host
	def setPort(self, port):
		self._port = port
	def setProtocol(self, protocol):
		self._protocol = protocol
	def setRequest(self, request):
		self._request = request
	def setResponse(self, response):
		self._response = response
	def setStatusCode(self, statusCode):
		self._statusCode = statusCode
	def setUrl(self, url):
		self._url = url

