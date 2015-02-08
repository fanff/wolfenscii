
import unittest
from lib import libVect


#import collidepoly

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass
    def test_intersect(self):

        ret = libVect.get_line_intersection( 
                0,0 ,  0,1 ,
                -.5,.5   , .5,.5)
        
        self.assertEqual( (0,.5), ret)
    
    def test_coll(self):
        
        ret = libVect.get_line_intersection( 
                0, 0 ,  0,1 ,
                -1,0   , -1,1)
        self.assertFalse( ret)

    def test_coll1(self):
        
        ret = libVect.get_line_intersection( 
                0,0 ,  0,0 ,
                0,0 ,  0,0 )
        self.assertFalse( ret)
class TestvectIntersection(unittest.TestCase):
    def test_intersect(self):

        ret = libVect.vectIntersection(
                libVect.Vect(0,0) , libVect.Vect( 0,1) ,
                libVect.Vect(-.5,.5)   , libVect.Vect(.5,.5))
        
        self.assertAlmostEqual( 0, ret.x)
        self.assertAlmostEqual( 0.5, ret.y)
       



        ret = libVect.vectIntersection(
                libVect.Vect(0,-10) , libVect.Vect( 0,10) ,
                libVect.Vect(-10,0)   , libVect.Vect(10,0))
        
        self.assertAlmostEqual( 0, ret.x)
        self.assertAlmostEqual( 0.0, ret.y)



class TestWallVect(unittest.TestCase):

    def test_collide(self):
        
        v0 = libVect.WallVect(libVect.Vect( 0,-10),libVect.Vect( 0,10),'w')
        
        v1 = libVect.WallVect(libVect.Vect( -10,0),libVect.Vect( 10,0),'w')
        
        #ret = v0.collide(v1)
        #self.assertAlmostEqual( 0, ret.x)
        #self.assertAlmostEqual( 0.0, ret.y)
   
class testRectWall(unittest.TestCase):

    def test_build(self):
        r = libVect.RectWall(libVect.Vect(-1,-1),libVect.Vect(1,1), 'w')
        
        #print r.wallList[0].a.x,
        #print r.wallList[0].a.y
        #
        #print r.wallList[1].a.x,
        #print r.wallList[1].a.y
        #
        #print r.wallList[2].a.x,
        #print r.wallList[2].a.y
        #
        #print r.wallList[3].a.x,
        #print r.wallList[3].a.y
        
    def test_collideRect(self):
        
        r = libVect.RectWall(libVect.Vect(-5,-5),libVect.Vect(10,10), 'w')
        ret  = r.collide(libVect.WallVect(libVect.Vect(0,0 ) , libVect.Vect(20,0 ) ,'r' ) )
        
        c , colider = ret[0]
        # 5 0
        #print ret[0].x,ret[0].y

        self.assertAlmostEqual(c.x,5)
        self.assertAlmostEqual(c.y,0)
        self.assertEqual(colider.char , 'w')

    
    def test_collideNested(self):
        r = libVect.RectWall(libVect.Vect(-5,-5),libVect.Vect(10,10), 'w')
        
        root = libVect.WallSet()
        root.nest(r)

        ret = root.collide(libVect.WallVect(libVect.Vect(0,0 ) , libVect.Vect(20,0 ) ,'r' ) )
        
        self.assertAlmostEqual(ret[0][0].x,5)
        self.assertAlmostEqual(ret[0][0].y,0)
        self.assertEqual(ret[0][1].char , 'w')


class TestVectRotate(unittest.TestCase):

    def test_rotate(self):
        from math import pi
        
        v = libVect.Vect()
        r = v.rotate(pi)
        
        self.assertAlmostEqual(r.x, -1.0)
        self.assertAlmostEqual(r.y, 0.0)
if __name__ == "__main__":
    unittest.main()
