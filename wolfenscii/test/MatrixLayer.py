import unittest
import logging

from wolfenscii.layers import MatrixSceneLayer
from wolfenscii.libVect import Pixel,StrechedTexture

class MatScenePlayerOp(unittest.TestCase):

    def setUp(self):
        pass


    def test_rotate1(self):
        logging.basicConfig(level = logging.DEBUG)
        
        worldMap=[
                ]

        lay = MatrixSceneLayer(None,worldMap)

        lay.playerTurnRight()

def printCanvas(canvas):
    """

    """
    for i in canvas:
        for j in i:
            print j.char,
        print
    print 

class MatScene(unittest.TestCase):

    def setUp(self):
        pass


    def test1(self):
        logging.basicConfig(level = logging.DEBUG)
        
        worldMap=[
                [1,1,1,1,1,1,2,1,3,1,3,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,2,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,6,0,0,8,8,8,8,1],
                [1,0,2,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,6,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]

        lay = MatrixSceneLayer(None,worldMap)



        res = lay.raycast(10)
        print res

    def test2(self):
        logging.basicConfig(level = logging.DEBUG)
        
        worldMap=[
                [1,1,1,1,1,3,2,1,4,1,3,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,2,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]

        lay = MatrixSceneLayer(None,worldMap)

        line = 34
        cols = 41
        canvas = [ [Pixel() for i in range(cols)] for j in range(line)]

        res = lay.update(canvas)

    def test3(self):
        #logging.basicConfig(level = logging.DEBUG)
        
        worldMap=[
                [1,1,2,2,2,3,2,1,4,1,3,1,1,1,1,1,1],
                [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]
        
        
        lay = MatrixSceneLayer(None,worldMap)
        
        
        # load Texture 
        lay.texmapping[1] = StrechedTexture("wolfenscii/asset/test/tex2")

        line = 34
        cols = 41
        canvas = [ [Pixel() for i in range(cols)] for j in range(line)]

        res = lay.update(canvas)
        printCanvas(canvas)

    def test_randomPoint(self):
        #logging.basicConfig(level = logging.DEBUG)
        
        worldMap=[
                [1,1,2,2,2,3,2,1,4,1,3,1,1,1,1,1,1],
                [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]
        
        
        lay = MatrixSceneLayer(None,worldMap)
        
        for i in range(1000):
            x,y = lay._randomPointInMap()

            self.assertTrue(worldMap[x][y] == 0)

    def test_setAutoMove(self):
        #logging.basicConfig(level = logging.DEBUG)
        
        worldMap=[
                [1,1,2,2,2,3,2,1,4,1,3,1,1,1,1,1,1],
                [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]
        
        
        lay = MatrixSceneLayer(None,worldMap)
        lay.posX = 1
        lay.posY = 1
        for i in range(1000):
            lay.setAutoMove(True)
            for x,y in lay.apmRoute:
                worldMap[x][y]


if __name__ == "__main__":
    unittest.main()
