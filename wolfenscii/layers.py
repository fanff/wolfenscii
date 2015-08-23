import logging
from math import sqrt,sin,cos,atan2,pi
from libVect import Vect,StrechedTexture

from wolfenscii import astar
import random 
class MatrixSceneLayer():


    def __init__(self,debug,worldMap):
        self.log =  logging.getLogger(__name__+".MSL")
        
        self.debug = debug
        
        self.texmapping = {}
        self.worldMap = worldMap
        self.planeX= 0.0
        self.planeY= 0.66


        self.magicFactor = 0.5
        
        # real player Dir
        #self.rdirX = 0.0
        #self.rdirY = -1.0
        
        # normal to player direction
        self.dirX = -1.0
        self.dirY = 0.0
        
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
                
                mapvalue = self.worldMap[mapX][mapY]
                self.log.debug("mapvalue : %s ",mapvalue)

                if mapvalue in self.texmapping:
                    texture = self.texmapping[mapvalue]

                    collideList.append((perpWallDist,texture ))
                else:
                    collideList.append((perpWallDist, mapvalue ))

            except Exception as e:
                self.log.exception("wow")
        #endFOR

        return collideList

    def update(self,canvas):
        """
        1. player info

        2. render 3D

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

        # render  
        colHeight = len(canvas)
        colsCount = len(canvas[0])
        
        colisionsResult = self.raycast(colsCount)
        texturedColumns = []
        for distance,objetc in colisionsResult:
            # calculate wallHeight
            wallHeight = int (colHeight/(distance * self.magicFactor))
            self.log.debug("WH %s"%wallHeight)

            # calculate texture

            if isinstance(objetc,int):
                if wallHeight<colHeight:
                    missing = colHeight-wallHeight
                    missingUP = missing/2
                    missingDown = colHeight-wallHeight-missingUP

                    textureCol = [" " for _ in range(missingUP)]

                    textureCol+= [objetc for _ in range(wallHeight)]
                    textureCol+= [" " for _ in range(missingDown)]
                    #print len(textureCol)
                else:
                    textureCol = [objetc for _ in range(colHeight)]

                texturedColumns.append(textureCol)

            elif isinstance(objetc,StrechedTexture):

                colu = objetc.getColl(0.5,wallHeight)
                
                missing = colHeight-wallHeight
                missingUP = missing/2
                missingDown = colHeight-wallHeight-missingUP
                
                textureCol = [" " for _ in range(missingUP)]

                textureCol+= [_.char for _ in colu]
                textureCol+= [" " for _ in range(missingDown)]
                
                #print len(textureCol)
                #textureCol = [objetc for _ in range(colHeight)]

                texturedColumns.append(textureCol)


        # apply textures on canvas
        for colid ,textureCol in enumerate(texturedColumns):
            for i,canvasline in enumerate(canvas):

                pix = canvasline[colid]
                pix.char = ("%s"%textureCol[i])
                pix.style= 2

        #render map
        px = int(self.posX)
        py = int(self.posY)
        mapsize = 10
        for i in range(mapsize):
            for j in range(mapsize):
                qi = px+i-mapsize/2
                qj = py+j-mapsize/2
                
                incanvai = i
                incanvaj = j

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
                
                self.apmRoute = astar.pathFind(self.worldMap,astar.DIRS4,
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

#    //move forward if no wall in front of you
#    if (keyDown(SDLK_UP))
#    {
#      if(worldMap[int(posX + dirX * moveSpeed)][int(posY)] == false) posX += dirX * moveSpeed;
#      if(worldMap[int(posX)][int(posY + dirY * moveSpeed)] == false) posY += dirY * moveSpeed;
#    }
#    //move backwards if no wall behind you
#    if (keyDown(SDLK_DOWN))
#    {
#      if(worldMap[int(posX - dirX * moveSpeed)][int(posY)] == false) posX -= dirX * moveSpeed;
#      if(worldMap[int(posX)][int(posY - dirY * moveSpeed)] == false) posY -= dirY * moveSpeed;
#    }
#    //rotate to the right
#    if (keyDown(SDLK_RIGHT))
#    {
#      //both camera direction and camera plane must be rotated
#      double oldDirX = dirX;
#      dirX = dirX * cos(-rotSpeed) - dirY * sin(-rotSpeed);
#      dirY = oldDirX * sin(-rotSpeed) + dirY * cos(-rotSpeed);
#      double oldPlaneX = planeX;
#      planeX = planeX * cos(-rotSpeed) - planeY * sin(-rotSpeed);
#      planeY = oldPlaneX * sin(-rotSpeed) + planeY * cos(-rotSpeed);
#    }
#    //rotate to the left
#    if (keyDown(SDLK_LEFT))
#    {
#      //both camera direction and camera plane must be rotated
#      double oldDirX = dirX;
#      dirX = dirX * cos(rotSpeed) - dirY * sin(rotSpeed);
#      dirY = oldDirX * sin(rotSpeed) + dirY * cos(rotSpeed);
#      double oldPlaneX = planeX;
#      planeX = planeX * cos(rotSpeed) - planeY * sin(rotSpeed);
#      planeY = oldPlaneX * sin(rotSpeed) + planeY * cos(rotSpeed);
#    }
#  }
#}
#


#class SceneLayer():
#    def __init__(self,debug,gameBoard):
#        self.debug = debug
#        self.gb = gameBoard
#
#    def update(self,canvas):
#        self.debug.setText("Scene.playerPos","%s"%self.gb.playerPos)
#        self.debug.setText("Scene.angle","%s"%self.gb.playerAngle)
#        
#        colsCount = len(canvas[0])
#        self.debug.setText("Scene.colsCount","%s"%colsCount)
#        angleStep = ENGINEOPTION.FOV/colsCount
#        self.debug.setText("Scene.angleStep","%s"%angleStep)
#        
#        colHeight = len(canvas)
#        
#        startT = time.time()
#        for colToRender in range(colsCount):
#            angleDeg = (float(colToRender) - float(colsCount)/2.0 ) * angleStep
#            angleRAD = ((self.gb.playerAngle+angleDeg)* 2 * pi)/ 360.0
#
#            rayAngle = angleRAD
#
#            ray = Vect()
#            ray.rotate_ip(rayAngle)
#            
#            ray.mul_ip(100)
#            ray.add_ip(self.gb.playerPos)
#            pp=self.gb.playerPos
#            rsn = self.gb.rootSceneNode
#
#            collideList= rsn.collide(WallVect( ray,pp ,"") )
#            
#            if len(collideList) > 0:
#
#                shortestDistance = 100*100
#                nearestCollisionPoint = None
#                nearestCollider = None
#                
#                for collisionPoint , collider in collideList:
#                    dist = collisionPoint.add(pp.mul(-1.0)).normsq()
#                    if dist < shortestDistance:
#                        shortestDistance = dist
#                        nearestCollisionPoint = collisionPoint
#                        nearestCollider = collider
#                
#                shortestDistance  = max(0.5,sqrt(shortestDistance))
#                magicFactor = 0.5
#
#                wallHeight = int (colHeight/(shortestDistance * magicFactor))
#                
#                # calculate the vertical collumn from texture
#                if  wallHeight < colHeight:
#                    
#                    firsttier = int( (colHeight-wallHeight) / 2.0) 
#
#                    # calculate ratio of Wallvect collided
#                    collisionRatio = nearestCollider.collisionRatio(nearestCollisionPoint)
#
#                    # get the collum of pixel to print 
#                    wallcoll = nearestCollider.texture.getColl( collisionRatio,int(wallHeight))
#
#                    for lineid,line in enumerate(canvas):
#                        pix = canvas[lineid][colToRender]
#                        if lineid < firsttier:
#                            pix.char = ' '
#                        elif lineid < firsttier + wallHeight:
#
#                            p = wallcoll[lineid-firsttier]
#                            pix.style= p.style
#                            pix.char = p.char
#                        else:
#                            pix.char = ' '
#                else:
#                    extend = (wallHeight-colHeight)
#                    
#                    wallcoll = nearestCollider.texture.getColl( 0.1,wallHeight)
#
#                    for lineid,line in enumerate(canvas):
#                        pix = canvas[lineid][colToRender]
#                        pix.char = wallcoll[0].char
#                        pix.style= wallcoll[0].style
#            else:
#                colContent = "NORENDER # %s "%ray
#                colSize = len(colContent)
#                for lineid,line in enumerate(canvas):
#                    pix = canvas[lineid][colToRender]
#                    pix.char = colContent[lineid] if lineid < colSize else " "
#                    pix.style= 5
#
#            # end for
#        
#
#        renderTime = ((time.time()-startT)*1000)
#        self.debug.setText("Scene.updateTime ms","%s"%renderTime)
#        self.debug.setText("Scene.update / s","%s"%(1000.0/renderTime))
#        self.debug.setText("Scene.angleMax","%s"%angleRAD)
#        


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


