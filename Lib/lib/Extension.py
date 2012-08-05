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

class Extension(object):

	def __init__(self, parent):
		self.parent = parent
#Alert when GUI is done launching	
	def finishedLaunching(self):
		pass

#Retrieve name of tool (class name)	
	def getName(self):
		return self.__class__.__name__
	
	def getGUI(self):
		return self.parent.GUI
	
	def getExtensionGUI(self):
		return self.getGUI().getExtensionGUI(self)
#Add a custom tab to the GUI from extension
	def addTabPanel(self, name, panel):
		self.getExtensionGUI().tabPane.addTab(name, panel)
#Append data to the text area in the log tab	
	def printLogTab(self, data):
		self.getExtensionGUI().textArea.append(data)
		
	def getCallBacks(self):
		return self.parent.mCallBacks
		
class ProcessHTTPRequests(Extension):

	def processHttpMessage(self, toolName, messageIsRequest, messageInfo):
		pass