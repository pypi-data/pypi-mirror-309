import curses

from epicure.collection.colors import CURSES_COLOR_MAP
from epicure.output import colored_print


def ask_yes_no_question(
    prompt: str,
    default: str = "yes",
    case_sensitive: bool = False,
    prompt_fg_color: str | None = None,
    prompt_bg_color: str | None = None,
    error_message: str = "Please respond with 'yes' or 'no' (or 'y' or 'n').",
) -> bool:
    """
    Ask the user a yes/no question.

    :param prompt: The question to ask the user.
    :type prompt: str
    :param default: The default answer if the user just presses Enter.
    :type default: str
    :param case_sensitive: Whether the response should be case-sensitive.
    :type case_sensitive: bool
    :param prompt_fg_color: The foreground color of the prompt text.
    :type prompt_fg_color: str
    :param prompt_bg_color: The background color of the prompt text.
    :type prompt_bg_color: str
    :param error_message: The message to display if the user enters an invalid response.
    :type error_message: str

    :return: 'True' if the user answers 'yes', 'False' if the user answers 'no'.
    :rtype: bool

    :raises:
        ValueError: If the default parameter is neither "yes" nor "no".

    :examples:
        >>> result = ask_yes_no_question("Do you want to proceed?")
        Do you want to proceed? [Y/n]: yes
        >>> print(result)
        True

        >>> result = ask_yes_no_question("Continue?", default="no")
        Continue? [y/N]: n
        >>> print(result)
        False

        >>> result = ask_yes_no_question("Continue?", case_sensitive=True)
        Continue? [Y/n]: Y
        >>> print(result)
        True

        >>> result = ask_yes_no_question("Continue?", default="maybe")
        Traceback (most recent call last):
        ...
        ValueError: Invalid default answer. Must be 'yes' or 'no'.

        >>> result = ask_yes_no_question("Continue?", error_message="Invalid response.")
        Continue? [Y/n]: maybe
        Invalid response.
        Continue? [Y/n]:
    """

    valid_yes = ["yes", "y"]
    valid_no = ["no", "n"]

    if default not in valid_yes + valid_no:
        raise ValueError("Invalid default answer. Must be 'yes' or 'no'.")

    default_prompt = " [Y/n]" if default in valid_yes else " [y/N]"
    full_prompt = f"{prompt}{default_prompt}:"

    while True:
        colored_print(
            full_prompt, fg_color=prompt_fg_color, bg_color=prompt_bg_color, end=" "
        )

        response = input().strip()
        if not response:
            response = default

        if not case_sensitive:
            response = response.lower()

        if response in valid_yes:
            return True
        elif response in valid_no:
            return False

        colored_print(error_message, fg_color="red", bg_color="black")


def simple_choice_question(
    prompt: str,
    choices: list,
    prompt_fg_color: str | None = None,
    prompt_bg_color: str | None = None,
) -> str:
    """
    Ask the user to choose one option from a list of choices.

    :param prompt: The question to ask the user.
    :type prompt: str
    :param choices: The list of choices to present to the user.
    :type choices: list
    :param prompt_fg_color: The foreground color of the prompt text.
    :type prompt_fg_color: str
    :param prompt_bg_color: The background color of the prompt text.
    :type prompt_bg_color: str

    :return: The chosen option.
    :rtype: str

    :examples:
        >>> result = simple_choice_question("Choose a color:", ["red", "green", "blue"])
        Choose a color:
        1. red
        2. green
        3. blue
        Enter the number of your choice: 2
        >>> print(result)
        "green"

        >>> result = simple_choice_question("Choose a color:", ["red", "green", "blue"])
        Choose a color:
        1. red
        2. green
        3. blue
        Enter the number of your choice: 4
        Invalid choice. Please enter a number corresponding to one of the options.
        Enter the number of your choice: 1
        >>> print(result)
        "red"
    """
    while True:
        colored_print(prompt, fg_color=prompt_fg_color, bg_color=prompt_bg_color)
        for i, choice in enumerate(choices, 1):
            colored_print(f"{i}. {choice}", fg_color="green")

        response = input("Enter the number of your choice: ").strip()
        if response.isdigit() and 1 <= int(response) <= len(choices):
            return choices[int(response) - 1]

        print(
            "Invalid choice. Please enter a number corresponding to one of the options."
        )


def multi_choice_question(
    prompt: str,
    choices: list,
    prompt_fg_color: str | None = None,
    prompt_bg_color: str | None = None,
) -> list:
    """
    Ask the user to choose multiple options from a list of choices.

    :param prompt: The question to ask the user.
    :type prompt: str
    :param choices: The list of choices to present to the user.
    :type choices: list
    :param prompt_fg_color: The foreground color of the prompt text.
    :type prompt_fg_color: str
    :param prompt_bg_color: The background color of the prompt text.
    :type prompt_bg_color: str
    :return: The list of chosen options.
    :rtype: list

    :examples:
        >>> result = multi_choice_question_interactive(
        ...     "Choose your favorite colors:",
        ...     ["red", "green", "blue"]
        ... )
        Choose your favorite colors:
        1. red
        2. green
        3. blue
        Enter the number of your choice (or press Enter to finish): 2
        1. red
        2. green [x]
        3. blue
        Enter the number of your choice (or press Enter to finish): 3
        1. red
        2. green [x]
        3. blue [x]
        Enter the number of your choice (or press Enter to finish):
        >>> print(result)
        ["green", "blue"]

        >>> result = multi_choice_question_interactive(
        ...     "Choose your favorite colors:",
        ...     ["red", "green", "blue"]
        ... )
        Choose your favorite colors:
        1. red
        2. green
        3. blue
        Enter the number of your choice (or press Enter to finish): 4
        Invalid choice.
        Please enter a number corresponding to one of the options.
        Enter the number of your choice (or press Enter to finish): 2
        1. red
        2. green [x]
        3. blue
        Enter the number of your choice (or press Enter to finish): 2
        1. red
        2. green [x]
        3. blue [x]
        Enter the number of your choice (or press Enter to finish):
    """
    selected_choices = []
    while True:
        colored_print(prompt, fg_color=prompt_fg_color, bg_color=prompt_bg_color)
        for i, choice in enumerate(choices, 1):
            selected = " [x]" if choice in selected_choices else ""
            colored_print(f"{i}. {choice}", fg_color="green", end="")
            colored_print(selected, fg_color="yellow", bg_color="black")

        response = input(
            "Enter the number of your choice (or press Enter to finish): "
        ).strip()
        if not response:
            return selected_choices

        if response.isdigit() and 1 <= int(response) <= len(choices):
            choice = choices[int(response) - 1]
            if choice in selected_choices:
                selected_choices.remove(choice)
            else:
                selected_choices.append(choice)
        else:
            print(
                "Invalid choice.\n"
                "Please enter a number corresponding to one of the options."
            )


def multi_choice_question_interactive(
    prompt: str,
    choices: list,
    prompt_fg_color: str = "white",
    prompt_bg_color: str = "black",
    option_fg_color: str = "white",
    option_bg_color: str = "black",
    hover_fg_color: str = "black",
    hover_bg_color: str = "white",
    selected_indicator_fg_color: str = "white",
    selected_indicator_bg_color: str = "black",
) -> list:
    """
    Ask the user to choose multiple options from a list of choices using an interactive
    menu.

    Parameters:

    :param prompt: The question to ask the user.
    :type prompt: str
    :param choices: The list of choices to present to the user.
    :type choices: list
    :param prompt_fg_color: The foreground color of the prompt text.
    :type prompt_fg_color: str
    :param prompt_bg_color: The background color of the prompt text.
    :type prompt_bg_color: str
    :param option_fg_color: The foreground color of the options.
    :type option_fg_color: str
    :param option_bg_color: The background color of the options.
    :type option_bg_color: str
    :param hover_fg_color: The foreground color of the hovered option.
    :type hover_fg_color: str
    :param hover_bg_color: The background color of the hovered option.
    :type hover_bg_color: str
    :param selected_indicator_fg_color: The foreground color of the selected options.
    :type selected_indicator_fg_color: str
    :param selected_indicator_bg_color: The background color of the selected options.
    :type selected_indicator_bg_color: str

    :return: The list of chosen options.
    :rtype: list

    :examples:
        >>> result = multi_choice_question_interactive(
                        "Choose your favorite colors:", ["red", "green", "blue"]
                     )
        Please choose one or more of the following options
        (use arrows to navigate, space to select, Enter to finish):
          > red
            green
            blue
        Press Enter to finish.
        >>> print(result)
        ["red"]

        >>> result = multi_choice_question_interactive(
                        "Choose your favorite colors:", ["red", "green", "blue"]
                     )
        Please choose one or more of the following options
        (use arrows to navigate, space to select, Enter to finish):
            red
          > green
            blue
        Press Enter to finish.
        >>> print(result)
        ["green"]

        >>> result = multi_choice_question_interactive(
                        "Choose your favorite colors:", ["red", "green", "blue"]
                     )
        Please choose one or more of the following options
        (use arrows to navigate, space to select, Enter to finish):
            red
            green
          > blue
        Press Enter to finish.
        >>> print(result)
        ["blue"]

        >>> result = multi_choice_question_interactive(
                        "Choose your favorite colors:", ["red", "green", "blue"]
                     )
        Please choose one or more of the following options
        (use arrows to navigate, space to select, Enter to finish):
            red
            green
            blue
        Press Enter to finish.
        >>> print(result)
        []
    """

    def draw_menu(stdscr, selected_idx, selected_choices):
        stdscr.clear()
        stdscr.addstr(0, 0, prompt, curses.color_pair(1))
        for idx, choice in enumerate(choices):
            if idx == selected_idx:
                stdscr.addstr(idx + 1, 0, f"> {choice}", curses.color_pair(3))
            else:
                stdscr.addstr(idx + 1, 0, f"  {choice}", curses.color_pair(2))
            if choice in selected_choices:
                stdscr.addstr(idx + 1, len(choice) + 3, "[x]", curses.color_pair(4))
        stdscr.refresh()

    def main(stdscr):
        curses.start_color()
        # prompt colors
        curses.init_pair(
            1,
            CURSES_COLOR_MAP.get(prompt_fg_color),
            CURSES_COLOR_MAP.get(prompt_bg_color),
        )
        # option colors
        curses.init_pair(
            2,
            CURSES_COLOR_MAP.get(option_fg_color),
            CURSES_COLOR_MAP.get(option_bg_color),
        )
        # hovered selection option colors
        curses.init_pair(
            3,
            CURSES_COLOR_MAP.get(hover_fg_color),
            CURSES_COLOR_MAP.get(hover_bg_color),
        )
        # selected indicator colors [x]
        curses.init_pair(
            4,
            CURSES_COLOR_MAP.get(selected_indicator_fg_color),
            CURSES_COLOR_MAP.get(selected_indicator_bg_color),
        )

        selected_idx = 0
        selected_choices = []

        while True:
            draw_menu(stdscr, selected_idx, selected_choices)
            key = stdscr.getch()

            if key == curses.KEY_UP and selected_idx > 0:
                selected_idx -= 1
            elif key == curses.KEY_DOWN and selected_idx < len(choices) - 1:
                selected_idx += 1
            elif key == ord(" "):
                choice = choices[selected_idx]
                if choice in selected_choices:
                    selected_choices.remove(choice)
                else:
                    selected_choices.append(choice)
            elif key == ord("\n"):
                break

        return selected_choices

    return curses.wrapper(main)
