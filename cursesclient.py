#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

# System Imports
import curses, time, traceback, sys
import curses.wrapper

# Twisted imports
from twisted.internet import reactor,task
from twisted.internet.protocol import ClientFactory
from twisted.python import log

from wolfenscii.libVect import Vect,WallVect,RectWall,WallSet,WallTexture
from math import pi
class TextTooLongError(Exception):
    pass

class CursesStdIO:
    """fake fd to be registered as a reader with the twisted reactor.
       Curses classes needing input should extend this"""

    def fileno(self):
        """ We want to select on FD 0 """
        return 0

    def doRead(self):
        """called when input is ready"""
    def logPrefix(self): 
        return 'CursesClient'


class Pixel():
    char = " "
    style = 1



class GameBoard():
    playerPos = Vect(0.0,0.0)
    WallTexture("W",5)
    playerAngle = 0.0

    baseWall = RectWall( Vect( -30.0,-30.0), Vect( 60.0,60.0), WallTexture("W",5) )
    rootSceneNode=WallSet()
    
    wallA = RectWall( Vect( 2.0,-2.0), Vect( 3.0,3.0), WallTexture("A",3))
    rootSceneNode.nest( wallA)

    wallC = RectWall( Vect( 1.0,2.0), Vect( 10.0,3.0), WallTexture("W",6))
    rootSceneNode.nest( wallC)
    rootSceneNode.nest( baseWall)

    def __init__(self,debug):
        self.debug = debug
    
    def playerTurnRight(self):
        self.playerAngle+=2.0
    def playerTurnLeft(self):
        self.playerAngle-=2.0
    def playerFront(self):
         
        ray = Vect()
        ray.rotate_ip(self.playerAngle*2*pi/360.0)
        
        ray.mul_ip(1)
        self.playerPos.add_ip(ray)

    def playerBack(self):
        ray = Vect()
        ray.rotate_ip(self.playerAngle*2*pi/360.0)
        
        ray.mul_ip(-1)
        self.playerPos.add_ip(ray)

class EngineOptions():
    FOV = 90.0

ENGINEOPTION = EngineOptions()
class ClearCanvas():
    clearPixer = Pixel()
    def update(self,canvas):
        for roid,ro in enumerate(canvas):
            for j,jch in enumerate(ro):
                canvas[roid][j].char = self.clearPixer.char


class SceneLayer():
    def __init__(self,debug,gameBoard):
        self.debug = debug
        self.gb = gameBoard

    def update(self,canvas):
        self.debug.setText("Scene.playerPos","%s"%self.gb.playerPos)
        self.debug.setText("Scene.angle","%s"%self.gb.playerAngle)
        
        colsCount = len(canvas[0])
        self.debug.setText("Scene.colsCount","%s"%colsCount)
        angleStep = ENGINEOPTION.FOV/colsCount
        self.debug.setText("Scene.angleStep","%s"%angleStep)
        
        colHeight = len(canvas)
        
        startT = time.time()
        for colToRender in range(colsCount):
            angleDeg = (float(colToRender) - float(colsCount)/2.0 ) * angleStep
            angleRAD = ((self.gb.playerAngle+angleDeg)* 2 * pi)/ 360.0

            rayAngle = angleRAD

            ray = Vect()
            ray.rotate_ip(rayAngle)
            
            ray.mul_ip(100)
            ray.add_ip(self.gb.playerPos)
            pp=self.gb.playerPos
            rsn = self.gb.rootSceneNode

            collideList= rsn.collide(WallVect( ray,pp ,"") )
            
            if len(collideList) > 0:

                shortestDistance = 200
                nearestCollisionPoint = None
                nearestCollider = None
                
                for collisionPoint , collider in collideList:
                    dist = collisionPoint.add(pp.mul(-1.0)).norm()
                    if dist < shortestDistance:
                        shortestDistance = dist
                        nearestCollisionPoint = collisionPoint
                        nearestCollider = collider
                
                
                magicFactor = 0.5

                wallHeight = colHeight/(shortestDistance * magicFactor)
                
                if  wallHeight < colHeight:
                    
                    firsttier = (colHeight-wallHeight)/2
                    

                    for lineid,line in enumerate(canvas):
                        pix = canvas[lineid][colToRender]
                        if lineid < firsttier:
                            pix.char = ' '
                        elif lineid < firsttier + wallHeight:
                            pix.style= nearestCollider.texture.colorCode
                            pix.char = nearestCollider.texture.char
                        else:
                            pix.char = ' '
                else:
                    colContent = "TOO BIG %s"%wallHeight

                    colSize = len(colContent)
                    for lineid,line in enumerate(canvas):
                        pix = canvas[lineid][colToRender]
                        pix.char = colContent[lineid] if lineid < colSize else " "
                        pix.style= 5
            else:
                colContent = "NORENDER # %s "%ray
                colSize = len(colContent)
                for lineid,line in enumerate(canvas):
                    pix = canvas[lineid][colToRender]
                    pix.char = colContent[lineid] if lineid < colSize else " "
                    pix.style= 5
        renderTime = ((time.time()-startT)*1000)
        self.debug.setText("Scene.updateTime ms","%s"%renderTime)
        self.debug.setText("Scene.update / s","%s"%(1000.0/renderTime))
        self.debug.setText("Scene.angleMax","%s"%angleRAD)
        




class DebugLayer():
    debugLines = {}
    def setText(self,sec,text):
        if sec in self.debugLines:
            self.debugLines[sec] = text
        else:
            self.debugLines[sec] = text

    def update(self,canvas):
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



class GameState(object):
    
    def __init__(self,rows,cols):
        self.canvas = []
        self.rows = rows
        self.cols= cols
        
        self.debugLayer = DebugLayer()
        self.gameBoard = GameBoard(self.debugLayer)
        
        self.sceneLayer = SceneLayer(self.debugLayer,self.gameBoard)

        
        self.layers = [ClearCanvas(),self.sceneLayer,self.debugLayer]
        self.lastKey = ""
        self.__populateCanvas()

    def __populateCanvas(self):

        # populateCanvas
        for i in range(self.rows):
            self.canvas.append([ Pixel() for j in range(self.cols)])


    def update(self):
        timeStart = time.time()
        for layer in self.layers:
            layer.update(self.canvas)
        
        self.debugLayer.setText("gs.update / s ",str(1.0/(time.time()-timeStart)))
        self.debugLayer.setText("lastKey",str(self.lastKey))
        
        return self.canvas
    
    def keyEvent(self,key):
        self.lastKey = key
        # 104 h
        # 105 i
        # 106 j
        # 107 k
        # 108 l
        # 109 m

        if key == 104:
            self.gameBoard.playerTurnLeft()
        if key == 107: # k
            self.gameBoard.playerFront()
        elif key == 106: # j
            self.gameBoard.playerBack()
        elif key == 108:
            self.gameBoard.playerTurnRight()

class Screen(CursesStdIO):
    def __init__(self, stdscr):
        self.stdscr = stdscr

        # set screen attributes
        self.stdscr.nodelay(1) # this is used to make input calls non-blocking
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)     # no annoying mouse cursor

        self.rows, self.cols = self.stdscr.getmaxyx()
        
        self.gameState = GameState(self.rows-1,self.cols)
        curses.start_color()

        # create color pair's 1 and 2
        self.colorSet = []
        self.__init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        self.__init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.__init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.__init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.__init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.__init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        self.__init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.__init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def __init_pair(self, key,c1,c2):
        self.colorSet.append(key)
        curses.init_pair(key, c1,c2)

    def connectionLost(self, reason):
        self.close()
    

    def redisplayLines(self):

        if self.canvas != None:
            for canvasLineKey , canvasLine in enumerate(self.canvas):
                for canvasColKey,pix in enumerate(canvasLine):
                    self.stdscr.addstr(canvasLineKey, canvasColKey, pix.char, 
                                   curses.color_pair(pix.style))

        self.stdscr.refresh()


    def doRead(self):
        """ Input is ready! """
        curses.noecho()
        
        c = self.stdscr.getch() # read a character
        
        self.gameState.keyEvent(c)
        
        if c == 113: # q
            reactor.stop()


    def close(self):
        """ clean up """

        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    
    def loopedCall(self):
        self.canvas = self.gameState.update()
        
        self.redisplayLines()





if __name__ == '__main__':
    stdscr = curses.initscr() # initialize curses
    screen = Screen(stdscr)   # create Screen object
    stdscr.refresh()
    reactor.addReader(screen) # add screen object as a reader to the reactor
    
    l = task.LoopingCall(screen.loopedCall)
    l.start(0.06)

    reactor.run() # have fun!
    screen.close()
