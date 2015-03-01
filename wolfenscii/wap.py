
import json
import xml.etree.ElementTree as ET


from wolfenscii.libVect import Vect,WallVect,RectWall,WallSet,ColorTexture, Pixel,StrechedTexture

def extractInfo(element):
    """

    """
    attribStr = element.find("panel_attributes").text
    attribStr = attribStr.replace("\n","")
    attribStr = attribStr.split("JSONSTART")[1]
    print attribStr
    attribs = json.loads(attribStr)
    
    coor =  element.find("coordinates")
    attribs['x'] = int(coor.find("x").text)
    attribs['y'] = int(coor.find("y").text)
    attribs['w'] = int(coor.find("w").text)
    attribs['h'] = int(coor.find("h").text)
    #
    return attribs

def buildRootNode(allElements):
    """
    @return scene root node builded from allElements. A scaling operation is performed in
    order to get a player size of (1,1) 
    """
    rootNode=WallSet()

    scale = 0
    for element in allElements:
        if element["type"] == "playerStart":
            scale = element["w"]
            playerx = 1+ (element["x"]/scale)
            playery = 1+ (element["y"]/scale)
            playerRotation = element["rotate"]


    for element in allElements:
        if element["type"] == "RectWall":
            x = element["x"]/scale
            y = element["y"]/scale
            w = element["w"]/scale
            h = element["h"]/scale

            texfile = element["texture"]["tex"]
            wstrech = element["texture"]["wstrech"]
            hstrech = element["texture"]["hstrech"]

            print "adding rectwall %s,%s   ,%s,%s" % (x,y,w,h,)
            texturew = StrechedTexture(texfile,wstrech) 
            textureh = StrechedTexture(texfile,hstrech) 
            rootNode.nest(RectWall(Vect(x,y),Vect(w,h),texturew,textureh))
    return rootNode,Vect(playerx,playery),playerRotation

def readMap(mapfile):
    """
    @return a list of dicts with x,y,w,h and everything inside the json from the element string 

    """
    xmldoc = ET.parse(mapfile)
    node = xmldoc.getroot()
    return [ extractInfo(element)  for element in node.findall("element") ]
         
