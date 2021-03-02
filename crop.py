import cv2
import xml.etree.ElementTree as ET
import re

srcPath = '/home/ubuntu/Pictures/app1.jpg'

img = cv2.imread(srcPath)


def showImg(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


GUIClass = {'Button':0,
'CheckBox':1,
'Chronometer':2,
'EditText':3,
'ImageButton':4,
'ImageView':5,
'ProgressBar':6,
'RadioButton':7,
'RatingBar':8,
'SeekBar':9,
'Spinner':10,
'Switch':11,
'ToggleButton':12,
'VideoView':13,
'TextView':14}

def traverse(node, feature):
    nodeClass = node.attrib['class'].split('.')[2]
    if nodeClass in GUIClass:
        feature.append({
            'class': nodeClass,
            'bounds': re.findall('\d+',node.attrib['bounds'])})
    for child in node:
        traverse(child, feature)


sampleXML = '/home/ubuntu/Documents/hierarchy_1.xml'
tree = ET.parse(sampleXML)
root = tree.getroot()

feature = []
for child in root:
    traverse(child, feature)

count = 0
for feat in feature:
    bounds = list(map(int,feat['bounds']))
    temp = img[bounds[1]:bounds[3],bounds[0]:bounds[2]]
    featClass = feat['class']

    cv2.imwrite(r'/home/ubuntu/Documents/Vinh/data/rico/images/{}.jpg'.format(count), temp)

    xcenter = ((bounds[2] - bounds[0] + 1) / 2)/1200
    ycenter = ((bounds[3] - bounds[1] + 1) / 2)/1824
    width = (bounds[2] - bounds[0] + 1) / 1200
    height = (bounds[3] - bounds[1] + 1)/1824
    labelFile = r'/home/ubuntu/Documents/Vinh/data/rico/labels/{}.txt'.format(count)
    with open(labelFile, 'w') as f:
        f.write('{} {} {} {} {}'.format(GUIClass[featClass], xcenter, ycenter, width, height))
    f.close()
    count = count + 1

