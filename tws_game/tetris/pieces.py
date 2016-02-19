class BasePiece:
    def __init__(self):
        pass


class PieceI(BasePiece):
    color = 'cyan'

    rotations = (
        (0, 0, 0, 0,
         1, 1, 1, 1,
         0, 0, 0, 0,
         0, 0, 0, 0, ),

        (0, 0, 1, 0,
         0, 0, 1, 0,
         0, 0, 1, 0,
         0, 0, 1, 0, ),
    )


class PieceO(BasePiece):
    color = 'yellow'

    rotations = (
        (0, 0, 0,
         1, 1, 1,
         0, 1, 0, ),

        (0, 1, 0,
         1, 1, 0,
         0, 1, 0, ),

        (0, 0, 0,
         0, 1, 0,
         1, 1, 1, ),

        (0, 1, 0,
         0, 1, 1,
         0, 1, 0, ),
    )


class PieceT(BasePiece):
    color = 'purple'


class PieceS(BasePiece):
    color = 'green'


class PieceZ(BasePiece):
    color = 'red'


class PieceJ(BasePiece):
    color = 'blue'


class PieceL(BasePiece):
    color = 'orange'
