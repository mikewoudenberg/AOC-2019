def getBoundingRect(coords):
    x1 = x2 = coords[0][0]
    y1 = y2 = coords[0][1]
    for (x, y) in coords:
        x1 = min(x1, x)
        x2 = max(x2, x)
        y1 = min(y1, y)
        y2 = max(y2, y)
    return x1, x2 + 1, y1, y2 + 1
