import math


class Coordinates:
    """
    Defines the interface for a 3-D coordinate system
    """

    def x(self) -> float:
        """
        Returns the "horizontal" coordinate, eg. longitude, X, width, left/right, column...
        """
        pass

    def y(self) -> float:
        """
        Returns the "vertical" coordinate, eg. latitude, Y, height, top/bottom, row...
        """
        pass

    def z(self) -> None | float:
        """
        Returns the third dimension if any, eg. altitude, Z, depth, up/down...
        """
        pass

    def __eq__(self, other):
        return self.x() == other.x() and self.y() == other.y() and self.z() == other.z()


class GPS(Coordinates):
    """
    Implements the GPS coordinates system
    """

    def __init__(self, longitude: float, latitude: float):
        self._x = longitude
        self._y = latitude

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def z(self) -> None | float:
        return None


class Tile(Coordinates):
    """
    Implements the coordinate of a tile in a Grid
    where `x` is the column and `y` is the row
    starting from the bottom-left point of the Grid
    """

    @staticmethod
    def Distance(t1, t2) -> float:
        """
        Computes the distance between two Tiles,
        returning the number of tiles in each direction
        """
        return math.sqrt(
            math.pow(t2.x() - t1.x(), 2) + math.pow(t2.y() - t1.y(), 2)
        ) / math.sqrt(2)

    @staticmethod
    def FromString(coord: str):
        """
        Returns the tile from the passed coordinate string
        """
        row, column = coord.split(".", 2)
        return Tile(column, row)

    def __init__(self, column: int, row: int):
        self._x = float(column)
        self._y = float(row)

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def z(self) -> None | float:
        return None

    def to_string(self) -> str:
        """
        Returns the tile as a &lt;row&gt;.&lt;column&gt; string
        """
        return f"{int(self._y)}.{int(self._x)}"


class XY(Coordinates):
    """
    Implements the X/Y coordinates system, naming the associated projection and geodesic systems (defaults to UTM with WGS84)
    """

    def __init__(self, x: float, y: float, projection="UTM", gis="WGS84"):
        self._x = x
        self._y = y
        self.projection = projection
        self.gis = gis

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def z(self) -> None | float:
        return None
