"""Color utilities for terminal output."""


def color_code(code: int) -> str:
    """Generate ANSI color code."""
    return f"\x1b[{code}m"


def colorize(code: int, s: str) -> str:
    """Colorize a string with ANSI color codes.

    Args:
        code: ANSI color code.
        s: String to colorize.

    Returns:
        Colorized string with ANSI codes.
    """
    reset_code = color_code(0)
    return f"{color_code(code)}{str(s).replace(reset_code, color_code(code))}{reset_code}"


def green(s: str) -> str:
    """Color string green."""
    return colorize(32, s)


def yellow(s: str) -> str:
    """Color string yellow."""
    return colorize(33, s)


def red(s: str) -> str:
    """Color string red."""
    return colorize(31, s)


def cyan(s: str) -> str:
    """Color string cyan."""
    return colorize(36, s)


def magenta(s: str) -> str:
    """Color string magenta."""
    return colorize(35, s)


def bold(s: str) -> str:
    """Make string bold."""
    return colorize(1, s)


def dim(s: str) -> str:
    """Make string dim."""
    return colorize(2, s)


def italic(s: str) -> str:
    """Make string italic."""
    return colorize(3, s)


def underline(s: str) -> str:
    """Underline string."""
    return colorize(4, s)


def blink(s: str) -> str:
    """Make string blink."""
    return colorize(5, s)


def reverse(s: str) -> str:
    """Reverse string colors."""
    return colorize(7, s)


def invisible(s: str) -> str:
    """Make string invisible."""
    return colorize(8, s)
