
from math import cos,sin,floor
from math import pi,sqrt

def get_line_intersection( p0_x,  p0_y,  p1_x,  p1_y, 
        p2_x,  p2_y,  p3_x,  p3_y):
    """
    
    return False if not
            ( Cx,Cy ) if intersect

    """

    s1_x = p1_x - p0_x     
    s1_y = p1_y - p0_y
    
    s2_x = p3_x - p2_x     
    s2_y = p3_y - p2_y
    
    sDiv = (-s2_x * s1_y + s1_x * s2_y)
    if sDiv == 0:
        return False
    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / sDiv
    
    tDiv = (-s2_x * s1_y + s1_x * s2_y)
    if tDiv == 0:
        return False
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / tDiv
    

    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        # Collision detected
        i_x = p0_x + (t * s1_x)
        i_y = p0_y + (t * s1_y)
        return (i_x,i_y)

    return False # No collision


class Pixel(object):
    def __init__(self,char=" ",style=1):
        self.char = char
        self.style = style

class ColorTexture():

    def __init__(self, char, colorCode):
        self.char = char
        self.colorCode = colorCode
    def getColl(self, ratio, height):
        c = []
        for i in range(height):
            p = Pixel()
            p.char = self.char
            p.style = self.colorCode
            c.append(p) 
        return c

class StrechedTexture():

    def __init__(self, texsciiFile,strech = 1.0):

        # [ [ Pixel.cchar/style ] ]
        self.texData = []

        self.strech = strech
         
        if texsciiFile.endswith(".png"):
            pass
        else:
            self.fromTexcii(texsciiFile)

    def fromTexcii(self,texsciiFile):
        """
        "
        """
        with open(texsciiFile,'r') as texFile:
            buff = [line for line in texFile]     
        try:
            colorStep=False
            for line, texcontent in enumerate(buff):
                if texcontent.startswith("#char"):
                    pass
                elif texcontent.startswith("#color"):
                    colorStep=True
                    colStart = line
                elif colorStep:
                    # colorStep
                    for chaidx , cha in enumerate(texcontent):
                        if cha in [ '1','2','3','4','5','6','7','8','9','0', ]:
                            style = int(cha)
                            self.texData[line-colStart-1][chaidx].style = style

                else:
                    # char step
                    pixLine = []
                    for cha in texcontent:
                        if cha not in [ '\n' , '\r','\t' ]:
                            p = Pixel()
                            p.char = cha
                            p.style = 3
                            pixLine.append(p)
                    self.texData.append(pixLine)
        except : 
            raise Exception("error loading texData: file read error")
        # perfom check
        if self.texHeight() == 0:
            raise Exception("error loading texture: no line")

        lineLen = self.texWidth()
        if lineLen == 0:
            raise Exception("error loading texture: no column ")
        
        for line in self.texData:
            if len(line) != lineLen:
                raise Exception("error loading texture: not regular")
                
    def texHeight(self):
        return len(self.texData)
    def texWidth(self):
        return len(self.texData[0])

    def getColl(self, ratio, height):
        
        if height == 0:
            return []

        ratioStreched = ratio*self.strech
        if ratioStreched < 1:
            colidx = int(floor(self.texWidth()*ratioStreched)) 
        else:
            newRatio = ratioStreched - int(floor(ratioStreched))
            if newRatio == 0:
                colidx = self.texWidth()-1
            else:
                colidx = int(floor(self.texWidth()*newRatio))

        #print "colIdx ",colidx
        if height > self.texHeight():
            coll = []
            vertFactor =self.texHeight()/ float(height) 
            for i in range(height):
                p = self.texData[int(i*vertFactor)][colidx]
                coll.append(p)
            return coll
        else:
            # render small collumn
            if height == 1:
                lineidx = self.texHeight() /2 
                return [ self.texData[lineidx][colidx], ]
            coll = []
            
            
            #vectFactor = float(height) / float(self.texHeight())   
            vectFactor = int(float(self.texHeight())/ float(height))
            #print "vectFactor ",vectFactor
            
            texCenter =   float(self.texHeight())/2.0
            #print "texCenter =" ,texCenter
            #
            #print "height/2  =" ,  height/ 2 
            height2 = height/2
            for i in range(height):
                lineidxFlt = ( ( i - height2 ) * vectFactor)+ texCenter
                #print i, " -> ",lineidxFlt 
                lineidx =int(lineidxFlt )
                #print i, " -> ",lineidx
                coll.append( self.texData[lineidx][colidx] )
            return coll





