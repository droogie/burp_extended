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

from burp import IBurpExtender #Burp Extension Imports
from burp import IHttpRequestResponse
from burp import IBurpExtenderCallbacks
from burp import IMenuItemHandler
import array #Python Imports
import sys
import traceback
from java.net import URL #Java Imports
sys.path.append('Lib/lib') #Custom Library Imports
sys.path.append('Lib/extensions') #Extension Imports
import BurpCommonClasses
import Extension
import FindExtensions
import GUI

#Keep in mind, we need to clean some of this up (obv)
#Generally tool == burp tool, extension == extension, it can still get confusing though.
#(\/)(*;;;;*)(\/) whoop! whoop! whoop! whoop!
		
class BurpExtender(IBurpExtender):

	def processHttpMessage(self, toolName, messageIsRequest, messageInfo):
		# This method is invoked whenever any of Burp's tools makes an HTTP request or receives a response. It allows extensions to intercept and modify the HTTP traffic of all Burp tools. 
		# For each request, the method is invoked after the request has been fully processed by the invoking tool and is about to be made on the network. 
		# For each response, the method is invoked after the response has been received from the network and before any processing is performed by the invoking tool.
		try:
			if self.mCallBacks.isInScope(messageInfo.getUrl()):
				if messageIsRequest: #is Request ,Call Request Extensions (you will need to add these with every new extension)
					for extension in self.processHTTPExtension[toolName]:
						extension.processHttpMessage(toolName, messageIsRequest, messageInfo)
		except:
			traceback.print_exc()
			raise	
	
	def registerExtenderCallbacks(self, callbacks):
		try:
			# This method is invoked on startup. It registers an instance of the IBurpExtenderCallbacks interface, providing methods that may be invoked by the implementation to perform various actions. 
			# The call to registerExtenderCallbacks need not return, and implementations may use the invoking thread for any purpose. 
			self.mCallBacks = callbacks

			toolClasses = FindExtensions.getExtensionClassList()
			self.extension_list = []
			for toolClass in toolClasses:
				self.extension_list.append(toolClass(self))
				
			self.processHTTPListeners = []

			self.processHTTPExtension = {
				'Repeater':[],
				'Proxy':[],
				'Spider':[],
				'Intruder':[],
			}
	
			self.GUI = GUI.ExtensionWindow(self)
			
			# last thing we do is let the extensions know that we have finished launching
			for extension in self.extension_list:
				extension.finishedLaunching()
				
			#Generic Code to import lineIP and Ports.  Currently HTTP(80), HTTPS(443), HTTP/HTTPS(All Other) 
			if self.args != None:
				for argument in self.args:
					list = argument.split(" ")
					currentIP = ""
					currentPort = ""
					for i in list:
						if i.strip() != None:
							if i.count(".") == 3:
								currentIP = i
							else:
								currentPort = i
								if currentPort == "80":
									uUrl = URL("http://" + currentIP + ":" + currentPort)
									self.mCallBacks.includeInScope(uUrl)
								elif currentPort == "443":
									uUrl = URL("https://" + currentIP + ":" + currentPort)
									self.mCallBacks.includeInScope(uUrl)
								else:
									uUrl = URL("http://" + currentIP + ":" + currentPort)
									self.mCallBacks.includeInScope(uUrl)
									uUrl = URL("https://" + currentIP + ":" + currentPort)
									self.mCallBacks.includeInScope(uUrl)
								currentIP = ""
								currentPort = ""
		except:
			traceback.print_exc()
			raise
			 
	def setCommandLineArgs(self, args): #self.arg[] to be used in BurpExtender.registerExtenderCallbacks()
		if len(args) >0:
			print "There are " + str(len(args)) + " arguments being passed to Burp Suite via startup"
			self.args = args
		else:
			print "There are NO arguments being passed to Burp Suite via startup"
			self.args = None

	def applicationClosing(self):
		print "Performing Fuctions on App Close"
		
	def addExtensionForTool(self, toolName, extension):
		self.processHTTPExtension[toolName].append(extension)
		for listener in self.processHTTPListeners:
			listener.extensionAdded(toolName, extension)
			
	def removeExtensionForTool(self, toolName, extension):
		index = self.processHTTPExtension[toolName].index(extension)
		self.processHTTPExtension[toolName].remove(extension)
		for listener in self.processHTTPListeners:
			listener.extensionRemoved(toolName, extension, index)
