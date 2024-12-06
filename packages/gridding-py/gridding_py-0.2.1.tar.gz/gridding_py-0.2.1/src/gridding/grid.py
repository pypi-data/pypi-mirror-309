import math

from gridding import GIS, GPS, PostalAddress, Tile, WGS84

KILOMETER = "km"
METER = "m"


class Resolution:
    """
    Defines the resolution of a tile / "carreau", eg. `200m`
    """

    @staticmethod
    def FromString(value: str):
        if "km" in value:
            unit = KILOMETER
        else:
            unit = METER
        size = int(value.replace(unit, ""))
        return Resolution(size, unit)

    def __init__(self, size: int, unit: str):
        self.size = size
        if unit == KILOMETER or unit == METER:
            self.unit = unit
        else:
            raise Exception("Unknown unit")

    def to_string(self) -> str:
        """
        Returns the code to use in a tile's ID, eg. `RES200m`
        """
        return "RES%d%s" % (self.size, self.unit)


class Grid:
    """
    A Grid is defined by:
    - a resolution: the size and unit to use for one tile / "carreau";
    - its pivot: the bottom-left corner of the bounding box covered (defaults to metropolitan France's);
    - the geodesic system to use (defaults to `WGS84`).
    """

    def __init__(
        self,
        resolution: Resolution,
        pivot: GPS = GPS(-5.151111, 41.316666),
        system: GIS = WGS84(),
    ):
        self.resolution = resolution
        self.pivot = pivot
        self.system = system

    def from_address(self, address: str, repository: PostalAddress) -> tuple[str, Tile]:
        """
        Returns the tile informations (code, coordinate) from the passed full address,
        eg. code: `WGS84|RES200m|N2471400|E0486123`, coordinate: `1234.4567`
        """
        point = repository.address2gps(address)
        return self.from_gps(point)

    def from_gps(self, point: GPS) -> tuple[str, Tile]:
        """
        Returns the tile informations (code, coordinate) from the passed GPS coordinates,
        eg. code: `WGS84|RES200m|N2471400|E0486123`, coordinate: `1234.4567`
        """
        side = self._get_side_in_meters()

        # First, search along latitude
        current_y = self.pivot.y()
        previous_y = current_y
        y = 1
        if current_y < point.y():
            up = self.system.delta_latitude(side, current_y)
            while point.y() > current_y:
                previous_y = current_y
                current_y += up
                up = self.system.delta_latitude(side, current_y)
                y += 1
        else:
            down = self.system.delta_latitude(side, current_y)
            while point.y() < current_y:
                previous_y = current_y
                current_y -= down
                down = self.system.delta_latitude(side, current_y)
                y -= 1

        # Then, search along longitude
        current_x = self.pivot.x()
        previous_x = current_x
        x = 1
        if current_x < point.x():
            right = self.system.delta_longitude(side, current_x, current_y)
            while point.x() > current_x:
                previous_x = current_x
                current_x += right
                x += 1
        else:
            left = self.system.delta_longitude(side, current_x, current_y)
            while point.x() < current_x:
                previous_x = current_x
                current_x -= left
                x -= 1

        # Finally, build code and coordinate
        return self._get_code(GPS(previous_x, previous_y)), Tile(x, y)

    # Private methods

    def _get_code(self, bottom_left: GPS) -> str:
        """
        Returns the actual code using the passed bottom-left GPS coordinates of the tile

        NB: only 5 digits are kept in the decimal degree used
        """
        ns = "N" if bottom_left.y() >= 0 else "S"
        y = "%07d" % math.ceil(abs(bottom_left.y()) * 100000)
        we = "E" if bottom_left.x() >= 0 else "W"
        x = "%07d" % math.ceil(abs(bottom_left.x()) * 100000)
        return "|".join(
            [self.system.name(), self.resolution.to_string(), f"{ns}{y}", f"{we}{x}"]
        )

    def _get_side_in_meters(self) -> float:
        """
        Returns the grid side size in meters
        """
        if self.resolution.unit == KILOMETER:
            return self.resolution.size * 1000.0
        else:
            return self.resolution.size
