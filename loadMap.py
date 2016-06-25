from  wolfenscii  import wap
from  wolfenscii.libVect  import WallVect,Vect
from pprint import pprint
if __name__ == "__main__":
    #res =   wap.readMap('wolfenscii/asset/map/map1.uxf')

    size = 30
    res = wap.randomMap(4,size)

    for r in res :

        if r["type"] == "RectWall":
            pass
            #print "->",
            #pprint(r)

        elif r["type"] == "playerStart":
            pass
            #print "->",r
    rootNode = wap.buildRootNode(res)

    rsn = rootNode[0]



    for i in range(size+1):
        for j in range(size+1):
            i = float(i)
            j = float(j)
            collideList= rsn.inside(Vect( i,j) )

            if collideList:
                print "#",
            else:
                print ".",

        print


