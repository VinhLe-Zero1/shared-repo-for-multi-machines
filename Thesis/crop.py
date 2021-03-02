import cv2
import xml.etree.ElementTree as ET
import re
from Util import xmlTraverse

srcPath = '/home/ubuntu/Pictures/app1.jpg'

img = cv2.imread(srcPath)

sampleXML = '/home/ubuntu/Documents/hierarchy_1.xml'
tree = ET.parse(sampleXML)
root = tree.getroot()

feature = []
for child in root:
    xmlTraverse(child, feature)

path4Crop = r'/home/ubuntu/Documents/Vinh/data/rico/images/{}.jpg'

def crop(feature, path):
    count = 0
    for feat in feature:
        bounds = list(map(int,feat['bounds']))
        temp = img[bounds[1]:bounds[3],bounds[0]:bounds[2]]

        cv2.imwrite(path.format(count), temp)

crop(feature, path4Crop)

path4Label = r'/home/ubuntu/Documents/Vinh/data/rico/labels/{}.txt'


