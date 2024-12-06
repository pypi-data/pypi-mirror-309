#!/usr/bin/env python3
"""peelee is one module to generate random palette and colors.

Example:
    python -m peelee.peelee -t 7 -T 7 -g 60 -G 60 -m 120 -M 20 -n 180 -N 40 -s 0.95  -S 0.95 -l 0.85 -L 0.85 -h 0.95 -H 0.95
"""
import getopt
import random
import sys
import typing
from enum import Enum

from loguru import logger

from peelee import color
from peelee.color import ColorName
from peelee.color_utils import bg, hex2hls, hex2rgb, hls2hex, rgb2hex
from peelee.random_color import SliceType, get_slice_colors

COLOR_RANGE_DENOMINATOR = 12


class PaletteMode(Enum):
    """Palette mode"""

    DARK = "D"
    LIGHT = "L"
    RANDOM = "A"


def get_scheme_colors(hex_color, n_colors=7):
    """
    Generate a list of n_colors triadic colors based on the given hex_color.

    Args:
        hex_color (str): The hexadecimal color code.
        n_colors (int): The number of triadic colors to generate. Default is 7.

    Returns:
        list: A list of n_colors triadic color codes.

    Raises:
        AssertionError: If hex_color is None or n_colors is not an integer
        greater than 0.
    """
    assert hex_color is not None, "Invalid argument: hex_color is None."
    assert (
        n_colors is not None and isinstance(n_colors, int) and n_colors > 0
    ), f"Invalid argument: n_colors = {n_colors}"
    hls_color = hex2hls(hex_color)
    triadic_colors = []
    for offset in range(0, 360, 360 // n_colors):
        triadic_colors.append(
            ((hls_color[0] + offset / 360) % 1.0, hls_color[1], hls_color[2])
        )
    base_colors = [hls2hex(hls_color) for hls_color in triadic_colors][0:n_colors]

    # the following line is to solve the deviation issue caused by
    # 360 //n_colors (e.g. if n_colors = 7, and base color is #130613,
    # then the base color would be changed to #130612.)
    base_colors.insert(1, hex_color)
    base_colors = base_colors[1:]

    # reverse the list to make sure the base color is the last - normally it
    # will be used as the main color of the workbench theme
    base_colors.reverse()
    return base_colors


def padding(num, target_length=2):
    """
    Padding left for number to make it's string format length reaches the
    target length.

    This is mainly used to construct valid hex color number in R,G,B
    position. Example, if the given num is a hex number 0xf and the
    target length is 2, then the padding result is 0f.
    """
    str_num = str(num)
    target_length = target_length if target_length and target_length > 2 else 2
    if str_num.startswith("0x"):
        str_num = str_num[2:]
    if len(str_num) < target_length:
        str_num = (
            f"{''.join(['0' for _ in range(target_length - len(str_num))])}{str_num}"
        )
    return str_num


def set_hue(hex_color, hue):
    """Set saturation."""
    if hue is None:
        return hex_color
    hls_color = hex2hls(hex_color)
    new_hls_color = (hue, hls_color[1], hls_color[2])
    return hls2hex(new_hls_color)


def set_saturation(hex_color, saturation):
    """Set saturation."""
    if saturation is None:
        return hex_color
    hls_color = hex2hls(hex_color)
    new_hls_color = (hls_color[0], hls_color[1], saturation)
    return hls2hex(new_hls_color)


def set_lightness(hex_color, lightness):
    """Set saturation."""
    if lightness is None:
        return hex_color
    hls_color = hex2hls(hex_color)
    new_hls_color = (hls_color[0], lightness, hls_color[2])
    return hls2hex(new_hls_color)


def set_hls_values(hex_color, hue, saturation, lightness):
    """Set saturation."""
    hls_color = hex2hls(hex_color)
    new_hls_color = (
        hue or hls_color[0],
        lightness or hls_color[1],
        saturation or hls_color[2],
    )
    return hls2hex(new_hls_color)


def generate_random_colors(
    min_color=0,
    max_color=231,
    colors_total=7,
    color_gradations=24,
    base_color_name=None,
    base_color=None,
    hue=None,
    saturation=None,
    lightness=None,
    palette_mode=PaletteMode.LIGHT,
):
    """
    Generate random color hex codes.

    Firstly, it will generate random integer from min_color (0-(255 - colors_gradations - 1)) to max_color (0-(255 - colors_gradations)).
    The max_color should be less than (255 - colors_gradations) because it needs the room to generate lighter colors.

    To generate darker colors, use smaller value for max_color.
    To generate ligher colors, use bigger value for min_color.

    It's recommended to use default values.
    If you want to make change, please make sure what you are doing.

    Secondly, it will generate 'colors_gradations' different hex color codes from base color to the lightest color.

        min_color - minimum color code. default: 0.
        max_color - maximum color code. default: 254 (cannot be bigger value).
        colors_total - how many base colors to generate. default: 7.
        color_gradations - how many lighter colors to generate. default: 24.
        base_color_name - color name. default: None. If None, then use random color name. it's used to generate the 'seed' random color which will be used to get more triadic colors.
        base_color - base color hex code. default: None. it has higher priority than base_color-name.
        saturation - saturation value to set for each base color. default: None.
        lightness - lightness value to set for each base color. default: None.

    Retrun:
        List of random colors list of each base color.
        The length of the outer list is colors_total, and the length of the inner list is color_gradations.
    """
    if color_gradations < 0 or color_gradations > 253:
        color_gradations = 24
    if min_color < 0 or min_color > (255 - color_gradations - 1):
        min_color = 0
    if max_color <= min_color or max_color >= (255 - color_gradations):
        max_color = 255 - color_gradations - 1
    # if base color is given, set hls values if they are given
    if base_color:
        base_color = set_hls_values(base_color, hue, saturation, lightness)
    random_color = base_color or generate_random_hex_color_code(
        min_color,
        max_color,
        color_name=base_color_name,
        hue=hue,
        saturation=saturation,
        lightness=lightness,
    )
    if palette_mode == PaletteMode.DARK:
        color_slice_type = SliceType.DARKER
    else:
        color_slice_type = SliceType.LIGHTER
    logger.debug(f"Random Color: {random_color}")
    base_colors = generate_base_colors(random_color, colors_total)
    logger.debug(f"Base Colors: {base_colors}")

    random_colors_list = []
    for _base_color in base_colors:
        slice_colors = get_slice_colors(_base_color, color_gradations, color_slice_type)
        random_colors_list.append(slice_colors)

    return random_colors_list

def generate_slice_colors(
    min_color=0,
    max_color=231,
    color_gradations=24,
    hue=None,
    saturation=None,
    lightness=None,
    palette_mode=PaletteMode.LIGHT
    ):
    """Generate slice colors for color names.

    In the ideal palette, except for random colors, we also need known colors.
    For example, to represents errors, we traditionally use red color, and for
    success or passed test results indicators, we use green color.

    This function will slice all known base colors defined in ColorName in
    color module and return a 2 dimentional list to present base known colors
    and their slided colors from light to dark.

    For each known base color name, it generate a random color code firstly,
    and then slice it to a series colors codes - total number is the value of
    color_gradations.

    The random color code of the base color is controlled by the parameters:
        min_color, max_color, color_name, hue, saturation, lightness
    Parameters:
    --------
    min_color: int
        RGB value from 0 to (255 - color_gradations - 1)
    max_color: int
        RGB value from min_color to (255 - color_gradations)
    color_gradations: int
        Total number of colors for the single base color
    hue: float
        Hue value for random base color
    saturation: float
        Saturation value for the random base color
    lightness: float
        Lightness value for the random base color
    palette_mode: PaletteMode
        LIGHT or DARK, to control how the sliced colors would be

    Return:
    --------
    typing.Mapping[ColorName, typing.List[str]]
        Mapping between ColorName and its sliced HEX colors codes

    See also:
    --------
    peelee#generate_random_hex_color_code
    random_color#get_slice_colors
    """
    if palette_mode == PaletteMode.DARK:
        color_slice_type = SliceType.DARKER
    else:
        color_slice_type = SliceType.LIGHTER
    random_colors_map = {}
    for base_color_name in ColorName:
        if base_color_name == ColorName.RANDOM:
            continue
        random_base_color = generate_random_hex_color_code(min_color,
                                                           max_color,
                                                           color_name=base_color_name,
                                                           hue=hue,
                                                           saturation=saturation,
                                                           lightness=lightness)
        logger.debug(f"random_base_color: {random_base_color}")
        logger.debug(f"converted random_base_color: {random_base_color}")
        slice_colors = get_slice_colors(random_base_color, color_gradations,
                                        color_slice_type)
        if palette_mode == PaletteMode.DARK:
            slice_colors.reverse()
        random_colors_map[base_color_name] = slice_colors

    # return random colors map
    return random_colors_map

def generate_random_hex_color_code(
    min_color,
    max_color,
    color_name: ColorName = None,
    hue=None,
    saturation=None,
    lightness=None,
):
    """
    Generates a list of base colors based on the given minimum and maximum
    color values and the total number of colors.

    Parameters:
    - min_color (int): The minimum value of the color range.
    - max_color (int): The maximum value of the color range.
    - total (int): The total number of base colors to generate.

    Returns:
    - base_colors (list): A list of base colors generated based on the given parameters.
    """
    hex_color_code_header = "#"
    random_hex_color_code = []

    # Old solution - only used for dark colors which needs dynamic colors.
    # By new solution, the dark color might be always the black color since
    # the max value is not big enough to have room to generate random colors
    # after divide by COLOR_RANGE_DENOMINATOR.
    # The old solution is usually used for workbench colors.
    diff = max_color - min_color
    if diff < COLOR_RANGE_DENOMINATOR:
        for index in range(0, 3):
            random_int = random.randint(min_color, max_color)
            _random_color = padding(hex(random_int))
            random_hex_color_code.append(_random_color)
    else:
        # New solution - 2023.12.19(Stockholm.Kungsängen.TibbleTorg) -in this
        # way, the generated colors are in the 'best' range and the theme
        # effection will be stable. The 'best' range will generate colors
        # that are comfortable for human eyes. E.g. #3c6464 or rgb(60,100,
        # 100). This is usually used for syntax(token) colors.
        step = diff // COLOR_RANGE_DENOMINATOR
        for index in range(
            1, COLOR_RANGE_DENOMINATOR, int(COLOR_RANGE_DENOMINATOR / 3.0)
        ):
            random_int = random.randint(
                min_color + (index * step), min_color + ((index + 2) * step)
            )
            _random_color = padding(hex(random_int))
            random_hex_color_code.append(_random_color)

    random_hex_color_code = sorted(random_hex_color_code)

    # By new solution, in default, the values of R,G,B is increased.
    # To generate the target color, need to swap the values of R,G,B
    if color_name is None or color_name == ColorName.RANDOM:
        color_name = random.choice(list(ColorName))
    # assume the color rgb is #223344
    random_int = random.randint(0, 255)
    if color_name == ColorName.RED:  # 442222 or 443333
        random_hex_color_code = swap_list(random_hex_color_code, 0, 2)
        if random_int % 2 == 0:
            random_hex_color_code[1] = random_hex_color_code[2]
        else:
            random_hex_color_code[2] = random_hex_color_code[1]
    elif color_name == ColorName.GREEN:  # 224422 or 334433
        random_hex_color_code = swap_list(random_hex_color_code, 1, 2)
        if random_int % 2 == 0:
            random_hex_color_code[2] = random_hex_color_code[0]
        else:
            random_hex_color_code[0] = random_hex_color_code[2]
    elif color_name == ColorName.YELLOW:  # 444422 or 444433
        random_hex_color_code = swap_list(random_hex_color_code, 0, 2)
        if random_int % 2 == 0:
            random_hex_color_code[1] = random_hex_color_code[0]
        else:
            random_hex_color_code[0] = random_hex_color_code[1]
    elif color_name == ColorName.CYAN:  # 224444 or 334444
        if random_int % 2 == 0:
            random_hex_color_code[1] = random_hex_color_code[2]
        else:
            random_hex_color_code = swap_list(random_hex_color_code, 0, 1)
            random_hex_color_code[1] = random_hex_color_code[2]
    elif color_name == ColorName.BLUE:  # 222244
        random_hex_color_code[1] = random_hex_color_code[0]
    elif color_name == ColorName.VIOLET:  # 442244 or 443344
        random_hex_color_code[0] = random_hex_color_code[2]
    elif color_name == ColorName.BLACK:  # 222222
        random_hex_color_code[1] = random_hex_color_code[0]
        random_hex_color_code[2] = random_hex_color_code[0]

    random_hex_color = hex_color_code_header + "".join(random_hex_color_code)
    if color_name == ColorName.VIOLET:
        # to have one grayish violet(magenta) color which is more proper
        # for the background color and human eyes
        random_rgb_color = hex2rgb(random_hex_color)
        random_rgb_color = (
            random_rgb_color[0],
            round(random_rgb_color[0] * 0.98),
            random_rgb_color[2],
        )
        random_hex_color = rgb2hex(random_rgb_color)
        
    # the given hue, saturation, and lightness might change the generated random color
    # which might not be expected. therefore, do not specify hue, saturation, and lightness unless you know what you are doing.
    if not isinstance(color_name, ColorName):
        random_hex_color = set_hls_values(
            random_hex_color, hue, saturation, lightness
        )

    return random_hex_color


def swap_list(_list, _from_index, _to_index):
    """Swap items in _from_index and _to_index in the list."""
    _tmp = _list[_from_index]
    _list[_from_index] = _list[_to_index]
    _list[_to_index] = _tmp
    return _list


def generate_base_colors(hex_color_code, total):
    """Generate base colors by the given hex color code and total number."""
    base_colors = get_scheme_colors(hex_color_code, total)[0:total]
    return base_colors


class Palette:
    """Generate palette colors."""

    def __init__(
        self,
        colors_total=7,
        colors_gradations=60,
        colors_min=120,
        colors_max=180,
        colors_saturation=0.35,
        colors_lightness=0.35,
        dark_colors_total=7,
        dark_colors_gradations_total=60,
        dark_colors_min=15,
        dark_colors_max=20,
        dark_colors_saturation=0.2,
        dark_colors_lightness=0.05,
        **kwargs,
    ):
        """
        Generate random palette.
        Parameters:
            colors_total: int
                how many base colors to generate. default: 5.
            colors_gradations: int
                how many lighter colors to generate. default: 6.
            colors_min: int
                the minimum color value in RGB
            colors_max: int
                the maximum color value in RGB
            colors_saturation: float
                saturation of the colors
            colors_lightness: float
                lightness of the colors
            dark_colors_total: int
                total of the dark base colors
            dark_colors_gradations_total: int
                gradations total of the dark base color
            dark_colors_min: int
                the minimum dark color value in RGB
            dark_colors_max: int
                the maximum dark color value in RGB
            dark_colors_saturation: float
                saturation of the dark colors
            dark_colors_lightness: float
                lightness of the dark colors

        Supported Keywords Parameters:
            dark_base_color_name: ColorName
                Base color name for dark color, it decides the dark colors
                generated. The given base dark color name is supposed to be used
                as background of the palette.
            dark_base_color: str
                The base color HEX value. The same purpose with
                `dark_base_color_name` but has higher priority than
                `dark_base_color_name`.
            palette_mode: PaletteMode
                The mode of the palette: PaletteMode.DARK or PaletteMode.LIGHT
                or PaletteMode.RANDOM
        """
        # random colors are used for sections, components, and pieces
        self.colors_total = colors_total
        self.colors_gradations = colors_gradations
        assert self.colors_total > 0, "colors_total must be greater than 0."
        assert self.colors_gradations > 0, "colors_gradations must be greater than 0."
        self.colors_min = colors_min
        self.colors_max = colors_max
        assert (
            self.colors_min <= self.colors_max
        ), "colors_min must be less than colors_max."
        self.colors_hue = kwargs.get("colors_hue", random.randint(0, 360) / 360)
        self.colors_saturation = colors_saturation
        self.colors_lightness = colors_lightness
        assert (
            self.colors_hue >= 0 and self.colors_hue <= 1
        ), "colors_hue must be greater than 0 and less than 1."
        assert (
            self.colors_saturation >= 0 and self.colors_saturation <= 1
        ), "colors_saturation must be greater than 0 and less than 1."
        assert (
            self.colors_lightness >= 0 and self.colors_lightness <= 1
        ), "colors_lightness must be greater than 0 and less than 1."

        self.dark_colors_total = dark_colors_total
        self.dark_colors_colors_gradations = dark_colors_gradations_total
        assert self.dark_colors_total > 0, "dark_colors_total must be greater than 0."
        assert (
            self.dark_colors_colors_gradations > 0
        ), "dark_colors_colors_gradations must be greater than 0."
        self.dark_colors_min = dark_colors_min
        self.dark_colors_max = dark_colors_max
        assert (
            self.dark_colors_min <= self.dark_colors_max
        ), "dark_colors_min must be less than dark_colors_max."
        self.dark_colors_hue = kwargs.get(
            "dark_colors_hue", random.randint(0, 360) / 360
        )
        self.dark_colors_saturation = dark_colors_saturation
        self.dark_colors_lightness = dark_colors_lightness
        if self.dark_colors_hue is not None:
            assert (
                self.dark_colors_hue >= 0 and self.dark_colors_hue <= 1
            ), "dark_colors_hue must be greater than 0 and less than 1."
        if self.dark_colors_saturation is not None:
            assert (
                self.dark_colors_saturation >= 0 and self.dark_colors_saturation <= 1
            ), "dark_colors_saturation must be greater than 0 and less than 1."
        if self.dark_colors_lightness is not None:
            assert (
                self.dark_colors_lightness >= 0 and self.dark_colors_lightness <= 1
            ), "dark_colors_lightness must be greater than 0 and less than 1."
        self.dark_base_color_name = kwargs.get("dark_base_color_name")
        if not any(member.name == self.dark_base_color_name for member in ColorName):
            self.dark_base_color_name = None
        else:
            self.dark_base_color_name = ColorName[self.dark_base_color_name]
        self.palette_mode = kwargs.get("palette_mode", "DARK")
        if not any(member.name == self.palette_mode for member in PaletteMode):
            self.palette_mode = None
        else:
            self.palette_mode = PaletteMode[self.palette_mode]
        self.dark_base_color = kwargs.get("dark_base_color", None)

    def generate_palette_colors(self):
        """
        Generate random palette.

        6 group base colors: 5 base colors + dark gray color. echo base
        color has 6 different colors from dark to light. placeholders
        are from light to dark, so need to reverse the order.
        """
        colors_list = []
        normal_colors = generate_random_colors(
            min_color=self.colors_min,
            max_color=self.colors_max,
            colors_total=self.colors_total,
            color_gradations=self.colors_gradations,
            hue=self.colors_hue,
            saturation=self.colors_saturation,
            lightness=self.colors_lightness,
        )
        if self.palette_mode == PaletteMode.LIGHT:
            for r_colors in normal_colors:
                r_colors.reverse()
        colors_list.extend(normal_colors)

        dark_colors = generate_random_colors(
            min_color=self.dark_colors_min,
            max_color=self.dark_colors_max,
            colors_total=self.dark_colors_total,
            color_gradations=self.dark_colors_colors_gradations,
            base_color_name=self.dark_base_color_name,
            base_color=self.dark_base_color,
            hue=self.dark_colors_hue,
            saturation=self.dark_colors_saturation,
            lightness=self.dark_colors_lightness,
        )

        if self.palette_mode == PaletteMode.DARK:
            for r_colors in dark_colors:
                r_colors.reverse()
        colors_list.extend(dark_colors)
        return [color for r_colors in colors_list for color in r_colors]

    def generate_slice_colors(self):
        """Return light slice colors and dark slice colors.

        Returns:
        --------
        typing.Mapping[PaletteMode, typing[Mapping[ColorName,
        typing.List[str]]]]
        Map of palette_mode and the slice colors map
        """

        # from light to dark
        light_slice_colors = generate_slice_colors(
                min_color=self.colors_min,
                max_color=self.colors_max,
                color_gradations=self.colors_gradations,
                hue=self.colors_hue,
                saturation=self.colors_saturation,
                lightness=self.colors_lightness,
                palette_mode=PaletteMode.DARK
                )

        # from dark to light
        dark_slice_colors = generate_slice_colors(
                min_color=self.dark_colors_min,
                max_color=self.dark_colors_max,
                color_gradations=self.dark_colors_colors_gradations,
                hue=self.dark_colors_hue,
                saturation=self.dark_colors_saturation,
                lightness=self.dark_colors_lightness,
                palette_mode=PaletteMode.LIGHT
                )
        return {PaletteMode.LIGHT: light_slice_colors, PaletteMode.DARK: dark_slice_colors} 


    def generate_palette(self):
        """
        Generate palette content.

        Palette contains a list of colors. Each color is a pair of color
        name and color code.
        The format is "C_[base color sequence]_[colormap sequence]".

        For example, "C_1_1":"#8f67ff".

        Note:
        The 'base color sequence' starts from 1 to base_colors_total (not
        included)
        The 'colormap sequence' starts from 0 to colors_gradations (not
        included)
        When "colormap sequence" is 0, then it represents the lightest color.

        One continuous colormap is for one base color and consists of a
        group of colors from lightest color to the base color.

        Return:
            A list of palette colors which consists of two sections: the base section and the dark section.
        """
        palette_color_codes = self.generate_palette_colors()
        color_sequence = 1
        sub_color_sequence = 0
        palette_colors = {}
        colors_gradations = self.colors_gradations
        for index, color in enumerate(palette_color_codes):
            sub_color_sequence = index % (self.colors_gradations)
            # the remaining colors codes belong to dark colors
            if color_sequence > self.colors_total:
                colors_gradations = self.dark_colors_colors_gradations
                sub_color_sequence = (
                    index - (self.colors_total * self.colors_gradations)
                ) % (self.dark_colors_colors_gradations)
            str_base_color_sequence = padding(
                color_sequence, max(len(str(self.colors_total)), 2)
            )
            str_colormap_sequence = padding(
                sub_color_sequence, max(len(str(colors_gradations)), 2)
            )
            color_name = f"C_{str_base_color_sequence}_{str_colormap_sequence}"
            palette_colors[color_name] = color
            if sub_color_sequence == colors_gradations - 1:
                color_sequence += 1

        slice_colors = self.generate_slice_colors()
        for palette_mode, slice_color_map in slice_colors.items():
            for color_name, color_codes in slice_color_map.items():
                color_codes_total = len(color_codes)
                for index, color in enumerate(color_codes):
                    color_index = padding(index, max(len(str(color_codes_total)), 2))
                    palette_colors[f"{palette_mode.value}_{color_name.value}_{color_index}"] = color
        return palette_colors


def generate_palette():
    """Generate palette colors."""
    return Palette().generate_palette()


def generate_palette_plain_text():
    """Generate random palette."""
    palette = generate_palette()
    return "\n".join([f"{color_name}:{color}" for color_name, color in palette.items()])

def main():
    """Test."""
    opts, _ = getopt.getopt(
        sys.argv[1:],
        "t:g:m:n:h:s:l:T:G:M:N:H:S:L:b:B:p:",
        [
            "--colors_total=",
            "--colors_gradations=",
            "--colors_min=",
            "--colors_max=",
            "--colors_hue=",
            "--colors_saturation=",
            "--colors_lightness=",
            "--dark_colors_total=",
            "--dark_colors_gradations=",
            "--dark_colors_min=",
            "--dark_colors_max=",
            "--dark_colors_hue=",
            "--dark_colors_saturation=",
            "--dark_colors_lightness=",
            "--dark_base_color_name=",
            "--dark_base_color=",
            "--palette_mode=",
        ],
    )
    colors_total = 7
    colors_gradations = 60
    colors_min=120
    colors_max=180
    colors_hue=0.95
    colors_saturation=0.95
    colors_lightness=0.85

    dark_colors_total=7
    dark_colors_gradations = 60
    dark_colors_min=15
    dark_colors_max=40
    dark_colors_hue=0.95
    dark_colors_saturation=0.95
    dark_colors_lightness=0.85

    dark_base_color_name=None
    dark_base_color = None
    palette_mode = PaletteMode.DARK.name
    for option, value in opts:
        if option in ("-t", "--colors_total"):
            colors_total = int(value)
        if option in ("-g", "--colors_gradations"):
            colors_gradations = int(value)
        if option in ("-m", "--colors_min"):
            colors_min = int(value) 
        if option in ("-n", "--colors_max"):
            colors_max = int(value)
        if option in ("-h", "--colors_hue"):
            colors_hue = float(value)
        if option in ("-s", "--colors_saturation"):
            colors_saturation = float(value)
        if option in ("-l", "--colors_lightness"):
            colors_lightness = float(value)
        if option in ("-T", "--dark_colors_total"):
            dark_colors_total = int(value)
        if option in ("-G", "--dark_colors_gradations_total"):
            dark_colors_gradations = int(value)
        if option in ("-M", "--dark_colors_min"):
            dark_colors_min = int(value) 
        if option in ("-N", "--dark_colors_max"):
            dark_colors_max = int(value) 
        if option in ("-H", "--dark_colors_hue"):
            dark_colors_hue = float(value)
        if option in ("-S", "--dark_colors_saturation:"):
            dark_colors_saturation = float(value)
        if option in ("-L", "--dark_colors_lightness:"):
            dark_colors_lightness = float(value)
        if option in ("-b", "--dark_base_color_name"):
            dark_base_color_name= value.upper()
        if option in ("-B", "--dark_base_color"):
            dark_base_color=value
        if option in ("-p", "--palette_mode"):
            palette_mode = value.upper()
    palette = Palette(
        colors_total=colors_total,
        colors_gradations=colors_gradations,
        colors_min=colors_min,
        colors_max=colors_max,
        colors_saturation=colors_saturation,
        colors_lightness=colors_lightness,
        dark_colors_total=dark_colors_total,
        dark_colors_gradations_total=dark_colors_gradations,
        dark_colors_min=dark_colors_min,
        dark_colors_max=dark_colors_max,
        dark_colors_saturation=dark_colors_saturation,
        dark_colors_lightness=dark_colors_lightness,
        dark_base_color_nam=dark_base_color_name,
        dark_base_color=dark_base_color,
        palette_mode=palette_mode,
    )
    for color_id, color_hex in palette.generate_palette().items():
        logger.info(bg(color_hex, f"{color_id}({color_hex})"))


if __name__ == "__main__":
    main()
