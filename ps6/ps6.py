# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

# -*- coding: utf-8 -*-

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.dirty_tiles = []
        self.clean_tiles = []
        for x in range(width):
            for y in range(height):
                self.dirty_tiles.append((x, y))


    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = int(math.floor(pos.getX()))
        y = int(math.floor(pos.getY()))
        if (x, y) in self.dirty_tiles:
            self.dirty_tiles.remove((x, y))
            self.clean_tiles.append((x, y))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (m, n) in self.clean_tiles:
            return True
        else:
            return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        clean_tiles = len(self.clean_tiles)
        dirty_tiles = len(self.dirty_tiles)
        return clean_tiles + dirty_tiles

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.clean_tiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        rand_x = random.random() * self.width
        rand_y = random.random() * self.height
        return Position(rand_x, rand_y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        if (y < 0 or y > self.height) or (x < 0 or x > self.width):
            return False
        else:
            return True



class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.random() * 360
        self.position = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)



    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_pos = self.position.getNewPosition(self.direction, self.speed)
        self.position = new_pos
        self.room.cleanTileAtPosition(self.position)



# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        attempted_new_pos = self.position.getNewPosition(self.direction, self.speed)
        if not self.room.isPositionInRoom(attempted_new_pos):
            new_x = attempted_new_pos.getX()
            new_y = attempted_new_pos.getY()
            if new_x > self.room.width:
                new_x = self.room.width
            if new_x < 0:
                new_x = 0
            if new_y > self.room.height:
                new_y = self.room.height
            if new_y < 0:
                new_y = 0

            attempted_new_pos = Position(new_x, new_y)
            self.setRobotDirection(random.random() * 360)
        self.position = attempted_new_pos
        self.room.cleanTileAtPosition(self.position)

# === Problem 3
def checkCoverage(room, min_coverage):
    """
    Returns True if percent of tiles >= min_coverage
    Returns False otherwise
    """
    total_tiles = len(room.clean_tiles) + len(room.dirty_tiles)
    percent_covered = float(len(room.clean_tiles)) / total_tiles
    if percent_covered >= min_coverage:
        return True
    else:
        return False

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    trial_results = []
    for i in range(num_trials):
        R1 = RectangularRoom(width, height)
        robot_list = []
        for n in range(num_robots):
            robot_list.append(robot_type(R1, speed))
        time_steps = 0
        min_coverage_achieved = checkCoverage(R1, min_coverage)
        while not min_coverage_achieved:
            for robot in robot_list:
                robot.updatePositionAndClean()
                #print "X =", robot.getRobotPosition().getX(), " Y =", robot.getRobotPosition().getY()
            time_steps += 1
            min_coverage_achieved = checkCoverage(R1, min_coverage)
        trial_results.append(time_steps)
    return float(sum(trial_results)) / len(trial_results)


# num_robots = 1
# speed = 1
# width = 20
# height = 20
# min_coverage = 1
# num_trials = 10
# robot_type = StandardRobot
# print runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
#                       robot_type)

# === Problem 4
#
# 1) How long does it take to clean 80 percent of a 20x20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80 percent of rooms with dimensions
#    20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    robot_range = range(1, 11)
    results = []
    for n in robot_range:
        sim_result = runSimulation(n, 1, 20, 20, 0.8, 10, StandardRobot)
        results.append(sim_result)
    pylab.plot(robot_range, results)
    pylab.xlabel("Number of Robots in Room")
    pylab.ylabel("Number of Time Steps")
    pylab.title("Time to clean 80% of 20 x 20 room")
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    room_sizes = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    width_to_height_ratio = []
    time_results = []
    for width, height in room_sizes:
        sim_result = runSimulation(2, 1, width, height, 0.8, 100, StandardRobot)
        time_results.append(sim_result)
        width_to_height_ratio.append(float(width) / float(height))
    pylab.plot(width_to_height_ratio, time_results)
    pylab.xlabel("Width to Height Ratio")
    pylab.ylabel("Number of Time Steps")
    pylab.title("Time to clean 80% of 400sq area room with two robots")
    pylab.show()


# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        attempted_new_pos = self.position.getNewPosition(self.direction, self.speed)
        if not self.room.isPositionInRoom(attempted_new_pos):
            new_x = attempted_new_pos.getX()
            new_y = attempted_new_pos.getY()
            if new_x > self.room.width:
                new_x = self.room.width
            if new_x < 0:
                new_x = 0
            if new_y > self.room.height:
                new_y = self.room.height
            if new_y < 0:
                new_y = 0

            attempted_new_pos = Position(new_x, new_y)
        self.setRobotDirection(random.random() * 360)
        self.position = attempted_new_pos
        self.room.cleanTileAtPosition(self.position)



# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    robot_types = [StandardRobot, RandomWalkRobot]
    stand_results = []
    rand_walk_results = []
    robot_range = range(1, 11)
    for n in robot_range:
        stand_result = runSimulation(n, 1, 20, 20, 0.8, 10, StandardRobot)
        rand_walk_result = runSimulation(n, 1, 20, 20, 0.8, 10, RandomWalkRobot)
        stand_results.append(stand_result)
        rand_walk_results.append(rand_walk_result)
    pylab.plot(robot_range, stand_results, color="red", label="Standard Robot")
    pylab.plot(robot_range, rand_walk_results, color="green", label="Random Walk Robot")
    pylab.legend()
    pylab.xlabel("Number of Robots in Room")
    pylab.ylabel("Number of Time Steps")
    pylab.title("Time to clean 80% of 20 x 20 room (10 trials)")
    pylab.show()
