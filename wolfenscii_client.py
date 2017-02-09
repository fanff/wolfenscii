#!/usr/bin/env python

# System Imports
import curses, time, traceback, sys
import curses.wrapper

# Twisted imports
from twisted.internet import reactor,task
from twisted.internet.protocol import ClientFactory
from twisted.python import log

from wolfenscii.libVect import ColorTexture, Pixel,StrechedTexture

from math import pi,sqrt,floor
from wolfenscii.layers import MatrixSceneLayer,DebugLayer
import logging

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




class EngineOptions():
    FOV = 90.0
    FPS = 100.0



class ClearCanvas():
    clearPixer = Pixel()
    def update(self,canvas):
        for roid,ro in enumerate(canvas):
            for j,jch in enumerate(ro):
                canvas[roid][j].char = self.clearPixer.char



class GameState(object):
    """
    Contains :

    * Canvas list

    * List of layers

    """
    def __init__(self,rows,cols):
        self.canvas = []
        self.rows = rows
        self.cols= cols

        self.debugLayer = DebugLayer()

        worldMap=[
                [1,1,1,1,1,1,2,1,3,1,3,1,3,1,3,1,1],
                [3,0,0,0,0,0,0,0,3,2,0,0,0,0,0,0,3],
                [3,0,0,0,2,0,0,0,3,2,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,3,2,0,0,0,0,0,0,3],
                [3,0,0,0,0,0,0,0,3,2,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,3,2,0,0,8,8,8,8,8],
                [3,0,0,0,0,0,0,0,4,2,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,4,2,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,4,2,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,8,8,8,8,8,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [5,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]


        self.sceneLayer = MatrixSceneLayer(self.debugLayer,worldMap)

        # load Texture
        self.sceneLayer.texmapping[1] = StrechedTexture("wolfenscii/asset/test/tex1")
        self.sceneLayer.texmapping[2] = StrechedTexture("wolfenscii/asset/test/tex2")
        self.sceneLayer.texmapping[3] = StrechedTexture("wolfenscii/asset/test/tex3")
        self.sceneLayer.texmapping[4] = StrechedTexture("wolfenscii/asset/test/tex4")
        self.sceneLayer.texmapping[5] = StrechedTexture("wolfenscii/asset/tex/Red3")
        self.sceneLayer.texmapping[6] = StrechedTexture("wolfenscii/asset/tex/brick1")
        self.sceneLayer.texmapping[7] = StrechedTexture("wolfenscii/asset/test/tex3")
        self.sceneLayer.texmapping[8] = StrechedTexture("wolfenscii/asset/test/tex3")
        self.sceneLayer.texmapping[9] = StrechedTexture("wolfenscii/asset/test/tex3")


        self.layers = [
                ClearCanvas(),
                self.sceneLayer,
                self.debugLayer]
        self.lastKey = ""
        self.lastMouse = ""
        self.__populateCanvas()

    def resetCanvas(self,rows,cols):
        self.canvas = []
        self.rows = rows
        self.cols= cols
        self.__populateCanvas()

    def __populateCanvas(self):

        # populateCanvas
        for i in range(self.rows):
            self.canvas.append([ Pixel() for j in range(self.cols)])


    def update(self):
        """

        Call every layer to fill the canvas.
        """
        # play random player move

        timeStart = time.time()
        for layer in self.layers:
            layer.update(self.canvas)

        self.debugLayer.setText("gs.update / s ","%.1f"%(1.0/(time.time()-timeStart)))
        self.debugLayer.setText("lastKey",str(self.lastKey))
        self.debugLayer.setText("lastMouse",str(self.lastMouse))

        return self.canvas
    
    def mouseEvent(self,x,y,pld):
        """
        dispatch

        """
        self.lastMouse='%f,%f %d '%(x,y,pld)
        diff = x - self.cols/2

        self.sceneLayer.playerTurn(diff/3.0)



    def keyEvent(self,key):
        """
        Dispatch key pressed as an action

        """

        self.lastKey = key
        # 104 h
        # 105 i
        # 106 j
        # 107 k
        # 108 l
        # 109 m

        if key in (104,115):  # h
            self.sceneLayer.playerTurnLeft()
        elif key == 72: # H
            self.sceneLayer.playerStepLeft()
        elif key in (75,101,107): # k
            self.sceneLayer.playerFront()
        elif key in (74, 100,106) : # j
            self.sceneLayer.playerBack()
        elif key in (102,108): # l
            self.sceneLayer.playerTurnRight()
        elif key == 76: # L
            self.sceneLayer.playerStepRight()
        elif key in (116,): # d
            # stop debug
            self.debugLayer.muted = not self.debugLayer.muted
        elif key == 97: # a
            # enable autoMove
            self.sceneLayer.setAutoMove(not self.sceneLayer.autoPlayerMove)

        elif key == 111: # o
            # decrease magic factor
            self.sceneLayer.magicFactor -=0.1
        elif key == 112: # p
            # increase magic factor
            self.sceneLayer.magicFactor +=0.1


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
        self.__init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.__init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.__init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
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
        """
        2d world
        """
        if self.canvas != None:
            for canvasLineKey , canvasLine in enumerate(self.canvas):
                for canvasColKey,pix in enumerate(canvasLine):
                    self.stdscr.addstr(canvasLineKey, canvasColKey, pix.char,
                                   curses.color_pair(pix.style))

        self.stdscr.refresh()


    def doRead(self):
        """ Input is ready! """
        try:
            curses.noecho()

            c = self.stdscr.getch() # read a character

            if c == curses.KEY_MOUSE:
                _ , x,y,_,pld = curses.getmouse()
                self.gameState.mouseEvent(x,y,pld)
            else:
                self.gameState.keyEvent(c)

            if c == 113: # q
                reactor.stop()
        except Exception as e:
            logging.exception("error in do Read")

    def close(self):
        """ clean up """

        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def loopedCall(self):
        # safe way
        try:
            r,c = self.stdscr.getmaxyx()

            if r!=self.rows or c!=self.cols:
                raise Exception("fdsljl")
            self.canvas = self.gameState.update()
            self.redisplayLines()
        except:
            self.rows, self.cols = self.stdscr.getmaxyx()
            self.gameState.resetCanvas(self.rows-1,self.cols)


import argparse
if __name__ == '__main__':
    #logging.basicConfig(filename="./log.log")
    import argparse

    parser = argparse.ArgumentParser(description='Wolfenscii')
    parser.add_argument('-D', dest='debug', action='store_true',
                        default=False,
                        help='Debug into ./log.log file by default')

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(filename="./log.log",level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    ENGINEOPTION = EngineOptions()

    stdscr = curses.initscr() # initialize curses
    curses.mousemask(1)
    screen = Screen(stdscr)   # create Screen object
    stdscr.refresh()
    reactor.addReader(screen) # add screen object as a reader to the reactor

    l = task.LoopingCall(screen.loopedCall)
    l.start(1.0/ENGINEOPTION.FPS )
    reactor.run() # have fun!
    screen.close()

