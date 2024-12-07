from .ansi_styles import ANSI_STYLES as _ANSI_STYLES
from .format import get_rgb_from_hexa as _get_rgb_from_hexa


def deactivate(do_warning: bool = True):
    """
    Deactivate stylisation, every functions remains active but useless (remove all previous stylisation)
    """
    global _is_activated

    if do_warning: print(rgb('WARNING: stylisation is now deactivated', rgb=(252, 186, 3)))
    # redefined constant to cancel its
    for style_, value in _ANSI_STYLES.items():
        # constants
        globals()[style_.upper()] = str()
    _is_activated = False


def reactivate(do_warning: bool = True):
    """
    Reactivate stylisation every function are back
    """
    global _is_activated

    _is_activated = True
    # redefine constants
    for style_, value in _ANSI_STYLES.items():
        # constants
        globals()[style_.upper()] = f"\033[{value}m"

    if do_warning: print(styles('INFO: stylisation is now reactivated', _ANSI_STYLES['yellow']))


def raw(*values: object, sep: str=' ') -> str:
    """
    Give raw stylised values.
    :param values: stylised objects
    :param sep: Separator for concatenated text objects.
    :return: raw stylised string
    """
    return sep.join([str(value) for value in values]).replace("\033", "\\033")

def rprint(*values: object, sep=' '):
    """
    print raw stylised values
    :param values: stylised objects
    :param sep: Separator for concatenated text objects.

    """
    print(raw(*values, sep=sep))

def _extract_styles(text: str) -> list:
    """
    Extract ANSI style codes from a styled text.
    :param text: ANSI-styled text.
    :return: List of extracted style codes.
    """
    if not text.startswith('\033['):
        return []
    style_end = text.find('m')
    style_codes = text[2:style_end].split(';')
    return style_codes


def _remove_styles(text: str) -> str:
    """
    Remove ANSI style codes from a styled text.
    :param text: ANSI-styled text.
    :return: Unstyled text.
    """
    style_end = text.find('m')
    text = text[style_end + 1:]  # Skip past the 'm'
    if text.endswith('\033[0m'):
        text = text[:-4]  # Remove trailing reset sequence
    return text


def styles(value: object, *styles: str | int) -> str:
    """
    Apply multiple ANSI styles to a text.
    :param value: object to style.
    :param styles: Style codes or names to apply.
    :return: Styled text.
    """
    text = str(value)
    if not styles:
        return text

    # Convert style names to codes or use as-is if numeric
    style_codes = [str(_ANSI_STYLES.get(s, s)) for s in styles]

    # Construct the ANSI escape sequence
    style_sequence = ';'.join(style_codes)

    # Split text by existing styles (if any) and apply new styles
    segments = text.split('\033[')
    styled_text = str()

    # test if activation is in False:
    if not _is_activated:
        return ''.join([_remove_styles(segment) for segment in segments])

    if segments[0]:  # Handle unstyled initial segment
        styled_text += f"\033[0;{style_sequence}m{segments[0]}"
    for segment in segments[1:]:
        style_end = segment.find('m')
        existing_styles = segment[:style_end].split(';')# if style_end != -1 else []
        unstyled_text = segment[style_end + 1:]# if style_end != -1 else segment
        combined_styles = ';'.join(existing_styles + style_codes)
        styled_text += f"\033[{combined_styles}m{unstyled_text}"
    return styled_text + '\033[0m'  # Ensure final reset


def style(*values: object, style: str | int, sep: str = ' ') -> str:
    """
    Apply a single ANSI style to multiple texts.
    :param values: objects to style (convert into str).
    :param style: Style code or name to apply.
    :param sep: Separator for concatenated text objects.
    :return: Styled text.
    """
    texts = [str(object) for object in values]
    return styles(sep.join(texts), style)


def rgb(*values: object, r: int = int(), g: int = int(), b: int = int(), rgb: tuple[int,int, int] = tuple(), sep: str= ' ') -> str:
    """
    Apply foreground rgb color style to a multiple texts.
    :param values: objects to style.
    :param r: Red color value.
    :param g: green color value.
    :param b: blue color value.
    :param rgb: [Optional] rgb color, to use instead of r, g, b.
    :param sep: Separator for concatenated texts objects.
    :return: Styled text.
    """
    if rgb:
        if len(rgb) != 3:
            raise ValueError(f'len of rgb must be 3 (R, G, B), (value: {rgb})')
        r,g,b = rgb

    if not all(0 <= color <= 255 for color in (r, g, b)):
        raise ValueError(f'r, g and b must be in the range of 0 to 255 (values: r: {r}, g: {g}, b: {b})')

    return styles(sep.join([str(obj) for obj in values]), 38, 2, r, g, b)


def brgb(*values: object, r: int = int(), g: int = int(), b: int = int(), rgb: tuple[int,int, int] = tuple(), sep: str= ' ') -> str:
    """
    Apply background rgb color style to a multiple texts.
    :param values: objects to style.
    :param r: Red color value.
    :param g: green color value.
    :param b: blue color value.
    :param rgb: [Optional] rgb color, to use instead of r, g, b.
    :param sep: Separator for concatenated texts objects.
    :return: Styled text.
    """
    if rgb:
        if len(rgb) != 3:
            raise ValueError(f'len of rgb must be 3 (R, G, B), (value: {rgb})')
        r,g,b = rgb

    if not all(0 <= color <= 255 for color in (r, g, b)):
        raise ValueError(f'r, g and b must be in the range of 0 to 255 (values: r: {r}, g: {g}, b: {b})')

    return styles(sep.join([str(obj) for obj in values]), 48, 2, r, g, b)


def hexa(*values: object, hexa: str, sep=' ') -> str:
    """
    Apply foreground hexadecimal color style to multimple texts
    :param values: objects to style.
    :param hexa: hexadecimal color code, start or not with '#'.
    :param sep: Separator for concatenated texts objects.
    :return: Styled text
    """
    return rgb(*values, rgb=_get_rgb_from_hexa(hexa), sep=sep)


def bhexa(*values: object, hexa: str, sep=' ') -> str:
    """
    Apply background hexadecimal color style to multimple texts
    :param values: objects to style.
    :param hexa: hexadecimal color code, start or not with '#'.
    :param sep: Separator for concatenated texts objects.
    :return: Styled text
    """
    return brgb(*values, rgb=_get_rgb_from_hexa(hexa), sep=sep)


_is_activated = True

# create a function for every style and color contains in _ANSI_STYLES
# e.g.: stylorize.blue(), stylorize.underline()
# also create a constant for every style and color, is the ANSI code
# e.g. stylorize.BLUE, stylorize.UNDERLINE
for style_, value in _ANSI_STYLES.items():
    # functions
    globals()[style_] = lambda *objects, sep= ' ', _=style_: style(*objects, style=_, sep=sep)
    # constants
    globals()[style_.upper()] = f"\033[{value}m"
