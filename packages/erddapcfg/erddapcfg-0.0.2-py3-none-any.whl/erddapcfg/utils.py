from enum import StrEnum


class Mode(StrEnum):
    """Enum used to select the mode of the line ending conversion."""

    Win2Unix = "Win2Unix"
    Unix2Win = "Unix2Win"


def change_line_ending(filename: str, mode: Mode = Mode.Win2Unix):
    """Convert the line ending of the given file using the given mode.

    Args:
        filename (str): File to convert the line ending.
        mode (Mode, optional): Type of conversion, windows to unix or vice versa. Defaults to Mode.Win2Unix.
    """
    WINDOWS_LINE_ENDING = b"\r\n"
    UNIX_LINE_ENDING = b"\n"

    # Open given file
    with open(filename, "rb") as open_file:
        content = open_file.read()

    if mode == Mode.Win2Unix:
        # Windows to Unix
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

    elif mode == Mode.Unix2Win:
        # Unix to Windows
        content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

    # Save converted file
    with open(filename, "wb") as open_file:
        open_file.write(content)
