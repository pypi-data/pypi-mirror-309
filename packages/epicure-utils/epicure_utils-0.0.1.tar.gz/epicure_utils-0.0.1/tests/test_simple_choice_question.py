from epicure.input.question import simple_choice_question


def test_simple_choice_valid_input(mocker, capsys):
    choices = ["red", "blue", "green"]
    mock_input = mocker.patch("builtins.input", return_value="2")

    result = simple_choice_question("Pick a color:", choices)

    assert result == "blue"
    assert mock_input.call_count == 1


def test_simple_choice_invalid_then_valid(mocker, capsys):
    choices = ["red", "blue", "green"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["4", "0", "invalid", "2"]

    result = simple_choice_question("Pick a color:", choices)

    captured = capsys.readouterr()
    assert result == "blue"
    assert mock_input.call_count == 4
    assert "Invalid choice" in captured.out


def test_simple_choice_out_of_range(mocker, capsys):
    choices = ["red", "blue", "green"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["4", "1"]

    result = simple_choice_question("Pick a color:", choices)

    captured = capsys.readouterr()
    assert result == "red"
    assert "Invalid choice" in captured.out


def test_simple_choice_non_numeric(mocker, capsys):
    choices = ["red", "blue", "green"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["abc", "!@#", "2"]

    result = simple_choice_question("Pick a color:", choices)

    captured = capsys.readouterr()
    assert result == "blue"
    assert "Invalid choice" in captured.out


def test_simple_choice_empty_input(mocker, capsys):
    choices = ["red", "blue", "green"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["", "1"]

    result = simple_choice_question("Pick a color:", choices)

    captured = capsys.readouterr()
    assert result == "red"
    assert "Invalid choice" in captured.out


def test_simple_choice_with_colors(mocker, capsys):
    choices = ["red", "blue"]
    mock_input = mocker.patch("builtins.input", return_value="1")

    result = simple_choice_question(
        "Pick a color:", choices, prompt_fg_color="red", prompt_bg_color="black"
    )

    assert result == "red"
    assert mock_input.call_count == 1
