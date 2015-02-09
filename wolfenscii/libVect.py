
from math import cos,sin
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


class WallTexture():

    def __init__(self, char, colorCode):
        self.char = char
        self.colorCode = colorCode



class WallVect(object):
    a = Vect()
    b = Vect()
    
    texture = WallTexture('W',3)
    def __init__(self,a,b, texture):
        self.a = a
        self.b = b
        self.texture = texture
    
    def __str__(self):
        return "WVect %s %s "%(self.a,self.b)
    def collide(self, otherWallVect):
        return vectIntersection(self.a,self.b,otherWallVect.a,otherWallVect.b)

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
    def __init__(self,init,extend,texture):

        a = init
        b = init.add( Vect(0,extend.y) ) 
        c = init.add( Vect(extend.x,extend.y) ) 
        d = init.add( Vect(extend.x,0) ) 
        self.wallList = [
               WallVect(a,b,texture), 
               WallVect(b,c,texture), 
               WallVect(c,d,texture), 
               WallVect(d,a,texture), 
        ]

