# Basic line follower example


!!! note
    This example is work-in-progress

## Planned

* [ ] demo notebook



## Design

Data flow:

```mermaid

graph TD
    controller_node --> |"(Vl,Vr)"|diffdrive_node
    diffdrive_node --> |"(Sl,Sr)"| odometry_node
    odometry_node -->|"(x,y,phi)"|controller_node

```


The system consists of 3 nodes:

* **controller** - uses  pure pursuit control algorithm to follow a line along x-axis
* **diffdrive** - simulates a differential drive robot
* **odometry** - keeps track of robot orientation based on dead reckoning

Each node is a class, running its own coroutines.

A class diagram would look like this:

```mermaid
classDiagram


class Controller {
    set_ab_line(a,b)
}

class Machine{

    get_pose() -> Pose
    cmd_vel(twist)
}

class DiffDrive{
    set_vel(k)
    get_pos() -> sl,sr
}

class Odometry{
    update(sl,sr)
    get_pose() -> Pose
}

class Wheel {
    set_vel(v)
    get_dst() ->s
}

Controller  o-- Machine
Machine *-- DiffDrive
DiffDrive *--"2"Wheel
DiffDrive *-- Odometry


```


**Note:** we are assuming perfect odometry tracking here. In real world, this is not the case and odometry values are subject to drift. To solve this, sensor fusion techiques are often used like particle filters or Kalman filter.
