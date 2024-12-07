from time import sleep

from epicure.collection.colors import BG_COLOR_CODES, FG_COLOR_CODES
from epicure.input import (
    ask_yes_no_question,
    multi_choice_question,
    multi_choice_question_interactive,
    simple_choice_question,
)
from epicure.output import colored_print


def welcome():
    colored_print("WELCOME TO THE EPICURE DEMO!", "magenta", "black", end="\n\n")
    colored_print(
        "All documentation is accessible at https://github.com/patillacode/epicure",
        "yellow",
        "black",
    )
    colored_print("Press Enter to continue...", "yellow", "black", end="")
    input()
    print()


def print_demo():
    colored_print("Let's demo the colored text!", "cyan", "black")
    colored_print("Press Enter to continue...", "yellow", "black", end="")
    input()

    for fg_color_name, _ in FG_COLOR_CODES.items():
        for bg_color_name, _ in BG_COLOR_CODES.items():
            if fg_color_name == bg_color_name:
                continue
            colored_print(
                f"This text is {fg_color_name} on {bg_color_name} background.",
                fg_color_name,
                bg_color_name,
            )
        print("\n")
        sleep(0.5)


def yes_no_questions_demo():
    colored_print("Let's demo the question asking!", "cyan", "black")
    colored_print("Press Enter to continue...", "yellow", "black", end="")
    input()

    response = ask_yes_no_question("Did you see all the colors above?")
    colored_print(f"You responded: {response}", end="\n\n")

    response = ask_yes_no_question(
        "Can you see this question has a colorful background?",
        prompt_fg_color="black",
        prompt_bg_color="yellow",
    )
    colored_print(f"You responded: {response}", end="\n\n")


def simple_choice_questions_demo():
    colored_print("Let's demo the simple choice questions!", "cyan", "black")
    colored_print("Press Enter to continue...", "yellow", "black", end="")
    input()

    response = simple_choice_question(
        "What is your favorite color?",
        ["red", "green", "blue", "yellow", "magenta", "cyan", "white"],
    )
    colored_print(
        f"You chose: {response}", fg_color=response, bg_color="black", end="\n\n"
    )


def multi_choice_questions_demo():
    colored_print("Let's demo the multi choice questions!", "cyan", "black")
    colored_print("Press Enter to continue...", "yellow", "black", end="")
    input()

    response = multi_choice_question(
        "What are your favorite colors?",
        ["red", "green", "blue", "yellow", "magenta", "cyan", "white"],
    )
    colored_print(
        f"You chose: {response}", fg_color="magenta", bg_color="black", end="\n\n"
    )


def multi_choice_questions_interactive_demo():
    colored_print("Let's demo the interactive multi choice questions!", "cyan", "black")
    colored_print("Press Enter to continue...", "yellow", "black", end="")
    input()

    selected_options = multi_choice_question_interactive(
        (
            "Please choose one or more of the following options (use arrows to navigate, "
            "space to select, Enter to finish):"
        ),
        ["Option A", "Option B", "Option C", "Option D"],
        prompt_fg_color="magenta",
        prompt_bg_color="black",
        option_fg_color="green",
        option_bg_color="black",
        hover_bg_color="cyan",
        hover_fg_color="black",
        selected_indicator_fg_color="yellow",
        selected_indicator_bg_color="black",
    )
    colored_print(
        f"You chose: {', '.join(selected_options)}",
        fg_color="magenta",
        bg_color="black",
    )


def main():
    welcome()
    print_demo()
    yes_no_questions_demo()
    simple_choice_questions_demo()
    multi_choice_questions_demo()
    multi_choice_questions_interactive_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        colored_print("\nExiting...", "red", "black")
        exit(1)
