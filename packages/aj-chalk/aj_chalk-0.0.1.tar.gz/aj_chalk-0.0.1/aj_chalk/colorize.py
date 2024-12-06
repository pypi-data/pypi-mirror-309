from utils.hex_to_rgb import hex_to_rgb


def colorize(color="#fff", text="", should_print=False):
    if color.startswith("#"):
        r, g, b = hex_to_rgb(color)
        color_code = f"\033[38;2;{r};{g};{b}m"
    else:
        color_code = "\033[0m"
        
    text = f"{color_code}{text}\033[0m"
    if should_print:
        print(text)
    return text