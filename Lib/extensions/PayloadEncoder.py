from Extension import Extension
import javax.swing as swing
import java.awt as awt
import java.net as net
import urllib
import base64
import re
import os
import imp
import inspect

class PayloadEncoder(Extension):
	INFO = {
			'Name'		:	'Payload Encoder',
			'Usage'		:	'This extension will help encode and parse out which payloads you will be able to use by stripping out sanitized characters.',
			'Author'	:	'James Lester, Joseph Tartaro'
	}

	def finishedLaunching(self):
		for key in ["Name", "Usage", "Author"]:
			self.printLogTab("%s: %s\n" % (key, self.INFO[key]))
		self.printLogTab("---\n\n")
		PayloadEncoderMain(self)

class PayloadEncoderMain(object):

	def __init__(self, parent):
		self.parent = parent
		
		Panel = swing.JPanel()
		Panel.layout = awt.BorderLayout()
		Panel.border = swing.BorderFactory.createTitledBorder("Payload Encoder")
		self.text = swing.JTextField( actionPerformed = self.encodePayload );
		Panel.add(self.text, Panel.layout.PAGE_START);
		
		self.textArea = swing.JTextArea()
		scrollPane = swing.JScrollPane(self.textArea)
		
		Panel.add(scrollPane, Panel.layout.CENTER)
		
		Panel1 = swing.JPanel()
		Panel1.layout = awt.BorderLayout()
		Panel1.border = swing.BorderFactory.createTitledBorder("Payload Parser")
		self.text1 = swing.JTextField( actionPerformed = self.parsePayload );
		Panel1.add(self.text1, Panel1.layout.PAGE_START);
		
		self.textArea1 = swing.JTextArea()
		scrollPane1 = swing.JScrollPane(self.textArea1)
		
		Panel1.add(scrollPane1, Panel1.layout.CENTER)

		self.splitPane = swing.JSplitPane(swing.JSplitPane.VERTICAL_SPLIT);

		self.splitPane.setDividerLocation(250)
		self.splitPane.setLeftComponent(Panel);
		self.splitPane.setRightComponent(Panel1);

		self.parent.addTabPanel("Options", self.splitPane)
#(\/)(*;;;;*)(\/) whoop! whoop! whoop! whoop!
#Should add more...
	def encodePayload(self, event):
		self.textArea.setText("")
		self.textArea.append("URL Encoded: " + self.urlencode(self.text.getText()) + "\n")
		self.textArea.append("URL Encoded(full): " + self.urlencodefull(self.text.getText()) + "\n")
		self.textArea.append("Double URL Encoded: " + self.doubleurlencode(self.text.getText()) + "\n")
		self.textArea.append("Double URL Encoded(full): " + self.doubleurlencodefull(self.text.getText()) + "\n")
		self.textArea.append("Base64: " + self.base64encode(self.text.getText()) + "\n")
		self.textArea.append("HTML: " + self.htmlencode(self.text.getText()) + "\n")
		
	def parsePayload(self, event):
		self.textArea1.setText("")
		if len(self.text1.getText()) > 0:
			var =  "[" + self.text1.getText() + "]"
			for r,d,f in os.walk("lib/payloads/"):
				for files in f:
					if files.endswith(".txt"):
						path = os.path.join(r,files)
						payloads = open(path, 'r')
						self.textArea1.append("\n\n=== " + path + " ===\n\n")
						for line in payloads:
							if not re.findall(var, line):
								self.textArea1.append(line)

	def urlencode(self, payload):
		return urllib.quote_plus(payload)

	def urlencodefull(self, payload):
		new = payload
		payload = ""
		for i in new:
			payload += "%" + str(hex(ord(i)))[2:]
		return payload
				
	def doubleurlencode(self, payload):
		payload = self.urlencode(payload)
		return re.sub('%', '%25', payload)
		
	def doubleurlencodefull(self, payload):
		payload = self.urlencodefull(payload)
		return re.sub('%', '%25', payload)

		
	def base64encode(self, payload):
		return base64.urlsafe_b64encode(payload)
		
	def htmlencode(self, payload):
		new = payload
		payload = ""
		for i in new:
			payload += "&#x" + str(hex(ord(i)))[2:] + ";"
		return payload	