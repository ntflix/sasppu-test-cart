# pyright: reportUnusedCallResult=false

import random
from sasppu import Sprite


from app import SASPPUApp
import sasppu
import time

from events.input import BUTTON_TYPES, ButtonDownEvent, ButtonUpEvent
from system.eventbus import eventbus
from system.scheduler.events import RequestStopAppEvent

from .player import Player

ASSET_PATH = "./apps/saspputest/"


class SASPPUTest(SASPPUApp):
    player: Player
    caves: list[Sprite] = []
    trees: list[Sprite] = []

    def __init__(self):
        super().__init__()
        self.request_fast_updates = True
        eventbus.on(ButtonDownEvent, self._handle_buttondown, self)
        self.exit = False
        self.ms = sasppu.MainState()
        self.ms.bind()
        self.cs = sasppu.CMathState()
        self.cs.bind()
        self.bg0 = sasppu.Background()
        self.bg0.bind(0)
        self.init_player()
        self.init_trees()
        self.init_caves()

        self.ms.mainscreen_colour = sasppu.TRANSPARENT_BLACK
        self.ms.flags = (
            sasppu.MainState.BG0_ENABLE
            | sasppu.MainState.BGCOL_WINDOW_ENABLE
            | sasppu.MainState.SPR0_ENABLE
        )
        self.cs.flags = (
            sasppu.CMathState.CMATH_ENABLE
            | sasppu.CMathState.ADD_SUB_SCREEN
            | sasppu.CMathState.HALF_MAIN_SCREEN
            | sasppu.CMathState.FADE_ENABLE
        )
        self.ms.bgcol_windows = (
            ((sasppu.WINDOW_B | sasppu.WINDOW_AB) << 4)
            | sasppu.WINDOW_A
            | sasppu.WINDOW_AB
        )

        self.bg0.flags = 0
        self.bg0.windows = 0x0F
        self.bg0.x = 0
        self.bg0.y = 0

        self.ms.window_1_left = 10
        self.ms.window_1_right = 200
        self.ms.window_2_left = 180
        self.ms.window_2_right = 230

        with open(ASSET_PATH + "hedhog.bin", "rb") as f:
            data = f.read()
            sasppu.blit_sprite(0, 0, 64 * 4, 64, data, False)

        # with open(ASSET_PATH + "bg.bin", "rb") as f:
        #    sasppu.blit_background(0, 0, 256, 256, f.read())
        # with open(ASSET_PATH + "spr.bin", "rb") as f:
        #     sasppu.blit_sprite(104, 104, 32 * 8, 32, f.read())

        green_bg_color = sasppu.rgb555(1, 12, 1)  # RGB555 goes from 0 to 31
        sasppu.fill_background(0, 0, self.bg0.WIDTH, self.bg0.HEIGHT, green_bg_color)

    def init_player(self):
        spr = sasppu.oam[0]
        spr: Sprite = self.init_sprite(
            oam=0,
            x=0,
            y=0,
            width=64,
            height=64,
            graphics_x=0,
            graphics_y=0,
        )
        self.player = Player(with_sprite=spr, graphics_x=0)

    def init_trees(self):
        self.trees = []
        for i in range(1, 5):
            pos = self.get_position_not_near_existing_sprites()
            spr = self.init_sprite(
                oam=i,
                x=pos[0],
                y=pos[1],
                width=64,
                height=64,
                graphics_x=128,
                graphics_y=0,
            )
            self.trees.append(spr)

    def init_caves(self):
        self.caves = []
        for i in range(5, 8):
            pos = self.get_position_not_near_existing_sprites()
            spr = self.init_sprite(
                oam=i,
                x=pos[0],
                y=pos[1],
                width=64,
                height=64,
                graphics_x=192,
                graphics_y=0,
            )
            flip_x = random.choice([True, False])
            if flip_x:
                spr.flags = spr.FLIP_X + spr.ENABLED
            self.caves.append(spr)

    def init_sprite(
        self,
        oam: int,
        x: int,
        y: int,
        width: int,
        height: int,
        graphics_x: int = 0,
        graphics_y: int = 0,
    ):
        spr = sasppu.oam[oam]
        spr.width = width
        spr.height = height
        spr.graphics_x = graphics_x
        spr.graphics_y = graphics_y
        spr.x = x
        spr.y = y
        spr.windows = sasppu.WINDOW_ALL
        spr.flags = spr.ENABLED
        return spr

    def get_random_position(self):
        import random

        x = random.randint(20, 220)
        y = random.randint(20, 220)
        return x, y

    def get_position_not_near_existing_sprites(self, radius: int = 48):
        """Get a random position that is not too close to existing sprites."""
        while True:
            pos = self.get_random_position()
            too_close = False
            for spr in self.trees + self.caves:
                if abs(pos[0] - spr.x) < radius and abs(pos[1] - spr.y) < radius:
                    too_close = True
                    break
            if not too_close:
                return pos

    def _cleanup(self):
        eventbus.remove(ButtonDownEvent, self._handle_buttondown, self)
        self.exit = True
        self.minimise()

    async def run(self, render_update):
        while not self.exit:
            await render_update()
            # await asyncio.sleep(1)

    def draw(self):
        cur_time = time.ticks_ms()

        # self.ms.flags = sasppu.MainState.CMATH_ENABLE
        # ms.window_1_left = int((math.sin(cur_time / 1300.0) + 1) * 64)
        # ms.window_1_right = int((math.cos(cur_time / 1500.0) + 3) * 64)
        # self.cs.flags = sasppu.CMathState.FADE_ENABLE
        # self.cs.fade = int((math.sin(cur_time / 1000.0) + 1) * 127)
        # print("fps:", display.get_fps())

    def _handle_buttondown(self, event: ButtonDownEvent):
        if BUTTON_TYPES["CANCEL"] in event.button:
            self._cleanup()
        elif BUTTON_TYPES["LEFT"] in event.button:
            self.player.move(-1, 0)
        elif BUTTON_TYPES["RIGHT"] in event.button:
            self.player.move(1, 0)
        elif BUTTON_TYPES["UP"] in event.button:
            self.player.move(0, -1)
        elif BUTTON_TYPES["DOWN"] in event.button:
            self.player.move(0, 1)

    def minimise(self):
        # Close this app each time
        eventbus.emit(RequestStopAppEvent(self))


# todo: party hat
