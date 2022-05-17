import numpy as np

import pygame as pg
import array

import pygame
from PIL.Image import Image

import PIL

from assetLoad import load_text


def pil_topygame(imgbuf):
    return pygame.image.fromstring(imgbuf.tobytes(), imgbuf.size, imgbuf.mode)


class PlayersStatus():
    movingFow = False
    movingBack = False


class MouseCTRL():

    def __init__(self):
        mapsize = 50
        self.screenw, self.screenh = 1000, 1000

        aa = np.zeros((mapsize, mapsize), dtype=int)

        aa[0, :] = 24
        aa[mapsize - 1, :] = 24
        aa[:, 0] = 24
        aa[:, mapsize - 1] = 24

        aa[1, 0] = 38
        aa[2, 0] = 31
        aa[3, 0] = 32
        aa[4, 0] = 49
        aa[5, 0] = 54

        aa[5, 5] = 49
        aa[5, 6] = 54
        aa[5, 7] = 49

        # aa[0, 1] = 60
        # aa[0, 2] = 61
        # aa[0, 3] = 62
        # aa[0, 4] = 63
        # aa[0, 5] = 64
        # aa[0, 6] = 65
        # aa[0, 7] = 66
        # aa[0, 8] = 67
        # aa[0, 9] = 68
        # aa[0, 10]= 69

        self.rawmap = aa

        self.worldMapArray = array.array('i', aa.reshape((mapsize ** 2)))

        self.screen = pygame.display.set_mode(
            [self.screenw, self.screenh])
        self.rayCount = 100

        self.running = True

        self.ppos = np.array([3.1, 3.2])
        self.pdir = np.array([1.0, 0.0])

        self.pplane = np.array([0.0, 0.66])

        self.debug_font = pygame.font.SysFont(None, 24)

        self.clock = pg.time.Clock()
        self.player_status: PlayersStatus = PlayersStatus()

        self.pitch = 0

        self.textures = load_text("./1375.png")

        self.texture_prebuff()

        self.pil_img = PIL.Image.new("RGB", (self.screenw, self.screenh), color=(0, 0, 0))
        self.blank_img = PIL.Image.new("RGB", (self.screenw, self.screenh), color=(0, 0, 0))

    def texture_prebuff(self):
        lineinter = self.screenw / self.rayCount

        for texNum, img in enumerate(self.textures):

            for heightidx in range(1, 1):
                for texX in range(2):
                    imgbuf = img.crop((texX, 0, texX + 1, 64))
                    imgbuf = imgbuf.resize((int(lineinter) + 1, heightidx * 2))

                    py_image = pil_topygame(imgbuf)

    def init(self):

        pygame.mouse.set_visible(False)

        pygame.event.set_grab(True)

    def update(self):
        # Did the user click the window close button?

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_UP:
                    self.player_status.movingFow = True

                if event.key == pygame.K_DOWN:
                    self.player_status.movingBack = True
            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_UP:
                    self.player_status.movingFow = False

                if event.key == pygame.K_DOWN:
                    self.player_status.movingBack = False


            elif event.type == pygame.MOUSEMOTION:

                pitch = float(event.rel[1])
                if pitch != 0:
                    self.pitch -= pitch

                    self.pitch = min(self.pitch, self.screenh // 2)
                    self.pitch = max(self.pitch, -self.screenh // 2)

                theta = event.rel[0]
                if theta != 0:
                    theta = float(theta)

                    theta = -theta / 50

                    c, s = np.cos(theta), np.sin(theta)
                    R = np.array(((c, -s), (s, c)))
                    self.pdir = np.dot(self.pdir, R)
                    self.pplane = np.dot(self.pplane, R)

        moveSpeed = 10 / (self.clock.get_fps() + 0.1)
        new_ppos = self.ppos
        if self.player_status.movingFow:
            new_ppos = self.ppos + self.pdir * moveSpeed
        if self.player_status.movingBack:
            new_ppos = self.ppos - self.pdir * moveSpeed

        if (self.rawmap[int(new_ppos[0] - .5), int(new_ppos[1])] == 0) and (
                self.rawmap[int(new_ppos[0] + .5), int(new_ppos[1])] == 0) and (
                self.rawmap[int(new_ppos[0]), int(new_ppos[1] - 0.5)] == 0) and (
                self.rawmap[int(new_ppos[0]), int(new_ppos[1] + 0.5)] == 0):
            self.ppos = new_ppos

    def render(self):
        self.screen.fill((0, 0, 0))

        self.pil_img = self.blank_img.copy()

        res = raycast.shoot_rays(self.worldMapArray,
                                 posX=self.ppos[0],
                                 posY=self.ppos[1],

                                 dirX=self.pdir[0],
                                 dirY=self.pdir[1],

                                 planeX=self.pplane[0],
                                 planeY=self.pplane[1],

                                 screenw=self.rayCount,
                                 screenh=self.screenh,
                                 pitch=self.pitch, )

        tex_color = {

            0: (50, 50, 50),
            1: (125, 125, 125),
            2: (0, 125, 125),
            3: (125, 125, 0),
            4: (0, 0, 125),
        }

        center = np.array([self.screenw // 2, (self.screenh // 3) * 2])

        img = self.debug_font.render("%.1f,%.1f" % (self.ppos[0], self.ppos[1]), True, (0, 255, 0))
        self.screen.blit(img, (10, 20))
        lineinter = self.screenw / self.rayCount

        for rayidx ,rayres in enumerate(res):
            (sideDistX, sideDistY,
             mapX,
             mapY,
             side, texNum, perpWallDist, drawStart, drawEnd,
             texX,
             posX,
             posY,

             ) = rayres
            lineHeight = int(self.screenh / perpWallDist)

            magicCut =int(lineinter*1.5)
            lineHeight = max((lineHeight//magicCut)*magicCut,1)


            drawStart= -lineHeight / 2 + self.screenh / 2 + self.pitch

            imgbuf:Image = self.textures[texNum]
        #
            imgbuf = imgbuf.crop((texX,0,texX+1,64))
            imgbuf = imgbuf.resize((int(lineinter)+1,lineHeight),
                                   resample=PIL.Image.Resampling.NEAREST)
        #
        #
        #
        #    # self.pil_img.paste(imgbuf,(int( rayidx*lineinter ),int(drawStart)))
            py_image = pil_topygame(imgbuf)
            self.screen.blit(py_image, (int((rayidx*lineinter)),drawStart))

        # self.screen.blit(pil_topygame(self.pil_img), (0,0))

        # player info
        mapSquareSize = 50
        pygame.draw.line(self.screen, (255, 0, 0),
                         center,
                         self.pdir * mapSquareSize + center, width=3)

        pygame.draw.line(self.screen, (0, 255, 0),
                         center + self.pdir * mapSquareSize,
                         self.pplane * mapSquareSize + center + self.pdir * mapSquareSize)

        img = self.debug_font.render("%.1f" % (self.clock.get_fps()), True, (0, 255, 0))

        self.screen.blit(img, (0, 0))

        pygame.display.flip()


def main():
    import pygame

    pygame.init()
    mc = MouseCTRL()
    # Set up the drawing window

    mc.init()

    while (mc.running):
        # mc.clock.tick()
        mc.update()
        mc.render()

        mc.clock.tick_busy_loop(800)
    pass


if __name__ == "__main__":
    import raycast

    main()
