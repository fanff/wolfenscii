
import json
import xml.etree.ElementTree as ET


from wolfenscii.libVect import Vect,WallVect,RectWall,WallSet,ColorTexture, Pixel,StrechedTexture

def extractInfo(element):
    """

    """
    attribStr = element.find("panel_attributes").text
    attribStr = attribStr.replace("\n","")
    attribStr = attribStr.split("JSONSTART")[1]
    #print attribStr
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

            #print "adding rectwall %s,%s   ,%s,%s" % (x,y,w,h,)
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
         



def __randDicWall(x,y,w,h,texturew,textureh,tex):
    """
    """
    rwall = RectWall(Vect(x,y),Vect(w,h),
            texturew,textureh).asDic()

    rwall["texture"] = {u'hstrech': textureh,
                     u'tex': tex,
                     u'wstrech': texturew} 
                
    return rwall

def randomMap(count,size=50):
    """


    """
    # player init 
    playerStart = {u'rotate': 0.0, 'h': 1, 'w': 1, 'y': 459, 'x': 549, u'type': u'playerStart'}
    res = [playerStart,]
    
    tex= u'wolfenscii/asset/tex/Red3'

    
    # border
    rwall = __randDicWall(0,0.,size,1,
            1,1,tex)
    res.append(rwall)
    
    rwall = __randDicWall(0,0.,1,size,
            1,1,tex)
    res.append(rwall)
    
    rwall = __randDicWall(size,0,1,size,
            1,1,tex)
    res.append(rwall)
    
    rwall = __randDicWall(0,size,size+1,1,
            1,1,tex)
    res.append(rwall)
    
    #rwall = __randDicWall(0,0,2,20,1,1,tex)
    #res.append(rwall)

    for i in range(count):
        #random x y
        import random

        x = random.random()*size
        y = random.random()*size
        h = random.random()*size/4.0 + 3
        w = random.random()*size/4.0 + 3


        # random texture
        texturew = 1
        textureh = 1
        
        tex= u'wolfenscii/asset/tex/Red3'
        

        rwall = __randDicWall(x,y,w,h,texturew,texturew,tex)
        
        res.append(rwall)


    return res 
