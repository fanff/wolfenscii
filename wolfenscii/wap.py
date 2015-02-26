
import json
import xml.etree.ElementTree as ET



def extractInfo(element):
    """

    """
    attribStr = element.find("panel_attributes").text
    attribStr = attribStr.replace("\n","")
    attribs = json.loads(attribStr)
    
    coor =  element.find("coordinates")
    attribs['x'] = int(coor.find("x").text)
    attribs['y'] = int(coor.find("y").text)
    attribs['w'] = int(coor.find("w").text)
    attribs['h'] = int(coor.find("h").text)
    #
    print "%s"%attribs

    
def readMap(mapfile):
    """
    @return a list of dicts with x,y,w,h and everything inside the json from the element string 

    """


    xmldoc = ET.parse(mapfile)
    node = xmldoc.getroot()
    for element in node.findall("element"):
         extractInfo(element)
