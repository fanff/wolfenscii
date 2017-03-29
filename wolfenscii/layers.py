import logging
from math import sqrt,sin,cos,atan2,pi
from libVect import Pixel

from wolfenscii import astar
import random 

    
class SubMenuMain():
    
    def __init__(self,lines):
        self.log = logging.getLogger("submain")
        self.selected = 0

        self.lines = lines
    def select(self,lid):
        self.selected = lid

    def selectDown(self):
        self.selected = (self.selected+1) % len(self.lines)
    def selectUp(self):
        self.selected = (self.selected-1) % len(self.lines)

    def linesit(self):
        return ((lid,self.selected==lid,line)for lid,line in enumerate(self.lines))

    def getBoxed(self):

        maxsize = max([len(line) for line in self.lines])
        pre = "*  "
        sus = "  *"
        full = maxsize + len(pre)+len(sus)
        
        res = [[]]
        for i in range(full):
            res[0].append(Pixel(char="#",style=3))
            
        for lid,selected,line in self.linesit():
            newline = []
            for char in pre:
                newline.append(Pixel(char,3))

            for _ in range(full -len(pre)-len(sus)-len(line)):
                newline.append(Pixel("*",1))

            for char in line:
                if selected:
                    newline.append(Pixel(char,4))
                else:
                    newline.append(Pixel(char,5))
            for char in sus:
                newline.append(Pixel(char,3))

            self.log.debug("new line len : %s",len(newline))
            res.append(newline)
        n = []
        for i in range(full):
            n.append(Pixel(char="#",style=3))
        res.append(n)

        return res,len(res),full

class MenuLayout():
    """

    """
    def __init__(self):
        self.log = logging.getLogger("menulayout")

        self.menuX = 200
        self.menuY = 2
        
        self.currentSub = SubMenuMain(["enter","quit","options"])


    def update(self,canvas):
        try:
            box,boxMR,boxMC = self.currentSub.getBoxed()
            self.log.debug("boxMR %s, boxMC %s"%(boxMR,boxMC))
            for i, ir in enumerate(canvas):
                for j,p in enumerate(ir):
                    if i<boxMR:
                        if j<boxMC:
                            #self.log.debug("box pix : %s %s",box[i][j].char,box[i][j].style)
                            #p.char = "#"#box[i][j].char
                            #p.style = 3#box[i][j].style
                            canvas[i][j] = box[i][j]
        except Exception as e:
            self.log.exception("error updating menulayout")
        
    def getMain(self,):
        pass

    def getServerList(self,):
        pass

    def actionMapper(self,):
        pass


class MatrixSceneLayer():


    def __init__(self,debug,worldMap):
        self.log =  logging.getLogger(__name__+".MSL")
        
        self.debug = debug
        
        self.texmapping = {}
        self.worldMap = worldMap

        self.magicFactor = 0.65
        
        # normal to player direction
        self.dirX = -1.0
        self.dirY = 0.0
        
        self.planeX= 0.0
        self.planeY= 0.66
        
        # player pos
        self.posX = 5.1
        self.posY = 6.1
        
        
        # moveSpeed ,rotSpeed
        self.moveSpeed = 0.05
        self.rotSpeed = 0.03

        self.autoPlayerMove = False
        self.apmDestX,self.apmDestY = None,None
        self.apmRoute = []

        
        
    def raycast(self, rayCount ):

        collideList = []
        for colToRender in range(rayCount):
            # for each columns to Render
            self.log.debug("--------------------col %s ",colToRender)
            
            #//x-coordinate in camera space
            cameraX = 2.0 * float(colToRender) / float(rayCount) - 1.0 
            
            self.log.debug("cameraX   : %.1f ",cameraX)
            
            rayPosX = self.posX
            rayPosY = self.posY
            
            rayDirX = self.dirX + (self.planeX * cameraX)
            rayDirY = self.dirY + (self.planeY * cameraX)
            
            # map box
            mapX = int(self.posX)
            mapY = int(self.posY)
            
            self.log.debug("rayX,rayY : %+.1f , %+.1f ",rayPosX,rayPosY)
            self.log.debug("raydir    : %+.1f , %+.1f ",rayDirX,rayDirY)
            
            # len of ray
            sideDistX=0
            sideDistY=0
            
            try:
                #  //length of ray from one x or y-side to next x or y-side
                deltaDistX = sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
                deltaDistY = sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
                 
                # //what direction to step in x or y-direction (either +1 or -1)
                stepX=0
                stepY=0

                hit = 0 #//was there a wall hit?
                #side #//was a NS or a EW wall hit?
                if (rayDirX < 0):
                    stepX = -1
                    sideDistX = (rayPosX - mapX) * deltaDistX
                else:
                    stepX = 1
                    sideDistX = (mapX + 1.0 - rayPosX) * deltaDistX
                if (rayDirY < 0):
                    stepY = -1
                    sideDistY = (rayPosY - mapY) * deltaDistY
                else:
                    stepY = 1
                    sideDistY = (mapY + 1.0 - rayPosY) * deltaDistY

                self.log.debug("sideX,sideY: %+.1f , %+.1f ",
                        sideDistX,sideDistY)

                #//perform DDA
                while (hit == 0):
                    #//jump to next map square, OR in x-direction, OR in y-direction
                    if (sideDistX < sideDistY):
                        sideDistX += deltaDistX
                        mapX += stepX
                        side = 0
                    else:
                        sideDistY += deltaDistY
                        mapY += stepY
                        side = 1
                    #//Check if ray has hit a wall
                    if (self.worldMap[mapX][mapY] > 0):
                        hit = 1


                #//Calculate distance projected on camera direction 
                #(oblique distance will give fisheye effect!)
                if (side == 0):
                    perpWallDist = abs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX);
                else:
                    perpWallDist = abs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY);
                
                """

                //calculate value of wallX
                double wallX; //where exactly the wall was hit
                if (side == 0) wallX = rayPosY + perpWallDist * rayDirY;
                else           wallX = rayPosX + perpWallDist * rayDirX;
                wallX -= floor((wallX));

                //x coordinate on the texture
                int texX = int(wallX * double(texWidth));
                if(side == 0 && rayDirX > 0) texX = texWidth - texX - 1;
                if(side == 1 && rayDirY < 0) texX = texWidth - texX - 1;


                """
                #//calculate value of wallX
                #double wallX; //where exactly the wall was hit
                if (side == 0):
                    
                    wallX = rayPosY + perpWallDist * rayDirY;
                else:           
                    wallX = rayPosX + perpWallDist * rayDirX;

                wallX -= int((wallX));

                #//x coordinate on the texture
                texWidth = 64.0
                texX = wallX * texWidth;
                if(side == 0 and rayDirX > 0) : texX = texWidth - texX - 1
                if(side == 1 and rayDirY < 0) : texX = texWidth - texX - 1;
                texX = texX/texWidth
                
                mapvalue = self.worldMap[mapX][mapY]
                self.log.debug("mapvalue : %s ",mapvalue)

                if mapvalue in self.texmapping:
                    texture = self.texmapping[mapvalue]

                    collideList.append((perpWallDist,texX,texture ))
                else:
                    collideList.append((perpWallDist,texX,mapvalue ))

            except Exception as e:
                self.log.exception("wow")
        #endFOR

        return collideList

    def update(self,canvas):
        """
        will modify canvas
        Suppose canvas is clean

        0. automove

        1. automove

        2. raycast

        3. render map
        """

        self.debug.setText("Player Pos      ",
                "%.1f ,%.1f     "%(self.posX,self.posY))
        self.debug.setText("Player Dir      ",
                "%.1f ,%.1f     "%(self.dirX,self.dirY))
        self.debug.setText("Player Rot      ",
                "%.1f      "%atan2(self.dirY,self.dirX))


        if self.autoPlayerMove:
            """

            """
            self.debug.setText("AutoMode      ","Active    ")
            self.debug.setText("AutoMode Dest       ",
                    "%s %s        "%(self.apmDestX,self.apmDestY))
            if (int(self.posX)==self.apmDestX) and (int(self.posY)==self.apmDestY):
                #player arrived
                # resert AutoMove
                self.setAutoMove(True)

            else:
                # player not arrived
                # calculate next action
                px = int(self.posX)
                py = int(self.posY)
                nextX,nextY = self.apmRoute[0]
                self.debug.setText("AutoMode Next","%s %s"%(nextX,nextY))
                if px==nextX and py==nextY:
                    # switch point
                    self.apmRoute = self.apmRoute[1:]

                else:
                    # player should move
                    
                    #  MOVETOFUNC = { 
                    #          -3 : self.playerTurnLeft,
                    #          -2 : self.playerTurnRight,
                    #          -1 : self.playerBack,
                    #          1 : self.playerFront,
                    #          2:self.playerTurnLeft,
                    #          3:self.playerTurnRight,
                    #          }

                    #  moves = [
                    #      [-1,3],
                    #      [-1,2],
                    #      [-1],
                    #      [1],
                    #      [2],
                    #      [3],
                    #      [2,1],
                    #      [3,1],
                    #      [1,2],
                    #      [1,3],
                    #      ]
                    #  
                    #  scores =[]
                    #  for moveList in moves:
                    #      for act in moveList:
                    #          MOVETOFUNC[act]()
                    #      c1x = (2*self.posX+self.dirX)/2.0
                    #      c1y = (2*self.posY+self.dirY)/2.0

                    #      score = (c1x-nextX+0.5)**2 + (c1y-nextY+0.5)**2

                    #      scores.append(score)
                    #      for act in reversed(moveList):
                    #          MOVETOFUNC[-act]()

                    #  # min score
                    #  scoreMin = min(scores)
                    #  scoreMinidx = [i for i, j in enumerate(scores) if j == scoreMin][0]

                    #  for act in moves[scoreMinidx]:
                    #      MOVETOFUNC[act]()



                    # calculate direction
                    dirx =  nextX+0.5 - self.posX 
                    diry =  nextY+0.5 - self.posY

                    norm = sqrt(dirx**2 + diry**2)

                    dirx = dirx/norm
                    diry = diry/norm

                    # calculate rotation
                    dirAngle =  atan2(diry,dirx)

                    if abs(dirAngle)<pi/2:
                        playerAngle = atan2(self.dirY,self.dirX)
                                    
                        angleDiff = playerAngle-dirAngle
                        
                        #self.debug.setText("AutoMode Next Dir      ",
                        #        "%.1f      "%dirAngle)
                        #

                        #self.debug.setText("AutoMode angle diff      ",
                        #        "%.1f      "%angleDiff)

                        if abs(angleDiff)<=0.3:
                            self.playerFront()
                        else:
                            if angleDiff > 0:
                                self.playerTurnRight()
                            else:
                                self.playerTurnLeft()

                    else :
                        dirAngle =  atan2(dirx,diry)
                        playerAngle = atan2(self.dirX,self.dirY)
                                    
                        angleDiff = playerAngle-dirAngle
                        
                        #self.debug.setText("AutoMode Next Dir      ",
                        #        "%.1f      "%dirAngle)
                        #

                        #self.debug.setText("AutoMode angle diff      ",
                        #        "%.1f      "%angleDiff)

                        if abs(angleDiff)<=0.3:
                            self.playerFront()
                        else:
                            if angleDiff > 0:
                                self.playerTurnLeft()
                            else:
                                self.playerTurnRight()


        else:
            self.debug.setText("AutoMode      ","Not Active    ")
        # End auto move


        # raycast  
        colHeight = len(canvas)
        colsCount = len(canvas[0])
        
        colisionsResult = self.raycast(colsCount)
        texturedColumns = []
        for distance,texX,objetc in colisionsResult:
            # calculate wallHeight
            wallHeight = int (colHeight/(distance * self.magicFactor))
            self.log.debug("WallHeightH :%s, texX : %s"%(wallHeight,texX))

            # calculate texture collumn
            colu = objetc.getColl(texX,wallHeight)
            
            if wallHeight<= colHeight:
                missing = colHeight-wallHeight
                missingUP = missing/2
                missingDown = missing-missingUP
                
                textureCol = [Pixel() for _ in range(missingUP)]
                textureCol+= colu
                textureCol+= [Pixel() for _ in range(missingDown)]
            else:
                missing = wallHeight - colHeight
                missingUP = missing/2
                
                #missingDown = missing-missingUP
                
                #fact = wallHeight/float(colHeight)

                #lencolu = "%s %s %s %.3f"%(len(colu),colHeight,missing,fact)
                #textureCol = [_ for _ in lencolu]
                #
                #while len(textureCol) < wallHeight:
                #    textureCol+=["."]
                #

                textureCol = [colu[missingUP+_] for _ in range(colHeight)]

            texturedColumns.append(textureCol)

        
        # render
        # apply textures on canvas
        for colid ,textureCol in enumerate(texturedColumns):
            for i,canvasline in enumerate(canvas):

                pix = canvasline[colid]
                pix.char = textureCol[i].char
                pix.style= textureCol[i].style  # TODO : fix here

        #render mini map
        px = int(self.posX)
        py = int(self.posY)
        mapsize = 10
        for i in range(mapsize):
            for j in range(mapsize):
                qi = px+i-mapsize/2
                qj = py+j-mapsize/2
                
                incanvai = i
                incanvaj = j

                canvas[incanvai][incanvaj].style=3
                if i == mapsize/2 and j == mapsize/2:
                    if abs(self.dirX) > abs(self.dirY):
                        if self.dirX > 0:
                            canvas[incanvai][incanvaj].char='v'
                        else:
                            canvas[incanvai][incanvaj].char='^'
                    else:
                        if self.dirY > 0:
                            canvas[incanvai][incanvaj].char='>'
                        else:
                            canvas[incanvai][incanvaj].char='<'

                elif qi>=0 and qi<len(self.worldMap) and qj>=0 and qj<len(self.worldMap[0]):
                    
                    if (qi,qj) in self.apmRoute:
                        canvas[incanvai][incanvaj].char='*'

                    else:
                        mapNum = self.worldMap[qi][qj]
                        if mapNum == 0:
                            canvas[incanvai][incanvaj].char=' '
                        else:
                            canvas[incanvai][incanvaj].char='%s'%mapNum
                
                else:
                    canvas[incanvai][incanvaj].char=' '

    def playerTurn(self,angle):

        rotangl = angle* self.rotSpeed

        # rotate dir
        oldDirX = self.dirX
        self.dirX = self.dirX * cos(-rotangl) - self.dirY * sin(-rotangl)
        self.dirY = oldDirX * sin(-rotangl) + self.dirY * cos(-rotangl)
        
        # rotate plane
        oldPlaneX = self.planeX
        self.planeX = self.planeX * cos(-rotangl) - self.planeY * sin(-rotangl)
        self.planeY = oldPlaneX * sin(-rotangl) + self.planeY * cos(-rotangl)


    def playerTurnRight(self):
        self.playerTurn(+1.0) 

    def playerTurnLeft(self):
        self.playerTurn(-1.0) 
    
    def playerFront(self):
        self.posX += self.dirX * self.moveSpeed
        self.posY += self.dirY * self.moveSpeed

    def playerBack(self):
        self.posX -= self.dirX * self.moveSpeed
        self.posY -= self.dirY * self.moveSpeed

    def playerStepRight(self):
        pass
    def playerStepLeft(self):
        pass

    def setAutoMove(self,value):
        """
        if true:
            random a new destination pointa

            perform Astart on it


        """
        self.autoPlayerMove = value

        if value:
            # random
            self.apmRoute = []

            while len(self.apmRoute) == 0:
                self.apmDestX,self.apmDestY = self._randomPointInMap()
                
                self.log.debug("dest: %s , %s", self.apmDestX,self.apmDestY)
                self.log.debug("player: %s , %s", int(self.posX),int(self.posY))
                
                self.apmRoute = astar.pathFind(self.worldMap,astar.DIRS8,
                        self.apmDestY,self.apmDestX, 
                        int(self.posY),int(self.posX))



    def _randomPointInMap(self):
        """
        find a random movable point on world map
        """
        found = 1

        while found>0:
            randX = random.randint(0,len(self.worldMap)-1)
            randY = random.randint(0,len(self.worldMap[0])-1)
            found = self.worldMap[randX][randY]

        return randX,randY






class DebugLayer():
    debugLines = {}
    muted = True
    def setText(self,sec,text):
        if sec in self.debugLines:
            self.debugLines[sec] = text
        else:
            self.debugLines[sec] = text

    def update(self,canvas):
        if not self.muted:
            lineID = 0
            for key in sorted(self.debugLines.keys()):
                for chaID, cha in  enumerate(key):
                    subpix = canvas[lineID][chaID]
                    subpix.char = cha
                    subpix.style = 2
                lineID+=1
                for chaID, cha in  enumerate("  %s"%self.debugLines[key]):
                    subpix = canvas[lineID][chaID]
                    subpix.char = cha
                    subpix.style = 2

                lineID+=1


