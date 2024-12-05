from typing import Generator

def citerator(data: list, x: int = 0, y: int = 0, layer: bool = False) -> Generator:
    """Bi-dimensional matrix iterator starting from any point (i, j),
    iterating layer by layer around the starting coordinates.

    Args:
        data (list): Data set to iterate over.
        x (int): X starting coordinate.
        y (int): Y starting coordinate.

    Optional args:
        layered (bool): Yield value by value or entire layer.

    Yields:
        value: Layer value.
        list: Matrix layer.
    """

    LEN = len(data)

    if layer:
        yield [data[y][x]]
    else:
        yield data[y][x]

    for depth in range(LEN):
        l = []
        # top row
        xpos = y - depth - 1
        for i in range(x - depth - 1, x + depth + 1):
            if (not (i < 0
                or xpos < 0
                or i >= LEN
                or xpos >= LEN)
                and not (xpos >= LEN
                or i >= len(data[xpos]))):
                l.append(data[xpos][i])
        # right column
        ypos = x + depth + 1
        for i in range(y - depth - 1, y + depth + 1):
            if (not (i < 0
                or ypos < 0
                or i >= LEN
                or ypos >= LEN)
                and not (ypos >= LEN
                or ypos >= len(data[i]))):
                l.append(data[i][ypos])
        # bottom row
        xpos = y + depth + 1
        for i in reversed(range(x - depth, x + depth + 2)):
            if (not (i < 0
                or xpos < 0
                or i >= LEN
                or xpos >= LEN)
                and not (xpos >= LEN
                or i >= len(data[xpos]))):
                l.append(data[xpos][i])
        # left column
        ypos = x - depth - 1
        for i in reversed(range(y - depth, y + depth + 2)):
            if (not (i < 0
                or ypos < 0
                or i >= LEN
                or ypos >= LEN)
                and not (ypos >= LEN
                or ypos >= len(data[i]))):
                l.append(data[i][ypos])

        if l:
            if layer:
                yield l
            else:
                for v in l:
                    yield v
        else:
            break
