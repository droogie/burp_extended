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

