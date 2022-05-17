


# https://mathworld.wolfram.com/Line-LineIntersection.html
import cython

import array


import numpy as np


if __name__=="__main__":

    import os

    # os.environ["PATH"] = os.environ["PATH"]+";"+"E:\\code\\wolfenscii\\inpy\\build\\lib.win-amd64-3.10\\inpy"


    import raycast


    mapsize=50
    aa = np.zeros((mapsize, mapsize),dtype=int)

    aa[0,:] = 1
    aa[mapsize-1, :] = 1
    aa[:, 0] = 1
    aa[:, mapsize-1] = 1
    print(aa)
    aa = aa.reshape((mapsize**2))
    aa = array.array('i', aa)

    #res = raycast.world_get(aa,2,3)
    import time
    for i in range(10):
        r = time.time()
        res = raycast.say_hello_to(aa,screenw= 3000)


        print(time.time()-r)

    res = raycast.shoot_rays(aa,
                                posX=2.2,
                                posY=1.2,

                               planeX=0,
                               planeY=0.66,
                            pitch=-10,

                               screenw= 3,
                               screenh = 100,)
    print(res)