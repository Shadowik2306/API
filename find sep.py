def sep_find(toponym):
    corn = toponym['boundedBy']['Envelope']
    a, b = map(float, corn['lowerCorner'].split())
    c, d = map(float, corn['upperCorner'].split())
    return str(a / c), str(b / d)