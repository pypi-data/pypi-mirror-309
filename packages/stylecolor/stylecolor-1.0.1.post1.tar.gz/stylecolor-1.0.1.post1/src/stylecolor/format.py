def get_rgb_from_hexa(hexa: str) -> tuple[int, int, int]:
    """
    convert hexadecimal color into RGB color
    :param hexa: hexadecimal color
    :return: r, g, b value
    """
    # convert hexa into upper chars
    hexa = hexa.upper()

    # checking format
    # eventually remove "#" at first char
    hexa = hexa[1:] if hexa.startswith('#') else hexa
    if len(hexa) != 6:
        raise ValueError(f"hexadecimal color must have a length of 6 (without '#') (length: {len(hexa)})")
    if not all(char in HEXA_CHARS for char in hexa):
        raise ValueError(
            f'hexa must be a combination of the 10 numbers and the 5 firsts letters (A to F), (value: {hexa})')

    # extract r,g, b value
    r = int(hexa[0:2], 16)  # First two characters represent Red
    g = int(hexa[2:4], 16)  # Middle two characters represent Green
    b = int(hexa[4:6], 16)  # Final two characters represent Blue
    return r, g, b



HEXA_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
