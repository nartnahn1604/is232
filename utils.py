def format_lv(level, text):
    levels = [
         "<h5>{}</h5>", 
         "<h6>{}</h6>",
         "<span>{}</span>"
    ]
    if level - 1 < len(levels):
        return levels[level - 1].format(text)
    return levels[len(levels) - 1].format(text)

def format_currency(value):
    s = ""
    temp = value
    if temp < 0:
        temp = abs(temp)
    while temp > 0:
        s = f".{temp % 1000}" + s
        temp //= 1000
    if value < 0:
        s = "-" + s
    return s