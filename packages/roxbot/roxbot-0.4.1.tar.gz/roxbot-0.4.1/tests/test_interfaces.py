# type: ignore

import time
from roxbot import interfaces
from rox_vectors import Vector


def test_machine():
    class TestMachine(interfaces.MachineProtocol):
        def get_pose(self) -> interfaces.Pose:
            return interfaces.Pose(1, 2, 3)

        def cmd_vel(self, linear_velocity: float, angular_velocity: float) -> None:
            pass

        def cmd_curvature(self, v_linear: float, curvature: float) -> None:
            pass

        async def main(self) -> None:
            pass

    m = TestMachine()
    assert m.get_pose() == interfaces.Pose(1, 2, 3)
    m.cmd_vel(1, 1)
    m.cmd_curvature(1, 1)

    xy = m.get_pose().xy
    assert xy == Vector(1, 2)


def test_data_classes():

    latlon = interfaces.GpsLatlon(1, 2)

    assert latlon.lat == 1
    assert latlon.lon == 2
    assert latlon.gps_qual == 0

    head = interfaces.GpsHeading(1, 2)
    assert head.heading == 1
    assert head.heading_stdev == 2

    pos = interfaces.PositionData(1, 2)
    assert pos.lat == 1
    assert pos.lon == 2
    assert pos.x == 0
    assert pos.y == 0
    assert pos.gps_qual == 0

    head = interfaces.HeadingData(1, 2, 3)
    assert head.heading == 1
    assert head.heading_stdev == 2
    assert head.theta == 3
