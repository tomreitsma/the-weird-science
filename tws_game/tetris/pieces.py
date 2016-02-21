class BasePiece(object):
    rotation = 0
    rotations = ()

    offset_top = 0
    offset_left = 0

    square_size = 3

    def __init__(self):
        self.offset_left = 0
        self.offset_top = 0

    def _get_next_rotation(self):
        rotation = self.rotation + 1

        if rotation >= len(self.rotations):
            rotation = 0

        return rotation

    def rotate(self):
        self.rotation += 1

        if self.rotation >= len(self.rotations):
            self.rotation = 0

    def current_rotation(self):
        return self.rotations[self.rotation]

    def next_rotation(self):
        return self.rotations[self._get_next_rotation()]

    def get_active_coordinates(self):
        active_coordinates = []
        current_rotation = self.current_rotation()

        for y, y_data in enumerate(current_rotation):
            for x, x_data in enumerate(current_rotation[y]):
                if current_rotation[y][x] == 1:
                    active_coordinates.append(
                        (self.offset_left + x, self.offset_top + y, )
                    )

        return active_coordinates

    def get_right_most_coordinate(self):
        highest = 0

        for y, y_data in enumerate(self.current_rotation()):
            for x, value in enumerate(y_data):
                if value == 1 and x > highest:
                    highest = x

        return highest

    def get_left_most_coordinate(self):
        lowest = 999

        for y, y_data in enumerate(self.current_rotation()):
            for x, value in enumerate(y_data):
                if value == 1 and x < lowest:
                    lowest = x

        return lowest


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

    square_size = 4

    rotations = (
        ((0, 0, 0, 0,),
         (0, 1, 1, 0,),
         (0, 1, 1, 0,),
         (0, 0, 0, 0,),),
    )


class PieceS(BasePiece):
    color = 'green'

    rotations = (
        ((0, 0, 0,),
         (0, 1, 1,),
         (1, 1, 0,), ),

        ((1, 0, 0,),
         (1, 1, 0,),
         (0, 1, 0,), ),
    )


class PieceZ(BasePiece):
    color = 'red'

    rotations = (
        ((0, 0, 0, ),
         (1, 1, 0, ),
         (0, 1, 1, ), ),

        ((0, 0, 1, ),
         (0, 1, 1, ),
         (0, 1, 0, ), )
    )


class PieceJ(BasePiece):
    color = 'blue'

    rotations = (
        ((0, 0, 0, ),
         (1, 1, 1, ),
         (0, 0, 1, ), ),

        ((0, 1, 0, ),
         (0, 1, 0, ),
         (1, 1, 0, ), ),

        ((0, 0, 0, ),
         (1, 0, 0, ),
         (1, 1, 1, ), ),

        ((0, 1, 1, ),
         (0, 1, 0, ),
         (0, 1, 0, ), )
    )


class PieceL(BasePiece):
    color = 'orange'

    rotations = (
        ((0, 0, 0, ),
         (1, 1, 1, ),
         (1, 0, 0, ), ),

        ((1, 1, 0, ),
         (0, 1, 0, ),
         (0, 1, 0, ), ),

        ((0, 0, 0, ),
         (0, 0, 1, ),
         (1, 1, 1, ), ),

        ((0, 1, 0, ),
         (0, 1, 0, ),
         (0, 1, 1, ), )
    )
