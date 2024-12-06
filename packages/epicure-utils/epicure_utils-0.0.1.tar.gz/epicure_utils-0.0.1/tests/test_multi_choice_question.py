from epicure.input.question import multi_choice_question


def test_multi_choice_single_selection(mocker, capsys):
    choices = ["Apple", "Banana", "Orange"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["1", ""]

    result = multi_choice_question("Select fruits:", choices)

    assert result == ["Apple"]
    assert mock_input.call_count == 2


def test_multi_choice_multiple_selections(mocker, capsys):
    choices = ["Apple", "Banana", "Orange"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["1", "2", ""]

    result = multi_choice_question("Select fruits:", choices)

    assert result == ["Apple", "Banana"]
    assert mock_input.call_count == 3


def test_multi_choice_deselection(mocker, capsys):
    choices = ["Apple", "Banana", "Orange"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["1", "2", "1", ""]

    result = multi_choice_question("Select fruits:", choices)

    assert result == ["Banana"]
    assert mock_input.call_count == 4


def test_multi_choice_empty_input(mocker, capsys):
    choices = ["Apple", "Banana", "Orange"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = [""]

    result = multi_choice_question("Select fruits:", choices)

    assert result == []
    assert mock_input.call_count == 1


def test_multi_choice_invalid_input(mocker, capsys):
    choices = ["Apple", "Banana", "Orange"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["invalid", "4", "0", "1", ""]

    result = multi_choice_question("Select fruits:", choices)

    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out
    assert result == ["Apple"]
    assert mock_input.call_count == 5


def test_multi_choice_with_colors(mocker, capsys):
    choices = ["Apple", "Banana"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["1", ""]

    result = multi_choice_question(
        "Select fruits:", choices, prompt_fg_color="blue", prompt_bg_color="white"
    )

    assert result == ["Apple"]


def test_multi_choice_preserves_order(mocker, capsys):
    choices = ["Apple", "Banana", "Orange"]
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["3", "1", "2", ""]

    result = multi_choice_question("Select fruits:", choices)

    assert result == ["Orange", "Apple", "Banana"]
    assert len(result) == 3
