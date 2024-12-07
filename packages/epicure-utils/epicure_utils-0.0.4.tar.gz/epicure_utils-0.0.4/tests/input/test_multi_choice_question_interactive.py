import curses

from unittest.mock import MagicMock

import pytest

from epicure.input.question import multi_choice_question_interactive


@pytest.fixture
def mock_curses(mocker):
    mock_curses = mocker.patch("epicure.input.question.curses")
    mock_curses.KEY_UP = 259
    mock_curses.KEY_DOWN = 258
    mock_stdscr = MagicMock()

    def wrapper_side_effect(func):
        return func(mock_stdscr)

    mock_curses.wrapper.side_effect = wrapper_side_effect
    mock_curses.color_pair.side_effect = lambda x: x

    return mock_curses, mock_stdscr


def test_basic_selection(mock_curses):
    mock_curses, mock_stdscr = mock_curses
    mock_stdscr.getch.return_value = ord("\n")  # Enter key

    choices = ["Option 1", "Option 2"]
    result = multi_choice_question_interactive("Select options:", choices)

    assert result == []
    mock_curses.start_color.assert_called_once()


def test_single_selection(mock_curses):
    mock_curses, mock_stdscr = mock_curses
    mock_stdscr.getch.side_effect = [ord(" "), ord("\n")]  # Space then Enter

    choices = ["Option 1", "Option 2"]
    result = multi_choice_question_interactive("Select options:", choices)

    assert result == ["Option 1"]


def test_multiple_selections(mock_curses):
    mock_curses, mock_stdscr = mock_curses
    mock_stdscr.getch.side_effect = [
        ord(" "),  # Select first option
        curses.KEY_DOWN,  # Move down
        ord(" "),  # Select second option
        ord("\n"),  # Finish
    ]

    choices = ["Option 1", "Option 2"]
    result = multi_choice_question_interactive("Select options:", choices)

    assert result == ["Option 1", "Option 2"]


def test_navigation_boundaries(mock_curses):
    mock_curses, mock_stdscr = mock_curses
    mock_stdscr.getch.side_effect = [
        curses.KEY_UP,  # Try to go above first option
        curses.KEY_DOWN,  # Go down
        curses.KEY_DOWN,  # Try to go below last option
        curses.KEY_UP,  # Go up
        ord("\n"),  # Finish
    ]

    choices = ["Option 1", "Option 2"]
    result = multi_choice_question_interactive("Select options:", choices)

    assert result == []


def test_deselection(mock_curses):
    mock_curses, mock_stdscr = mock_curses
    mock_stdscr.getch.side_effect = [
        ord(" "),  # Select first option
        ord(" "),  # Deselect first option
        ord("\n"),  # Finish
    ]

    choices = ["Option 1", "Option 2"]
    result = multi_choice_question_interactive("Select options:", choices)

    assert result == []


def test_custom_colors(mock_curses):
    mock_curses, mock_stdscr = mock_curses
    mock_stdscr.getch.return_value = ord("\n")

    choices = ["Option 1"]
    result = multi_choice_question_interactive(
        "Select options:",
        choices,
        prompt_fg_color="red",
        prompt_bg_color="white",
        option_fg_color="green",
        option_bg_color="black",
    )

    assert mock_curses.init_pair.call_count == 4
    assert result == []


def test_menu_drawing(mock_curses):
    mock_curses, mock_stdscr = mock_curses
    mock_stdscr.getch.side_effect = [ord(" "), ord("\n")]

    choices = ["Option 1", "Option 2"]
    multi_choice_question_interactive("Select options:", choices)

    # Verify menu is drawn
    assert mock_stdscr.clear.called
    assert mock_stdscr.addstr.called
    assert mock_stdscr.refresh.called
