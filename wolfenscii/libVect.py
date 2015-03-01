
from math import cos,sin,floor
from math import pi,sqrt


class Vect(object):
    x = float(1)
    y = float(0)

    def __init__(self,x=1,y=0):
        self.x = float(x)
        self.y = float(y)
    def __str__(self):
        return '(%s,%s)'%(self.x,self.y)
    
    def mul_ip(self,scal):
        self.x = self.x * scal
        self.y = self.y * scal
    
    def mul(self,scal):
        return Vect(self.x * scal,self.y * scal)

    def add(self,vect):
        return Vect(self.x + vect.x,self.y + vect.y)

    def add_ip(self,vect):
        self.x = self.x + vect.x
        self.y = self.y + vect.y

    def rotate(self,angleRAD):
        #A = array([[cos(angleRAD), -sin(angleRAD)], # rotation matrix
        #        [sin(angleRAD), cos(angleRAD)]])
        x = cos(angleRAD)*self.x -sin(angleRAD)*self.y
        y = sin(angleRAD)*self.x +  cos(angleRAD)* self.y
        return Vect(x,y)

    def rotate_ip(self,angleRAD):
        x = cos(angleRAD)*self.x -sin(angleRAD)*self.y
        y = sin(angleRAD)*self.x +  cos(angleRAD)* self.y

        self.x = x
        self.y = y
    
    def norm(self):
        return sqrt(self.x*self.x + self.y*self.y)
    def normsq(self):
        return self.x*self.x + self.y*self.y



def vectIntersection( v0,v1  ,v2,v3):
    res = get_line_intersection(
            v0.x,v0.y,
            v1.x,v1.y,
            v2.x,v2.y,
            v3.x,v3.y)

    if res:
        return Vect(res[0],res[1])
    else:
        return False

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


class Pixel():
    char = " "
    style = 1

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

    def __init__(self, texsciiFile,strech = 1):
        self.texData = []

        self.strech = strech
         
        
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
                lineidx =int(round(lineidxFlt ))
                #print i, " -> ",lineidx
                coll.append( self.texData[lineidx][colidx] )
            return coll






class WallVect(object):
    a = Vect()
    b = Vect()
    
    texture = ColorTexture('W',3)
    def __init__(self,a,b, texture):
        self.a = a
        self.b = b
        self.texture = texture
        self.__normsq = self.b.add(self.a.mul(-1.0)).normsq()
        self.__norm = sqrt(self.__normsq)
    
    def __str__(self):
        return "WVect %s %s "%(self.a,self.b)
    def collide(self, otherWallVect):
        return vectIntersection(self.a,self.b,otherWallVect.a,otherWallVect.b)
    def collisionRatio(self, collisionPoint ):

        dist = collisionPoint.add(self.a.mul(-1.0)).norm()

        return dist / self.__norm
        
class WallSet(object):

    wallList = []
    def __str__(self):
        return "wallSet[%s]"%len(self.wallList)
    def collide(self,wallVect ) :
        
        self.collisionList= []

        for wall in self.wallList:
            #print wall,self.collisionList
            if type(wall) in [WallSet,RectWall] :
                for res in wall.collide(wallVect):
                    #print "appending",res
                    self.collisionList.append(res)
            else:
                collisionVector =  wall.collide(wallVect)
                if collisionVector :
                    self.collisionList.append((collisionVector,wall))
                else:
                    pass
        return self.collisionList

    def nest(self,wallSet):
        self.wallList.append(wallSet)

class RectWall(WallSet):
    def __init__(self,init,extend,texturew,textureh):

        a = init
        b = init.add( Vect(0,extend.y) ) 
        c = init.add( Vect(extend.x,extend.y) ) 
        d = init.add( Vect(extend.x,0) ) 
        self.wallList = [
               WallVect(a,b,texturew), 
               WallVect(b,c,textureh), 
               WallVect(c,d,texturew), 
               WallVect(d,a,textureh), 
        ]

        
