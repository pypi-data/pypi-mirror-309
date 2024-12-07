from epicure.collection.colors import BG_COLOR_CODES, FG_COLOR_CODES, RESET_COLOR_CODE


def colored_print(
    text: str, fg_color: str | None = None, bg_color: str | None = None, end: str = "\n"
) -> None:
    """
    Print text in the specified foreground and background colors.

    :param text: The text to print.
    :type text: str
    :param fg_color: The foreground color to print the text in.
    :type fg_color: str
    :param bg_color: The background color to print the text in.
    :type bg_color: str
    :param end: The string to print at the end of the text.
    :type end: str

    :return: None
    :rtype: None

    :examples:
        >>> colored_print("Hello, world!", fg_color="red", bg_color="black")
        Hello, world!  # In red text on a black background.

        >>> colored_print("Hello, world!", fg_color="red")
        Hello, world!  # In red text, default background.


    """
    fg_code = FG_COLOR_CODES.get(fg_color, "")
    bg_code = BG_COLOR_CODES.get(bg_color, "")

    if fg_code and bg_code:
        print(f"\033[{fg_code};{bg_code}m{text}\033[{RESET_COLOR_CODE}m", end=end)
    elif fg_code:
        print(f"\033[{fg_code}m{text}\033[{RESET_COLOR_CODE}m", end=end)
    elif bg_code:
        print(f"\033[{bg_code}m{text}\033[{RESET_COLOR_CODE}m", end=end)
    else:
        print(text, end=end)
