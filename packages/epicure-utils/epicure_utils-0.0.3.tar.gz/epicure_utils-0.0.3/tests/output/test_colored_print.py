from epicure.output.print import colored_print


def test_colored_print_with_default_colors(capsys):
    """Test colored_print with default colors"""
    message = "Test message"
    colored_print(message)

    captured = capsys.readouterr()
    assert message in captured.out


def test_colored_print_with_custom_colors(capsys):
    """Test colored_print with custom foreground and background colors"""
    message = "Test message"
    colored_print(message, fg_color="red", bg_color="white")

    captured = capsys.readouterr()
    assert message in captured.out


def test_colored_print_with_only_fg_color(capsys):
    """Test colored_print with only foreground color"""
    message = "Test message"
    colored_print(message, fg_color="red")

    captured = capsys.readouterr()
    assert message in captured.out


def test_colored_print_with_only_bg_color(capsys):
    """Test colored_print with only background color"""
    message = "Test message"
    colored_print(message, bg_color="white")

    captured = capsys.readouterr()
    assert message in captured.out


def test_colored_print_empty_message(capsys):
    """Test colored_print with empty message"""
    colored_print("")

    captured = capsys.readouterr()
    assert captured.out == "\n"
