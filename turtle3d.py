from vpython import *
from math import cos, sin

PI = 3.141592


class Turtle3D:

    def __init__(self):
        """Initializes the scene and the turtle"""
        # setup the scene
        scene.height = scene.width = 720
        scene.autocenter = True
        scene.caption = "Welcome to my Turtle3D visualizer"

        # paint the cartesian axis to not get lost in the "3D" space
        # cylinder(pos=vector(0, 0, 0), axis=vector(10, 0, 0), radius=0.1, color=color.white)
        # cylinder(pos=vector(0, 0, 0), axis=vector(0, 10, 0), radius=0.1, color=color.white)
        # cylinder(pos=vector(0, 0, 0), axis=vector(0, 0, 10), radius=0.1, color=color.white)

        # private variables because other programs have no business knowing these
        self.__direction_angle_h = 0
        self.__direction_angle_v = 0
        self.__direction_vector = vector(1, 0, 0)
        self.__hidden = False
        self.__color = color.red
        self.__turtle = sphere(pos=vector(
            0, 0, 0), radius=0.5, color=color.red)

    def forward(self, dist):
        """Moves turtle forward dist distance, so in the direction of the direction vector"""
        if(not self.__hidden):
            cylinder(pos=self.__turtle.pos, axis=dist*self.__direction_vector,
                     radius=self.__turtle.radius, color=self.__color)
            sphere(pos=self.__turtle.pos,
                   radius=self.__turtle.radius, color=self.__color)
        self.__turtle.pos += dist*self.__direction_vector

    def backward(self, dist):
        """Moves turtle backwar dist distance, so in the oposite direction of the direction vector"""
        if(not self.__hidden):
            cylinder(pos=self.__turtle.pos, axis=-dist*self.__direction_vector,
                     radius=self.__turtle.radius, color=self.__color)
            sphere(pos=self.__turtle.pos,
                   radius=self.__turtle.radius, color=self.__color)
        self.__turtle.pos -= dist*self.__direction_vector

    def right(self, deg):
        """Turns the turtle deg degrees to the right, changing its direction vector"""
        self.__direction_angle_h = (self.__direction_angle_h-deg)
        self.__direction_vector = Turtle3D.polarToCartesian(
            self.__direction_angle_v, self.__direction_angle_h)

    def left(self, deg):
        """Turns the turtle deg degrees to the left, changing its direction vector"""
        self.__direction_angle_h = (self.__direction_angle_h+deg)
        self.__direction_vector = Turtle3D.polarToCartesian(
            self.__direction_angle_v, self.__direction_angle_h)

    def up(self, deg):
        """Turns the turtle deg degrees upward, changing its direction vector"""
        self.__direction_angle_v = (self.__direction_angle_v+deg)
        self.__direction_vector = Turtle3D.polarToCartesian(
            self.__direction_angle_v, self.__direction_angle_h)

    def down(self, deg):
        """Turns the turtle deg degrees downward, changing its direction vector"""
        self.__direction_angle_v = (self.__direction_angle_v-deg)
        self.__direction_vector = Turtle3D.polarToCartesian(
            self.__direction_angle_v, self.__direction_angle_h)

    def hide(self):
        """Hides the turtle, so it stops making its trail"""
        self.__hidden = True
        sphere(pos=self.__turtle.pos,
                   radius=self.__turtle.radius, color=self.__color)

    def show(self):
        """Shows the turtle, so it starts making its trail"""
        self.__hidden = False

    def color(self, r, g, b):
        """Changes the turtle's trail color"""
        self.__color = vector(r, g, b)

    def home(self):
        """Puts the turtle back in the origen (its original spot)"""
        self.__turtle.pos = vector(0, 0, 0)

    def polarToCartesian(vert, hor):
        """Calculates a direction vector from 2 angles: vertical(vert) and horizontal(hor)"""
        vert_rad = (vert/180)*PI
        hor_rad = (hor/180)*PI
        return vector((cos(vert_rad) * cos(hor_rad)), sin(vert_rad),
                      (sin(hor_rad)*cos(vert_rad)))
