# pylint:disable=invalid-name


class Color:
    """Codes des couleurs et styles d'affichage écran."""

    END = "\33[0m"
    BOLD = "\33[1m"
    ITALIC = "\33[3m"
    URL = "\33[4m"

    BLACK = "\33[30m"
    RED = "\33[31m"
    GREEN = "\33[32m"
    YELLOW = "\33[33m"
    BLUE = "\33[34m"
    VIOLET = "\33[35m"
    BEIGE = "\33[36m"
    WHITE = "\33[37m"
    GREY = "\33[90m"

    BLACK_BG = "\33[40m"
    RED_BG = "\33[41m"
    GREEN_BG = "\33[42m"
    YELLOW_BG = "\33[43m"
    BLUE_BG = "\33[44m"
    VIOLET_BG = "\33[45m"
    BEIGE_BG = "\33[46m"
    WHITE_BG = "\33[47m"
    GREY_BG = "\33[100m"
