
import unittest
import logging
import time
from wolfenscii.layers import MatrixSceneLayer
from wolfenscii.libVect import Pixel,StrechedTexture
from wolfenscii import astar

class AstarTest(unittest.TestCase):

    def setUp(self):
        pass


    def test_1(self):
        the_map=[
                [1,1,2,2,2,3,2,1,4,1,3,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]
        



        t = time.time()
        
        route = astar.pathFind(the_map,astar.DIRS8, 
                1, 1,
                1, 1)
        self.assertTrue(len(route)>0)
        
        route = astar.pathFind(the_map,astar.DIRS8, 
                1, 1,
                10, 1)
        print route
        self.assertTrue(len(route)>0)

        #print 'Time to generate the route (seconds): ', time.time() - t
        #print 'Route:'
        #print route

        

if __name__ == "__main__":

    unittest.main()
