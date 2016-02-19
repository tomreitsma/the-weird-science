class BasePiece(object):
    rotation = 0
    rotations = ()

    offset_top = 0
    offset_left = 0

    square_size = 3

    def rotate(self):
        self.rotation += 1

        if self.rotation >= len(self.rotations):
            self.rotation = 0

    def current_rotation(self):
        return self.rotations[self.rotation]


class PieceI(BasePiece):
    color = 'cyan'

    square_size = 4

    rotations = (
        ((0, 0, 0, 0,),
         (1, 1, 1, 1,),
         (0, 0, 0, 0,),
         (0, 0, 0, 0,), ),

        ((0, 0, 1, 0,),
         (0, 0, 1, 0,),
         (0, 0, 1, 0,),
         (0, 0, 1, 0,), ),
    )


class PieceT(BasePiece):
    color = 'yellow'

    rotations = (
        ((0, 0, 0,),
         (1, 1, 1,),
         (0, 1, 0,), ),

        ((0, 1, 0,),
         (1, 1, 0,),
         (0, 1, 0,), ),

        ((0, 0, 0,),
         (0, 1, 0,),
         (1, 1, 1,), ),

        ((0, 1, 0,),
         (0, 1, 1,),
         (0, 1, 0,), ),
    )


class PieceO(BasePiece):
    color = 'purple'


class PieceS(BasePiece):
    color = 'green'


class PieceZ(BasePiece):
    color = 'red'


class PieceJ(BasePiece):
    color = 'blue'


class PieceL(BasePiece):
    color = 'orange'
