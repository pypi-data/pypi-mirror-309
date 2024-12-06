def hex_to_rgb(hex_color="#fff"):
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


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