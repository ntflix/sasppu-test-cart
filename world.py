from sasppu import Sprite
import random

from .player import Player


class World:
    """
    World handles positioning of game objects relative to the player (camera).
    Coordinates are in pixels. The world is tile-based, with tile_size defining the grid.
    """

    world_size_tiles: tuple[int, int]
    screen_size: tuple[int, int]

    def __init__(
        self,
        tile_size: int,
        world_size_tiles: tuple[int, int],
        screen_width: int,
        screen_height: int,
    ):
        self.tile_size = tile_size
        self.screen_size = (screen_width, screen_height)
        self.screen_center_x = self.screen_size[0] // 2
        self.screen_center_y = self.screen_size[1] // 2
        self.world_size_tiles = world_size_tiles
        self.player: Player | None = None
        self.player_sprite: Sprite | None = None
        # map from (tile_x, tile_y) to sprite
        self.objects: dict[tuple[int, int], Sprite] = {}
        # initialize free tile list and shuffle for random placement
        self.free_tiles: list[tuple[int, int]] = [
            (x, y)
            for x in range(self.world_size_tiles[0])
            for y in range(self.world_size_tiles[1])
        ]
        self._shuffle_free_tiles()
        print(
            f"World initialized with tile size {self.tile_size} and size {self.world_size_tiles} tiles"
        )

    def _shuffle_free_tiles(self) -> None:
        """Shuffle self.free_tiles in place with Fisher–Yates algorithm."""
        print("Shuffling free tiles for random placement")
        n = len(self.free_tiles)
        for i in range(n - 1, 0, -1):
            # getrandbits is available in MicroPython; enough bits for n<=65536
            j = random.getrandbits(16) % (i + 1)
            # swap
            self.free_tiles[i], self.free_tiles[j] = (
                self.free_tiles[j],
                self.free_tiles[i],
            )
        print("Free tiles shuffled")

    def set_player(self, player: Player) -> None:
        """Attach the player entity to the world for camera centering."""
        self.player = player
        self.player_sprite = player.sprite

    def register_object(self, world_x: int, world_y: int, sprite: Sprite) -> None:
        """Place a sprite at a given world position (in pixels) on the tile grid."""
        key = (world_x // self.tile_size, world_y // self.tile_size)
        if key in self.objects:
            raise ValueError(f"Tile {key} already occupied")
        self.objects[key] = sprite

    def register_object_random(self, sprite: Sprite) -> None:
        """Place a sprite at a random position on the tile grid.
        Automatically avoids occupied tiles."""
        # ensure free tiles are available
        if not self.free_tiles:
            raise ValueError("No free tiles available to place sprite")
        # pop a random tile key
        key = self.free_tiles.pop()
        tx, ty = key
        self.objects[key] = sprite
        print(
            f"Going to attempt to place sprite at tile {key} ({tx}, {ty}) at {tx * self.tile_size}, {ty * self.tile_size})"
        )
        # set sprite world position (in pixels)
        sprite.x = tx * self.tile_size
        sprite.y = ty * self.tile_size
        print(
            f"Placing sprite at random tile {key} ({tx}, {ty}) with xy ({sprite.x}, {sprite.y})"
        )

    def update(self) -> None:
        """Recompute screen positions for all sprites based on player camera."""
        if not self.player or not self.player_sprite:
            return
        # reposition all world objects
        for (tx, ty), sprite in self.objects.items():
            dx = tx * self.tile_size - self.player.world_x
            dy = ty * self.tile_size - self.player.world_y
            sprite.x = self.screen_center_x + dx
            sprite.y = self.screen_center_y + dy
        # center player sprite
        self.player_sprite.x = self.screen_center_x - self.player_sprite.width // 2
        self.player_sprite.y = self.screen_center_y - self.player_sprite.height // 2
