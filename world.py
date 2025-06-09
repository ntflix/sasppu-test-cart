from sasppu import Sprite
from .player import Player


class World:
    """
    World handles positioning of game objects relative to the player (camera).
    Coordinates are in pixels. The world is tile-based, with tile_size defining the grid.
    """

    def __init__(self, tile_size: int, screen_width: int, screen_height: int):
        self.tile_size = tile_size
        self.screen_center_x = screen_width // 2
        self.screen_center_y = screen_height // 2
        self.player: Player | None = None
        self.player_sprite: Sprite | None = None
        # map from (tile_x, tile_y) to sprite
        self.objects: dict[tuple[int, int], Sprite] = {}

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
