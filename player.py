from sasppu import Sprite

from .direction import Direction


class Player:
    x: int
    y: int
    facing: str
    graphics_x: int
    sprite_offset: int
    sprite: Sprite

    def __init__(self, with_sprite: Sprite, graphics_x: int, x: int = 0, y: int = 0):
        self.sprite = with_sprite
        self.graphics_x = graphics_x
        self.sprite.graphics_x = self.graphics_x
        self.x = x
        self.y = y
        self.facing = Direction.TOP
        self.sprite_offset = 0

    def __calculate_offset(self):
        if (self.facing == Direction.TOP) or (self.facing == Direction.BOTTOM):
            self.sprite_offset = 0
        elif (self.facing == Direction.LEFT) or (self.facing == Direction.RIGHT):
            self.sprite_offset = 64

        self.sprite.graphics_x = self.graphics_x + self.sprite_offset

    def __calculate_flags(self):
        flags: list[int] = [self.sprite.ENABLED]
        if self.facing == Direction.RIGHT:
            flags.append(self.sprite.FLIP_X)
        elif self.facing == Direction.TOP:
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

    def move(self, move_x: int, move_y: int):
        """Moves the player in the specified direction.
        Either move_x or move_y must be non-zero.
        Only one of them can be non-zero at a time."""

        assert (move_x != 0) or (
            move_y != 0
        ), "Either move_x or move_y must be non-zero."
        # assert (move_x == 0) or (
        #     move_y == 0
        # ), "Only one of move_x or move_y can be non-zero at a time."

        if move_x < 0:
            self.facing = Direction.RIGHT
        elif move_x > 0:
            self.facing = Direction.LEFT
        elif move_y < 0:
            self.facing = Direction.BOTTOM
        else:
            self.facing = Direction.TOP

        self.__calculate_offset()
        self.__calculate_flags()

        self.x += move_x * 8
        self.y += move_y * 8
        # Positioning of sprite is handled by World; removed direct sprite.x/y assignments
