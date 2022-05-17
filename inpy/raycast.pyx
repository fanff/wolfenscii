import cython
from libc.math cimport floor, ceil, round


def world_get_p(wm: cython.int[:],
              x: cython.int,
              y: cython.int
              ) -> cython.int:


    return world_get(wm,x,y)

@cython.cfunc
def world_get(wm: cython.int[:],
              x: cython.int,
              y: cython.int
              ) -> cython.int:


    return wm[x * 50 + y]


@cython.cfunc
def perform_dda(deltaDistX: cython.double,
                deltaDistY: cython.double,
                sdx: cython.double,
                sdy: cython.double,
                posX: cython.double,
                posY: cython.double,

                rayDirY:cython.double,
                rayDirX:cython.double,

                start_mapX: cython.int,
                start_mapY: cython.int,

                stepX: cython.int,
                stepY: cython.int,
                worldMap: cython.int[:],

                screenh:cython.int,
                pitch: cython.int,

                ):
    hit: cython.int = 0
    side: cython.int = 0

    sideDistX: cython.double = sdx
    sideDistY: cython.double = sdy

    mapX: cython.int = start_mapX
    mapY: cython.int = start_mapY

    perpWallDist : cython.double = 1.0

    while (hit == 0):
        # jump to next map square, either in x-direction, or in y-direction
        if (sideDistX < sideDistY):
            sideDistX += deltaDistX
            mapX += stepX
            side = 0
        else:
            sideDistY += deltaDistY
            mapY += stepY
            side = 1

        # Check if ray has hit a wall

        texNum = world_get(worldMap, mapX, mapY)
        if (texNum > 0):
            hit = 1


    # Calculate distance of perpendicular ray (Euclidean distance would give fisheye effect!)
    if(side == 0) :
        perpWallDist = (sideDistX - deltaDistX)
    else:
        perpWallDist = (sideDistY - deltaDistY)


    # Calculate height of line to draw on screen
    lineHeight: cython.int = int(screenh / perpWallDist)

    # calculate lowest and highest pixel to fill in current stripe
    drawStart : cython.int = -lineHeight / 2 + screenh / 2 + pitch
    if(drawStart < 0) :
        drawStart = 0

    drawEnd : cython.int = lineHeight / 2 + screenh / 2 + pitch
    if(drawEnd >= screenh) :
        drawEnd = screenh - 1


    # calculate value of wallX
    wallX : cython.double
    texX : cython.int
    if side==0:
        wallX = posY + perpWallDist * rayDirY
    else:
        wallX = posX + perpWallDist * rayDirX
    wallX -= floor((wallX)) # [0,1]


    texWidth:cython.int = 64
    # x coordinate on the texture
    texX = int(wallX * float(texWidth))
    if(side == 0 and rayDirX > 0) :texX = texWidth - texX - 1
    if(side == 1 and rayDirY < 0) :texX = texWidth - texX - 1

    return (sideDistX, sideDistY,
        mapX,
        mapY,
        side, texNum,perpWallDist,drawStart,drawEnd,texX)


@cython.cfunc
@cython.cdivision(True)
def one_ray(x: cython.int,
            w: cython.int,
            posX: cython.double,
            posY: cython.double,
            dirX: cython.double,
            dirY: cython.double,
            planeX: cython.double,
            planeY: cython.double,
            worldMap: cython.int[:],
            screenh:cython.int,
            pitch: cython.int,
            ):

    rayDirX: cython.double
    rayDirY: cython.double

    sdx: cython.double
    sdy: cython.double

    deltaDistX : cython.double
    deltaDistY : cython.double

    stepX : cython.int
    stepY : cython.int



    cameraX:cython.double = ((2 * x) / float(w)) - 1  # //x-coordinate in camera space
    rayDirX = dirX + (planeX * cameraX)
    rayDirY = dirY + (planeY * cameraX)

    deltaDistX = 1000 if (rayDirX == 0) else abs(1.0 / rayDirX)
    deltaDistY = 1000 if (rayDirY == 0) else abs(1.0 / rayDirY)

    start_mapX : cython.int = int((posX))
    start_mapY : cython.int = int((posY))


    if (rayDirX < 0):

        stepX = -1
        sdx = (posX - start_mapX) * deltaDistX

    else:

        stepX = 1
        sdx = (start_mapX + 1.0 - posX) * deltaDistX

    if (rayDirY < 0):

        stepY = -1
        sdy = (posY - start_mapY) * deltaDistY

    else:

        stepY = 1
        sdy = (start_mapY + 1.0 - posY) * deltaDistY




    (sideDistX, sideDistY,
        mapX,
        mapY,
        side, texNum,perpWallDist,drawStart,drawEnd,texX)= perform_dda(
                        deltaDistX,
                       deltaDistY,
                       sdx,
                       sdy,
                       posX,
                       posY,
                       rayDirY,
                       rayDirX,
                       start_mapX,
                       start_mapY,

                       stepX,
                       stepY,
                       worldMap,
                       screenh,
                       pitch)

    return (sideDistX, sideDistY,
        mapX,
        mapY,
        side, texNum,perpWallDist,drawStart,drawEnd,texX,
        posX,
        posY,
        )


def shoot_rays(
    worldMap : cython.int[:],
    posX: cython.double ,
    posY: cython.double ,  # //x and y start position

    dirX: cython.double,
    dirY: cython.double,  # //initial direction vector

    planeX: cython.double,
    planeY: cython.double,  # //the 2d raycaster version of camera plane

    screenw: cython.int = 5,
    screenh: cython.int = 300,

    pitch: cython.int= 100,


    ):



    x: cython.int



    allRes = []
    for x in range(screenw):


        ray_res = one_ray(x, screenw,
                posX,
                posY,

                dirX, dirY,
                planeX, planeY,worldMap,screenh,pitch)

        allRes.append(ray_res)

    return allRes
