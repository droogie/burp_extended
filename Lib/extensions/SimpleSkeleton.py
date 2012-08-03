from burp import IMenuItemHandler
from Extension import Extension
import javax.swing as swing
import java.awt as awt
import java.net as net


class SimpleSkeleton(Extension):
	INFO = {
			'Name'		:	'Simple Skeleton',
			'Usage'		:	'This is a Simple Example Skeleton',
			'Author'	:	'James Lester, Joseph Tartaro'
	}
	def finishedLaunching(self):
		self.getCallBacks().registerMenuItem("Extension: ___Simple Example Menu Item___", MenuHandler(self))
		


class MenuHandler(IMenuItemHandler):

	def __init__(self, parent):
		self.parent = parent
		for key in ["Name", "Usage", "Author"]:
			self.parent.printLogTab("%s: %s\n" % (key, self.parent.INFO[key]))

	def menuItemClicked(self, menuItemCaption, messageInfo):
		self.parent.printLogTab("You clicked the simple example button!\n")
		msglen = len(messageInfo)
		for l in range(0,msglen):
			#print all selected items in "scope" area
			self.parent.printLogTab(str(messageInfo[l].getUrl()) + "\n")
			#(\/)(*;;;;*)(\/) whoop! whoop! whoop! whoop!

