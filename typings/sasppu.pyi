from typing import Optional, Union, TypeAlias

# Type aliases for clarity
Color: TypeAlias = int
Coordinate: TypeAlias = int
Dimension: TypeAlias = int
ResultCode: TypeAlias = int
Text: TypeAlias = str
Palette: TypeAlias = bytes
Data: TypeAlias = Union[bytes, bytearray]

# Color manipulation macros
def grey555(g: int) -> Color: ...
def grey555_cmath(g: int) -> Color: ...
def rgb555(r: int, g: int, b: int) -> Color: ...
def rgb555_cmath(r: int, g: int, b: int) -> Color: ...
def rgb888(r: int, g: int, b: int) -> Color: ...
def rgb888_cmath(r: int, g: int, b: int) -> Color: ...
def mul_rgb555(r: int, g: int, b: int, mul: int) -> Color: ...
def mul_col(col: Color, mul: int) -> Color: ...
def r_channel(col: Color) -> int: ...
def g_channel(col: Color) -> int: ...
def b_channel(col: Color) -> int: ...
def cmath_channel(col: Color) -> int: ...

# Predefined colors
TRANSPARENT_BLACK: Color
OPAQUE_BLACK: Color
RED: Color
GREEN: Color
BLUE: Color
WHITE: Color

# Image codes
class ImageCode:
    Success: ResultCode
    TooWide: ResultCode
    TooTall: ResultCode
    InvalidBitdepth: ResultCode

# Function signatures
def copy_sprite(
    dst_x: Coordinate,
    dst_y: Coordinate,
    width: Dimension,
    height: Dimension,
    src_x: Coordinate,
    src_y: Coordinate,
    double_size: bool = False,
) -> ResultCode: ...
def copy_sprite_transparent(
    dst_x: Coordinate,
    dst_y: Coordinate,
    width: Dimension,
    height: Dimension,
    src_x: Coordinate,
    src_y: Coordinate,
    double_size: bool = False,
) -> ResultCode: ...
def fill_sprite(
    x: Coordinate, y: Coordinate, width: Dimension, height: Dimension, colour: Color
) -> ResultCode: ...
def draw_text_sprite(
    x: Coordinate,
    y: Coordinate,
    colour: Color,
    line_width: Dimension,
    text: Text,
    double_size: bool = False,
    newline_height: Dimension = 10,
) -> ResultCode: ...
def draw_text_next_sprite(
    x: Coordinate,
    y: Coordinate,
    colour: Color,
    line_start: int,
    line_width: Dimension,
    text: Text,
    double_size: bool = False,
    newline_height: Dimension = 10,
) -> tuple[ResultCode, Coordinate, Coordinate]: ...
def blit_sprite(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def blit_sprite_transparent(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def paletted_sprite(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def paletted_sprite_transparent(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def compressed_sprite(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def compressed_sprite_transparent(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def copy_background(
    dst_x: Coordinate,
    dst_y: Coordinate,
    width: Dimension,
    height: Dimension,
    src_x: Coordinate,
    src_y: Coordinate,
    double_size: bool = False,
) -> ResultCode: ...
def copy_background_transparent(
    dst_x: Coordinate,
    dst_y: Coordinate,
    width: Dimension,
    height: Dimension,
    src_x: Coordinate,
    src_y: Coordinate,
    double_size: bool = False,
) -> ResultCode: ...
def fill_background(
    x: Coordinate, y: Coordinate, width: Dimension, height: Dimension, colour: Color
) -> ResultCode: ...
def draw_text_background(
    x: Coordinate,
    y: Coordinate,
    colour: Color,
    line_width: Dimension,
    text: Text,
    double_size: bool = False,
    newline_height: Dimension = 10,
) -> ResultCode: ...
def draw_text_next_background(
    x: Coordinate,
    y: Coordinate,
    colour: Color,
    line_start: int,
    line_width: Dimension,
    text: Text,
    double_size: bool = False,
    newline_height: Dimension = 10,
) -> tuple[ResultCode, Coordinate, Coordinate]: ...
def blit_background(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def blit_background_transparent(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def paletted_background(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def paletted_background_transparent(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def compressed_background(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def compressed_background_transparent(
    x: Coordinate,
    y: Coordinate,
    width: Dimension,
    height: Dimension,
    palette: Palette,
    bitdepth: int,
    data: Data,
    double_size: bool = False,
) -> ResultCode: ...
def get_text_size(
    line_width: Dimension,
    text: Text,
    double_size: bool = False,
    newline_height: Dimension = 10,
) -> tuple[Dimension, Dimension]: ...
def gfx_reset() -> None: ...
def macro_cmath(col: Color) -> ResultCode: ...
def macro_rgb555(r: int, g: int, b: int) -> ResultCode: ...
def macro_rgb555_cmath(r: int, g: int, b: int) -> ResultCode: ...
def macro_rgb888(r: int, g: int, b: int) -> ResultCode: ...
def macro_rgb888_cmath(r: int, g: int, b: int) -> ResultCode: ...
def macro_grey555(g: int) -> ResultCode: ...
def macro_grey555_cmath(g: int) -> ResultCode: ...
def macro_mul_channel(col: Color, mul: int) -> ResultCode: ...
def macro_mul_rgb555(r: int, g: int, b: int, mul: int) -> ResultCode: ...
def macro_r_channel(col: Color) -> ResultCode: ...
def macro_g_channel(col: Color) -> ResultCode: ...
def macro_b_channel(col: Color) -> ResultCode: ...
def macro_cmath_channel(col: Color) -> ResultCode: ...
def macro_mul_col(col: Color, mul: int) -> ResultCode: ...

# Predefined constants
SPRITE_COUNT: int
SPRITE_CACHE: int
MAP_WIDTH: int
MAP_HEIGHT: int
MAP_WIDTH_POWER: int
MAP_HEIGHT_POWER: int

# Window masks
WINDOW_A: int
WINDOW_B: int
WINDOW_AB: int
WINDOW_X: int
WINDOW_ALL: int

# Bit depth definitions
BPP1: int
BPP2: int
BPP4: int
BPP8: int

# Flags
ENABLED: int
PRIORITY: int
FLIP_X: int
FLIP_Y: int
C_MATH: int
DOUBLE: int

# Classes and objects
class Background:
    x: Coordinate
    y: Coordinate
    windows: int
    window_1: int
    window_2: int
    flags: int

    def bind(self, bind_point: int, flush: bool = True) -> None: ...
    def unbind(self) -> None: ...
    def get_bind_point(self) -> Optional[int]: ...

class Sprite:
    x: Coordinate
    y: Coordinate
    width: Dimension
    height: Dimension
    graphics_x: Coordinate
    graphics_y: Coordinate
    windows: int
    window_1: int
    window_2: int
    flags: int

    def bind(self, bind_point: int, flush: bool = True) -> None: ...
    def unbind(self) -> None: ...
    def get_bind_point(self) -> Optional[int]: ...

class CMathState:
    fade: int
    flags: int

    def bind(self, flush: bool = True) -> None: ...
    def unbind(self) -> None: ...
    def get_bind_point(self) -> bool: ...

class MainState:
    mainscreen_colour: Color
    subscreen_colour: Color
    window_1_left: int
    window_1_right: int
    window_2_left: int
    window_2_right: int
    bgcol_windows: int
    bgcol_window_1: int
    bgcol_window_2: int
    flags: int

    def bind(self, flush: bool = True) -> None: ...
    def unbind(self) -> None: ...
    def get_bind_point(self) -> bool: ...

class OAM:
    def __getitem__(self, index: int) -> Sprite: ...
    def __setitem__(self, index: int, value: Sprite) -> None: ...
    def __len__(self) -> int: ...

class MAP:
    def __getitem__(self, index: int) -> int: ...
    def __setitem__(self, index: int, value: int) -> None: ...
    def __len__(self) -> int: ...

class HDMA:
    def __getitem__(self, index: int) -> Optional[
        Union[
            None,
            bool,
            MainState,
            CMathState,
            tuple[int, Sprite],
            tuple[int, Background],
        ]
    ]: ...
    def __setitem__(
        self,
        index: int,
        value: Optional[
            Union[
                None,
                bool,
                MainState,
                CMathState,
                tuple[int, Background],
                tuple[int, Sprite],
            ]
        ],
    ) -> None: ...
    def __len__(self) -> int: ...

# Module-level objects
oam: OAM
bg0: MAP
bg1: MAP
hdma_0: HDMA
hdma_1: HDMA
hdma_2: HDMA
hdma_3: HDMA
hdma_4: HDMA
hdma_5: HDMA
hdma_6: HDMA
hdma_7: HDMA
hdma_enable: int
