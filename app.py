# pyright: reportUnusedCallResult=false

from app import SASPPUApp
import sasppu
import time

from events.input import BUTTON_TYPES, ButtonDownEvent, ButtonUpEvent
from system.eventbus import eventbus
from system.scheduler.events import RequestStopAppEvent

ASSET_PATH = "./apps/saspputest/"


class SASPPUTest(SASPPUApp):
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
        self.init_sprites()
        self.init_trees()

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
            sasppu.blit_sprite(0, 0, 64 * 2, 64, data, False)

        # with open(ASSET_PATH + "bg.bin", "rb") as f:
        #    sasppu.blit_background(0, 0, 256, 256, f.read())
        # with open(ASSET_PATH + "spr.bin", "rb") as f:
        #     sasppu.blit_sprite(104, 104, 32 * 8, 32, f.read())

        green_bg_color = sasppu.rgb555(1, 12, 1)  # RGB555 goes from 0 to 31
        sasppu.fill_background(0, 0, self.bg0.WIDTH, self.bg0.HEIGHT, green_bg_color)

    def init_sprites(self):
        self.sprites = []
        for i in range(0, 2):
            spr = sasppu.oam[0]
            spr.width = 64
            spr.height = 64
            spr.graphics_x = 0  # offset of 0 x for hog in spritesheet
            spr.graphics_y = 0
            spr.x = 10
            spr.y = 10
            spr.windows = sasppu.WINDOW_ALL
            spr.flags = spr.ENABLED  # | spr.DOUBLE | spr.FLIP_Y | spr.FLIP_X
            self.sprites.append(spr)

    def init_trees(self):
        self.trees = []
        for i in range(1, 5):
            pos = self.get_random_tree_position()
            spr = sasppu.oam[i]
            spr.width = 64
            spr.height = 64
            spr.graphics_x = 64  # offset of 64 x for tree in spritesheet
            spr.graphics_y = 0
            spr.x = pos[0]
            spr.y = pos[1]
            spr.windows = sasppu.WINDOW_ALL
            spr.flags = spr.ENABLED
            self.trees.append(spr)

    def get_random_tree_position(self):
        import random

        x = random.randint(20, 220)
        y = random.randint(20, 220)
        return x, y

    def move_sprites(self, move_x: int, move_y: int):
        rotation: int
        if move_x < 0:
            rotation = 1
        elif move_x > 0:
            rotation = 3
        elif move_y < 0:
            rotation = 2
        else:
            rotation = 0

        for _, spr in enumerate(self.sprites):
            print(spr.rotation)
            spr.x = spr.x + move_x * 8
            spr.y = spr.y + move_y * 8
            spr.rotation = rotation
            print("Sprite position: ", spr.x, spr.y, "rotation:", spr.rotation)

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
            for sprite in self.sprites:
                sprite.x = 0
                sprite.y = 0
        elif BUTTON_TYPES["LEFT"] in event.button:
            self.move_sprites(-1, 0)
        elif BUTTON_TYPES["RIGHT"] in event.button:
            self.move_sprites(1, 0)
        elif BUTTON_TYPES["UP"] in event.button:
            self.move_sprites(0, -1)
            for sprite in self.sprites:
                sprite.rotation = (sprite.rotation + 1) % 4
        elif BUTTON_TYPES["DOWN"] in event.button:
            self.move_sprites(0, 1)

    def minimise(self):
        # Close this app each time
        eventbus.emit(RequestStopAppEvent(self))
