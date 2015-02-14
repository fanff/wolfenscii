
import unittest
from wolfenscii import libVect

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
        
        ret = v0.collide(v1)
        self.assertAlmostEqual( 0, ret.x)
        self.assertAlmostEqual( 0.0, ret.y)
   
    def test_collisionRatio(self):
        v0 = libVect.WallVect(libVect.Vect( 0,-10),libVect.Vect( 0,10),'w')

        self.assertAlmostEqual( 0.5, v0.collisionRatio( libVect.Vect(0,0) ) )
        self.assertAlmostEqual( 0.0, v0.collisionRatio( libVect.Vect(0,-10) ) )
        self.assertAlmostEqual( 1.0, v0.collisionRatio( libVect.Vect(0,10) ) )
        self.assertAlmostEqual( .75, v0.collisionRatio( libVect.Vect(0,5) ) )
        self.assertAlmostEqual( .25, v0.collisionRatio( libVect.Vect(0,-5) ) )
        
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
        self.assertEqual(colider.texture , 'w')

    
    def test_collideNested(self):
        r = libVect.RectWall(libVect.Vect(-5,-5),libVect.Vect(10,10), 'w')
        
        root = libVect.WallSet()
        root.nest(r)

        ret = root.collide(libVect.WallVect(libVect.Vect(0,0 ) , libVect.Vect(20,0 ) ,'r' ) )
        
        self.assertAlmostEqual(ret[0][0].x,5)
        self.assertAlmostEqual(ret[0][0].y,0)
        self.assertEqual(ret[0][1].texture , 'w')


class TestVectRotate(unittest.TestCase):

    def test_rotate(self):
        from math import pi
        
        v = libVect.Vect()
        r = v.rotate(pi)
        
        self.assertAlmostEqual(r.x, -1.0)
        self.assertAlmostEqual(r.y, 0.0)


class TestStrechedTexture(unittest.TestCase):

    def test_loadTexture(self):
        tex = libVect.StrechedTexture("wolfenscii/asset/test/tex1")
        #print tex.texData
        
        tex = libVect.StrechedTexture("wolfenscii/asset/test/tex2")
        #print tex.texData

    def test_renderTex1(self):
        tex = libVect.StrechedTexture("wolfenscii/asset/test/tex1")

        for i in range(15):
            res = tex.getColl(i/10.0,1)
            self.assertTrue(res[0].char == 'A')
            self.assertTrue(len(res) == 1)
    def test_renderTex1_collHeight(self):
        tex = libVect.StrechedTexture("wolfenscii/asset/test/tex1")

        res = tex.getColl(0.1,0)
        self.assertTrue(len(res) == 0)

        res = tex.getColl(0.1,1)
        self.assertTrue(len(res) == 1)
        for p in res:
            self.assertEqual(p.char , 'A')
        
        res = tex.getColl(0.1,2)
        self.assertTrue(len(res) == 2)
        for p in res:
            self.assertEqual(p.char , 'A')

        res = tex.getColl(0.1,4)
        self.assertTrue(len(res) == 4)
        for p in res:
            self.assertEqual(p.char , 'A')


    def test_renderTex2(self):
        tex = libVect.StrechedTexture("wolfenscii/asset/test/tex2")

        for i in range(11):
            ratio = i/10.0
            #print "ratio", ratio

            res = tex.getColl(ratio,1)
            if ratio < 0.5:
                self.assertEqual(res[0].char ,'A')
                self.assertTrue(len(res) == 1)
            else:
                self.assertEqual(res[0].char ,'B')
                self.assertTrue(len(res) == 1)
        
        for i in range(11):
            ratio = i/10.0
            #print "ratio", ratio

            res = tex.getColl(ratio,2)
            self.assertTrue(len(res) == 2)
            if ratio < 0.5:
                self.assertEqual(res[0].char ,'A')
                self.assertEqual(res[1].char ,'C')
            else:
                self.assertEqual(res[0].char ,'B')
                self.assertEqual(res[1].char ,'D')

    def test_renderTex2_collHeight(self):
        tex = libVect.StrechedTexture("wolfenscii/asset/test/tex2")

        res = tex.getColl(0.1,0)
        self.assertTrue(len(res) == 0)
        
        res = tex.getColl(0.1,1)
        self.assertTrue(len(res) == 1)
        self.assertEqual(res[0].char , 'A')

        res = tex.getColl(0.1,2)
        self.assertTrue(len(res) == 2)
        self.assertEqual(res[0].char , 'A')
        self.assertEqual(res[1].char , 'C')

        
        res = tex.getColl(0.1,3)
        self.assertTrue(len(res) == 3)
        self.assertEqual(res[0].char , 'A')
        self.assertEqual(res[1].char , 'A')
        self.assertEqual(res[2].char , 'C')
        
        
        res = tex.getColl(0.1,4)
        self.assertTrue(len(res) == 4)
        self.assertEqual(res[0].char , 'A')
        self.assertEqual(res[1].char , 'A')
        self.assertEqual(res[2].char , 'C')
        self.assertEqual(res[3].char , 'C')
if __name__ == "__main__":
    
    unittest.main()
