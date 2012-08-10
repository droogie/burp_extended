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

import javax.swing
from javax.swing import event #I need this? javax.swing.event was not working for some reason. weeeee
import java.awt
import BurpExtender
import Extension

#Hi, my names droogie. feel free to ask my questions about this or make additions 
#but you shouldn't have to modify anything for extension development.... 
#
#                              ,oooooo888888888oooooo.
#                         .oo88^^^^^^            ^^^^^Y8o.
#                      .dP'                              `Yb.
#                    dP'                                   `Yb 
#                  .dP'                                     `Yb.
#                 dP'                                         `Yb
#                d8                                             8b
#               ,8P                                             `8b
#               88'                                              88
#               88                                               88
#               dP                                               88
#              d8'                                               88
#              8P                                               ,dY
#            ,dP                                                88'
#           CP   ,,.....                ,,.....                 88 
#           `b,d8P'^^^'Y8b           ,d8P'^^^'Y8b.             ,dY
#            dP'         `Yb        dP'         `Yb            88'
#           dP             Yb      dP             Yb           88 
#          dP     db        Yb    dP     db        Yb         ,dY
#          88     YP        88    88     YP        88         88'
#          Yb               dP    Yb               dP         88 
#           Yb             dP      Yb             dP         ,dY
#          dP`Yb.       ,dP'        `Yb.       ,dP'          88'
#         CCo_ `YbooooodP'            `YbooooodP'            88
#          dP"oo_    ,dP            Ybo__                    88
#         88    "ooodP'                ""88oooooP'           88
#          Yb .ood""                                        ,dY
#          ,dP"                                             88'
#        ,dP'                                               88
#       dP'    ,dP'     ,dP       ,dP'      .bmw.           88
#      d8     dP       dP        dP        o88888b          88
#      88    dP       dP       ,dP       o8888888P          88
#      Y8.   88      88       d8P       o8888888P          ,dY 
#      `8b   Yb      88       88       ,8888888P           88'
#       88    Yb     Y8.      88       888888P'            88
#       88    `8b    `8b      88       88                 ,dY 
#       88     88     88      Yb.      Yb                 88'
#       Y8.   ,Y8    ,Y8      ,88      ,8b                88
#        `"ooo"`"oooo" `"ooooo" `8boooooP                ,8Y
#            88boo__      """       """  ____oooooooo888888
#           dP  ^^""ooooooooo..oooooo"""^^^^^             88
#           88               88                           88
#           88               88                           88 
#           Yboooo__         88          ____oooooooo88888P
#             ^^^"""ooooooooo''oooooo"""^^^^^
#
#(\/)(*;;;;*)(\/) whoop! whoop! whoop! whoop!
	
class Listener(javax.swing.event.ListSelectionListener):
	def __init__(self, parent):
		self.parent = parent
	
	def valueChanged(self, e):
		status = e.valueIsAdjusting
		if status != True:
			wrapper = e.source.selectedValue
			if isinstance(wrapper, ProcessHTTPWrapper):
				self.parent.switchToProcessRequstsGUI()
			else:
				value = wrapper.tool
				self.parent.updateExtensionGUI(value)
			
class ToolWrapper(object):
	def __init__(self, tool):
		self.tool = tool
	
	def __repr__(self):
		return self.tool.getName()
		
class ProcessHTTPWrapper(object):
	def __repr__(self):
		return "Process Requests"
		
class ExtensionGUI(object):
	def __init__(self, tabPane, textArea):
		self.tabPane = tabPane
		self.textArea = textArea
		
class ActiveToolsListModel(javax.swing.AbstractListModel):

	def __init__(self, parent, toolName):
		self.parent = parent
		self.toolName = toolName
		self.parent.processHTTPListeners.append(self)

	def extensionAdded(self, toolName, extension):
		if toolName == self.toolName:
			index = self.parent.processHTTPExtension[self.toolName].index(extension)
			self.fireIntervalAdded(self, index, index)
			
	def extensionRemoved(self, toolName, extension, index):
		if toolName == self.toolName:
			self.fireIntervalRemoved(self, index, index)			
	
	def getElementAt(self, index):
		return ToolWrapper(self.parent.processHTTPExtension[self.toolName][index])
		
	def getSize(self):
		return len(self.parent.processHTTPExtension[self.toolName])
		

class ToolOutboundPanel(javax.swing.JPanel):

	def __init__(self, parent, toolName):
		javax.swing.JPanel.__init__(self, java.awt.BorderLayout())
		
		self.gui = parent
		self.toolName = toolName
		self.outboundToolsWrapped = self.getOutboundExtensionList()
	
		self.border = javax.swing.BorderFactory.createTitledBorder("HTTP Request Outbound Extensions")
				
		self.outboundExtensionList = javax.swing.JList(ActiveToolsListModel(self.gui.parent, toolName))
		self.add(self.outboundExtensionList, self.layout.CENTER)
		
		buttonPanel = javax.swing.JPanel()
		buttonPanel.layout = java.awt.FlowLayout()
		addButton = javax.swing.JButton('+', actionPerformed=self.addOutboundExtension)
		removeButton = javax.swing.JButton('-', actionPerformed=self.removeOutboundExtension)
		if len(self.outboundToolsWrapped) == 0:
			addButton.setEnabled(False)
			removeButton.setEnabled(False)
		buttonPanel.add(removeButton)
		buttonPanel.add(addButton)
		self.add(buttonPanel, self.layout.PAGE_END)
		
	def addOutboundExtension(self, parent):
		wrapper = javax.swing.JOptionPane.showInputDialog(self.gui.frame, "Please select which extension to add for this tool", "Outbound Extension Manager", javax.swing.JOptionPane.QUESTION_MESSAGE, None, self.outboundToolsWrapped, self.outboundToolsWrapped[0])	
		if wrapper != None:
			self.gui.parent.addExtensionForTool(self.toolName, wrapper.tool)
		
	def removeOutboundExtension(self, parent):
		selected = self.outboundExtensionList.selectedValue
		if selected != None:
			self.gui.parent.removeExtensionForTool(self.toolName, selected.tool)
		
	def getOutboundExtensionList(self):
		outboundList = filter(lambda x: isinstance(x, Extension.ProcessHTTPRequests), self.gui.parent.extension_list)
		outbound_extensions = [ToolWrapper(extension) for extension in outboundList]
		return outbound_extensions
		


class ExtensionWindow(object):
	def __init__(self, parent):
		
		self.parent = parent
		self.processRequestsGUI = None
		
		self.extensionGUIs = {}
		
		self.frame = javax.swing.JFrame("Burp Extension Framework")
		self.frame.setSize(800, 600)
		self.frame.setLayout(java.awt.BorderLayout())
		#self.frame.setAlwaysOnTop( True )

		self.splitPane = javax.swing.JSplitPane(javax.swing.JSplitPane.HORIZONTAL_SPLIT);
		
		tools = [ToolWrapper(tool) for tool in self.parent.extension_list]
		tools.insert(0, ProcessHTTPWrapper())
		
		self.list = javax.swing.JList(tools)
		self.list.setSelectionMode(javax.swing.DefaultListSelectionModel.SINGLE_SELECTION);
		
		self.splitPane.setLeftComponent(self.list);
		
		label = javax.swing.JLabel()
		label.setIcon(javax.swing.ImageIcon("BEFlogo_CycloneSweetie.jpeg"))
		panel1 = javax.swing.JPanel()
		panel1.add(label)
		#panel1.setBackground(java.awt.Color(255,140,0))
		self.splitPane.setRightComponent(panel1);
	
		self.frame.add(self.splitPane)
		self.frame.setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE)
		self.frame.setVisible(True)

		self.list.addListSelectionListener(Listener(self))
		

	def switchToProcessRequstsGUI(self):
		if self.processRequestsGUI == None:
			self.processRequestsGUI = self.createProcessRequestsGUI()
		self.splitPane.setRightComponent(self.processRequestsGUI);
	
	def createProcessRequestsGUI(self):	
		tabPane = javax.swing.JTabbedPane(javax.swing.JTabbedPane.TOP)

		for toolName in self.parent.processHTTPExtension.iterkeys():
			tabPane.addTab(toolName, ToolOutboundPanel(self, toolName))

		return tabPane
		
	def updateExtensionGUI(self, extension):
		tabs = self.getExtensionGUI(extension).tabPane
		self.splitPane.setRightComponent(tabs);

	def getExtensionGUI(self, extension): #grab pane from Dictionary
		if extension in self.extensionGUIs:
			return self.extensionGUIs[extension]
		else:
			tab = self.createExtensionGUI(extension)
			self.extensionGUIs[extension] = tab
			return tab

	def createExtensionGUI(self, extension):

		tabPane = javax.swing.JTabbedPane(javax.swing.JTabbedPane.TOP)

		textArea = javax.swing.JTextArea()
		scrollPane = javax.swing.JScrollPane(textArea)
		textArea.setEditable(False)
		
		tabPane.addTab("Log",scrollPane)

		return ExtensionGUI(tabPane, textArea)
		
