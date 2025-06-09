# pyright: reportUnusedCallResult=false

import random
from sasppu import Sprite


from app import SASPPUApp
import sasppu
import time

from events.input import BUTTON_TYPES, ButtonDownEvent, Buttons
from system.eventbus import eventbus
from system.scheduler.events import RequestStopAppEvent


from .direction import Direction, DirectionTuple
from .player import Player
from .world import World  # camera and world management
from .constants import (
    SPRITE_WIDTH,
    SPRITE_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSET_PATH,
    SPRITE_FILENAME,
)


class SASPPUTest(SASPPUApp):
    # entities
    player: Player
    caves: list[Sprite] = []
    trees: list[Sprite] = []
    # camera/world
    world: World
    # state
    request_fast_updates: bool
    exit: bool
    ms: sasppu.MainState
    cs: sasppu.CMathState
    bg0: sasppu.Background

    @property
    def all_sprites(self) -> list[Sprite]:
        """Return a list of all sprites in the app."""
        return [self.player.sprite] + self.trees + self.caves

    @property
    def all_sprites_non_player(self) -> list[Sprite]:
        """Return a list of all sprites except the player."""
        return self.trees + self.caves

    def __init__(self):
        super().__init__()
        self.button_states = Buttons(self)
        self.request_fast_updates = True
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
        # setup world camera
        # use SCREEN_WIDTH/HEIGHT from sasppu for world dimensions
        self.world = World(
            tile_size=SPRITE_WIDTH,
            world_size_tiles=(8, 8),
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
        )
        self.world.set_player(self.player)
        # register world objects
        for obj in self.all_sprites_non_player:
            self.world.register_object_random(obj)

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

        with open(ASSET_PATH + SPRITE_FILENAME, "rb") as f:
            data = f.read()
            sasppu.blit_sprite(0, 0, SPRITE_WIDTH * 4, SPRITE_HEIGHT, data, False)

        # with open(ASSET_PATH + "bg.bin", "rb") as f:
        #    sasppu.blit_background(0, 0, 256, 256, f.read())
        # with open(ASSET_PATH + "spr.bin", "rb") as f:
        #     sasppu.blit_sprite(104, 104, 32 * 8, 32, f.read())

        green_bg_color = sasppu.rgb555(1, 12, 1)  # RGB555 goes from 0 to 31
        sasppu.fill_background(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, green_bg_color)

    def init_player(self):
        spr = sasppu.oam[0]
        spr: Sprite = self.init_sprite(
            oam=0,
            x=104,
            y=104,
            width=SPRITE_WIDTH,
            height=SPRITE_HEIGHT,
            graphics_x=0,
            graphics_y=0,
        )
        self.player = Player(with_sprite=spr, graphics_x=0)

    def init_trees(self, n: int = 20):
        self.trees = []
        # create tree sprites; world placement will assign positions
        start = len(self.all_sprites)
        print(f"start at {start} for {n} trees, end at {start + n}")
        for i in range(start, start + n):
            spr = self.init_sprite(
                oam=i,
                x=0,
                y=0,
                width=SPRITE_WIDTH,
                height=SPRITE_HEIGHT,
                graphics_x=SPRITE_WIDTH * 2,
                graphics_y=0,
            )
            self.trees.append(spr)

    def init_caves(self, n: int = 5):
        self.caves = []
        # create tree sprites; world placement will assign positions
        start = len(self.all_sprites)
        print(f"start at {start} for {n} trees, end at {start + n}")
        for i in range(start, start + n):
            spr = self.init_sprite(
                oam=i,
                x=0,
                y=0,
                width=SPRITE_WIDTH,
                height=SPRITE_HEIGHT,
                graphics_x=SPRITE_WIDTH * 3,
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

    def _cleanup(self):
        eventbus.remove(ButtonDownEvent, self._handle_buttondown, self)
        self.exit = True
        self.minimise()

    async def run(self, render_update):
        while not self.exit:
            movement_button_states: dict[Direction, bool] = {
                DirectionTuple.N: self.button_states.get(BUTTON_TYPES["CANCEL"])
                and self.button_states.get(BUTTON_TYPES["RIGHT"]),
                DirectionTuple.S: self.button_states.get(BUTTON_TYPES["LEFT"])
                and self.button_states.get(BUTTON_TYPES["CONFIRM"]),
                DirectionTuple.E: self.button_states.get(BUTTON_TYPES["RIGHT"])
                and self.button_states.get(BUTTON_TYPES["CONFIRM"]),
                DirectionTuple.W: self.button_states.get(BUTTON_TYPES["CANCEL"])
                and self.button_states.get(BUTTON_TYPES["LEFT"]),
            }

            if not (
                movement_button_states.get(DirectionTuple.N)
                or movement_button_states.get(DirectionTuple.S)
                or movement_button_states.get(DirectionTuple.E)
                or movement_button_states.get(DirectionTuple.W)
            ):
                # only calculate diagonal movement if no cardinal direction is pressed
                diagonal_movement_button_states: dict[Direction, bool] = {
                    DirectionTuple.NW: self.button_states.get(BUTTON_TYPES["CANCEL"]),
                    DirectionTuple.NE: self.button_states.get(BUTTON_TYPES["RIGHT"]),
                    DirectionTuple.SW: self.button_states.get(BUTTON_TYPES["LEFT"]),
                    DirectionTuple.SE: self.button_states.get(BUTTON_TYPES["CONFIRM"]),
                }
                movement_button_states.update(diagonal_movement_button_states)

            for direction, pressed in movement_button_states.items():
                if pressed:
                    self.player.move(direction)

            if self.button_states.get(BUTTON_TYPES["UP"]):
                pass
            elif self.button_states.get(BUTTON_TYPES["DOWN"]):
                pass

            # self.button_states.clear()

            await render_update()
            # await asyncio.sleep(1)

    def draw(self):
        cur_time = time.ticks_ms()
        # update camera to center player and move world
        self.world.update()

        # self.ms.flags = sasppu.MainState.CMATH_ENABLE
        # ms.window_1_left = int((math.sin(cur_time / 1300.0) + 1) * 64)
        # ms.window_1_right = int((math.cos(cur_time / 1500.0) + 3) * 64)
        # self.cs.flags = sasppu.CMathState.FADE_ENABLE
        # self.cs.fade = int((math.sin(cur_time / 1000.0) + 1) * 127)
        # print("fps:", display.get_fps())

    def minimise(self):
        # Close this app each time
        eventbus.emit(RequestStopAppEvent(self))


# todo: party hat
