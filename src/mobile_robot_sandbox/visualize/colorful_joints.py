from Rhino.Display import ColorRGBA
from ghpythonlib.components import ColourRGBf


def colorful_joints(planes, scale=1.0, width=3):
    red = ColourRGBf(255, 255, 0, 0)
    green = ColourRGBf(255, 0, 255, 0)
    blue = ColourRGBf(255, 0, 0, 255)

    P = []
    V = []
    C = []

    for plane in planes:
        if not plane:
            continue
        P += [plane.Origin] * 3
        V.append(plane.XAxis * scale)
        V.append(plane.YAxis * scale)
        V.append(plane.ZAxis * scale)
        C += [red, green, blue]

    W = width
    return P, V, C, W