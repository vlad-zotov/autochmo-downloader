from httplib import *
from xml.dom.minidom import *
import os
import urllib2
from urllib import urlretrieve

def getPictures():
	host = "xml.autochmo.ru"
	h = HTTP(host)
	h.putrequest("GET", "/")
	h.putheader('Host', host)
	h.putheader('User-agent', 'python-httplib')
	h.endheaders()
	h.getreply()
	xml = parseString(h.getfile().read())
	ids = [i.getAttribute('id') for i in xml.getElementsByTagName("fact")]
	for id in ids:
		h.putrequest("GET", "/"+str(id))
		h.putheader('Host', host)
		h.putheader('User-agent', 'python-httplib')
		h.endheaders()
		h.getreply()
		xml = parseString(h.getfile().read())
		elem = xml.getElementsByTagName("pictures")
		try:
			os.mkdir(str(id))
			print "true"
		except Exception as e:
			print e
		f = open(str(id)+"\\number.txt", "w")
		number = xml.getElementsByTagName("gosnomer")[0].childNodes[0].nodeValue
		try:
			number = str(number)
			f.write(number)
		except:
			pass
		f.close()
		for node in elem[0].getElementsByTagName("original")[0].getElementsByTagName("src"):
			try:
				name = str(node.childNodes[0].nodeValue).split('/')[-1]
				urlretrieve("http://autochmo.ru"+node.childNodes[0].nodeValue, str(id) + "\\" +name)
			except:
				pass
	print "That's all"
	
if __name__ == '__main__':
	getPictures()