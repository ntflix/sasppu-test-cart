from sasppu import Sprite

from .direction import Direction, DirectionTuple
from .constants import SPRITE_WIDTH

GraphicsOffset = int


class Player:
    x: int
    y: int
    facing: Direction
    graphics_x: int
    sprite_offset: int
    sprite: Sprite

    directional_sprites: dict[Direction, GraphicsOffset] = {
        DirectionTuple.N: 0,
        DirectionTuple.S: 0,
        DirectionTuple.E: SPRITE_WIDTH,
        DirectionTuple.W: SPRITE_WIDTH,
        DirectionTuple.NE: SPRITE_WIDTH,
        DirectionTuple.NW: SPRITE_WIDTH,
        DirectionTuple.SE: SPRITE_WIDTH,
        DirectionTuple.SW: SPRITE_WIDTH,
    }

    def __init__(self, with_sprite: Sprite, graphics_x: int, x: int = 0, y: int = 0):
        self.sprite = with_sprite
        self.graphics_x = graphics_x
        self.sprite.graphics_x = self.graphics_x
        self.x = x
        self.y = y
        self.facing = DirectionTuple.N
        self.sprite_offset = 0

    def __calculate_offset(self):
        """Calculate the sprite offset based on the current facing direction."""
        self.sprite_offset = self.directional_sprites[self.facing]
        self.sprite.graphics_x = self.graphics_x + self.sprite_offset

    def __calculate_flags(self):
        print(f"Facing {DirectionTuple.to_string(self.facing)}")
        flags: list[int] = [self.sprite.ENABLED]

        parts = DirectionTuple.parts(self.facing)
        if DirectionTuple.W in parts:
            flags.append(self.sprite.FLIP_X)
        elif DirectionTuple.S in parts and not (
            DirectionTuple.E in parts or DirectionTuple.W in parts
        ):
            flags.append(self.sprite.FLIP_Y)

        self.sprite.flags = sum(flags)

    @property
    def world_x(self) -> int:
        """World X coordinate of the player."""
        return self.x

    @property
    def world_y(self) -> int:
        """World Y coordinate of the player."""
        return self.y

    def move(self, direction: Direction):
        """Moves the player in the specified DirectionTuple.
        Either move_x or move_y must be non-zero.
        Only one of them can be non-zero at a time."""

        self.facing = direction

        self.__calculate_offset()
        self.__calculate_flags()

        self.x += direction[0] * 2
        self.y += direction[1] * 2
        # Positioning of sprite is handled by World; removed direct sprite.x/y assignments
