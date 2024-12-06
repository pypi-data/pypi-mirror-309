from epicure.collection.colors import BG_COLOR_CODES, FG_COLOR_CODES, RESET_COLOR_CODE


def colored_print(
    text: str, fg_color: str | None = None, bg_color: str | None = None, end: str = "\n"
) -> None:
    """
    Print text in the specified foreground and background colors.

    Parameters:
    - text (str): The text to print.
    - fg_color (str): The foreground color to print the text in.
    - bg_color (str): The background color to print the text in.
    - end (str): The string to print at the end of the text.

    Returns:
    - None
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
