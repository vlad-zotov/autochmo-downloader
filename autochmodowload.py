from httplib import *
from xml.dom.minidom import *
import os, sys
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
    ids = [int(i.getAttribute('id')) for i in xml.getElementsByTagName("fact")]
    for id in range(max(ids),0,-1):
        print "processing %d" % id
        try:
            h.putrequest("GET", "/"+str(id))
            h.putheader('Host', host)
            h.putheader('User-agent', 'python-httplib')
            h.endheaders()
            h.getreply()
            xml = parseString(h.getfile().read())
            elem = xml.getElementsByTagName("pictures")
            number = xml.getElementsByTagName("gosnomer")[0].childNodes[0].nodeValue

            for node in elem[0].getElementsByTagName("original")[0].getElementsByTagName("src"):
                src = "http://autochmo.ru" + str(node.childNodes[0].nodeValue)
                name = str(node.childNodes[0].nodeValue).split('/')[-1]
                new_name = "data/%05d_%s" % (id, name)
                print "\tget %s" % src
                urlretrieve(src, new_name)

        except KeyboardInterrupt:
            raise
        except:
            print "\terror"
            continue
        print "\tok"
        sys.stdout.flush()

if __name__ == '__main__':
    try: os.mkdir("data")
    except: pass
    getPictures()
