from Util import xmlTraverse
import xml.etree.ElementTree as ET

sampleXML = '/home/ubuntu/Documents/hierarchy_1.xml'
tree = ET.parse(sampleXML)
root = tree.getroot()



