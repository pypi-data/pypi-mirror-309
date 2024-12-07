import pytest

from epicure.input.question import ask_yes_no_question


def test_ask_yes_no_question_default_yes(mocker):
    mocker.patch("builtins.input", return_value="")
    assert ask_yes_no_question("Is this a test?", default="yes")


def test_ask_yes_no_question_default_no(mocker):
    mocker.patch("builtins.input", return_value="")
    assert not ask_yes_no_question("Is this a test?", default="no")


def test_ask_yes_no_question_yes_responses(mocker):
    for response in ["yes", "y", "YES", "Y"]:
        mocker.patch("builtins.input", return_value=response)
        assert ask_yes_no_question("Is this a test?")


def test_ask_yes_no_question_no_responses(mocker):
    for response in ["no", "n", "NO", "N"]:
        mocker.patch("builtins.input", return_value=response)
        assert not ask_yes_no_question("Is this a test?")


def test_ask_yes_no_question_case_sensitive_yes(mocker):
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["yes"]
    assert ask_yes_no_question("Is this a test?", case_sensitive=True)


def test_ask_yes_no_question_case_sensitive_invalid_then_yes(mocker):
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["Yes", "yes"]  # First try wrong case, then correct
    assert ask_yes_no_question("Is this a test?", case_sensitive=True)
    assert mock_input.call_count == 2


def test_ask_yes_no_question_case_sensitive_no(mocker):
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["no"]
    assert not ask_yes_no_question("Is this a test?", case_sensitive=True)


def test_ask_yes_no_question_invalid_default(mocker):
    with pytest.raises(ValueError, match="Invalid default answer. Must be 'yes' or 'no'"):
        ask_yes_no_question("Is this a test?", default="invalid")


def test_ask_yes_no_question_retry_on_invalid_input(mocker):
    # Mock input to return invalid answer first, then valid answer
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["invalid", "yes"]

    assert ask_yes_no_question("Is this a test?")
    assert mock_input.call_count == 2


def test_ask_yes_no_question_custom_error_message(mocker, capsys):
    # Mock the input function to return invalid input first, then valid input
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["invalid", "yes"]

    # Call the function with custom error message
    result = ask_yes_no_question("Is this a test?", error_message="Invalid response.")

    # Capture the printed output
    captured = capsys.readouterr()

    # Verify the function returned True (from "yes" input)
    assert result is True

    # Verify input was called twice (invalid + valid)
    assert mock_input.call_count == 2

    # Verify our custom error message was printed
    assert "Invalid response." in captured.out
