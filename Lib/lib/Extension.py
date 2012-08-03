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