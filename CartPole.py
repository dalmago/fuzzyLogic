#!/usr/bin/env python2.7

import pygame
import pygame.image
import pygame.transform
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
import pymunk.util
from pymunk import Vec2d
from math import *
import os

class CartPole():
    '''
    CartPole implements a simulation of the classic
    cart-pole inverted pendulum experiment using
    PyMunk for physics and PyGame for display
    '''
    def __init__(self, screen_width = 800, \
            screen_height = 600, gravity=200.0, \
            show_graphics=True):
        '''
        This is the constructor
        '''
        # Save member variables
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gravity = gravity
        self.show_graphics = show_graphics
        self.proportional_cart_height = (1.0 / 3.0)
        self.cart_group = 1
        self.pos_center = Vec2d(self.screen_width/2.0, \
            self.screen_height*self.proportional_cart_height)
        self.pos_left = Vec2d(0.0, \
            self.screen_height*self.proportional_cart_height)
        self.pos_right = Vec2d(self.screen_width, \
            self.screen_height*self.proportional_cart_height)
        self.thing = None
        self.thing_movepos = Vec2d(0.0,0.0)
        self.thing_clickpos = Vec2d(0.0,0.0)
        self.spring = None
        self.delay = 1 / 60.0
        self.cart_velocity_target = 0.0
        self.running = True
        self.cart_max_position = 605.0
        self.cart_min_position = 75.0
        self.max_length = self.cart_max_position - self.cart_min_position
        # Initialize PyGame (if required)
        if self.show_graphics:
            self._init_PyGame()
            self._load_images()
        # Initialize PyMunk
        self._init_PyMunk()
        # Create the floor
        self._init_floor()
        # Create the cart
        self._init_cart()
        # Create the pole
        self._init_pole()
        # Create the joints
        self._init_joints()
    def _init_PyGame(self):
        '''
        PyGame initialization
        '''
        # Initialize PyGame
        pygame.init()
        self.screen = \
        pygame.display.set_mode((self.screen_width,
            self.screen_height))
        self.clock = pygame.time.Clock()
    def _load_images(self):
        self.img_background = \
            pygame.image.load(os.path.join('Art','background.png')).convert_alpha()
        self.img_cart = \
            pygame.image.load(os.path.join('Art','cart.png')).convert_alpha()
        self.img_screw = \
            pygame.image.load(os.path.join('Art','screw.png')).convert_alpha()
        self.img_base = \
            pygame.image.load(os.path.join('Art','base.png')).convert_alpha()
        self.img_pole = \
            pygame.image.load(os.path.join('Art','pole.png')).convert_alpha()
        self.pole_sprite = []
        for i in range(720):
            self.pole_sprite.append(\
                pygame.transform.rotate(self.img_pole, float(i)/2.0-90.0).convert_alpha())
    def _init_PyMunk(self):
        '''
        PyMunk initialization
        '''
        # Create the pymunk space
        self.space = pymunk.Space()
        self.space.gravity = (0, -self.gravity)
    def _cart_calc_xy_pos(self):
        '''
        Utility funciton calculates x,y position
        of the cart based on its position on the
        linear movement
        '''
        return (self.screen_width/2.0, \
            self.screen_height * self.proportional_cart_height)
    def _init_floor(self):
        '''
        Creates the floor
        '''
        # Floor body with no mass, because it's static
        body = pymunk.Body()
        # Body's cg position doesn't matter, it won't
        # move or rotate or collide, it's only a reference
        # for the slide joint of the cart
        body.position = self.pos_center
        # Create the floor geometry
        self.floor = pymunk.Segment(body, \
            (-self.screen_width/2.0, 0.0), \
            ( self.screen_width/2.0, 0.0), \
#            (-self.screen_width/2.0, self.pos_center[1]), \
#            ( self.screen_width/2.0, self.pos_center[1]), \
            1)
        # Set floor contact group
        self.floor.group = self.cart_group
        # Add floor to space
        self.space.add(self.floor)
    def _init_cart(self, cart_width=75.0, cart_height=30.0, \
            cart_mass=2000.0):
        '''
        Creates the cart
        '''
        # Centre of gravity of the cart
        cg = Vec2d(0,0)
        # Create the polygon of the cart
        vertices = []
        vertices.append((-cart_width/2.0 - 10.0,  cart_height/2.0))
        vertices.append(( cart_width/2.0 - 20.0,  cart_height/2.0))
        vertices.append(( cart_width/2.0 - 20.0, -cart_height/2.0 - 50.0))
        vertices.append((-cart_width/2.0 - 10.0, -cart_height/2.0 - 50.0))
        # Infinite moment for the cart
        cart_moment = float('inf')
        # Create the body of the cart
        body = pymunk.Body(cart_mass, cart_moment)
        body.position = cg + self.pos_center
        # Create the geometry of the cart
        self.cart = pymunk.Poly(body, vertices)
        self.cart.group = self.cart_group
        # Add body and shape to space
        self.space.add(self.cart, body)
    def _init_pole(self, pole_width=15.0, pole_height=300.0, \
            pole_mass=750.0, pole_moment=50.0, pole_initial_angle=pi):
        '''
        Creates the pole
        '''
        # Centre of gravity of the pole
        cg = Vec2d(0,-pole_height/2.0).rotated(pole_initial_angle)
        # Create the polygon of the pole 
        vertices = []
        vertices.append(Vec2d(-pole_width/2.0, \
                 pole_height/2.0).rotated(pole_initial_angle))
        vertices.append(Vec2d( pole_width/2.0, \
                 pole_height/2.0).rotated(pole_initial_angle))
        vertices.append(Vec2d( pole_width/2.0, \
                -pole_height/2.0).rotated(pole_initial_angle))
        vertices.append(Vec2d(-pole_width/2.0, \
                -pole_height/2.0).rotated(pole_initial_angle))
        # Create the body of the pole
        body = pymunk.Body(pole_mass, pole_moment)
        body.position = cg + self._cart_calc_xy_pos()
        # Create the geometry of the pole
        self.pole = pymunk.Poly(body, vertices)
        self.pole.group = self.cart_group
        # Add body and shape to space
        self.space.add(self.pole, body)
    def _init_joints(self):
        # Creates the slider
        self.rails1 = pymunk.GrooveJoint(self.floor.body, self.cart.body, \
            self.pos_left + Vec2d(42.0,0), self.pos_right + Vec2d(-162.0,0), \
            self.cart.body.position - (35.0, 0.0))
        self.rails2 = pymunk.GrooveJoint(self.floor.body, self.cart.body, \
            self.pos_left + Vec2d(42.0,0), self.pos_right + Vec2d(-162.0,0), \
            self.cart.body.position + (35.0, 0.0))
        # Add the slider joints to the space
        self.space.add(self.rails1, self.rails2)
        # Creates the pole's pivot
        self.pivot = pymunk.PivotJoint(self.cart.body, self.pole.body, \
                self._cart_calc_xy_pos())
        # Add the pivot joint to the space
        self.space.add(self.pivot)
    def _invy(self, pos):
        return pos[0], self.screen_height - pos[1]
    def step(self, delta):
        '''
        Simulation step
        '''
        if (self.cart_velocity_target > 0.0 \
            and self.cart.body.position[0] < self.cart_max_position) \
            or (self.cart_velocity_target < 0.0 \
            and self.cart.body.position[0] > self.cart_min_position):
            e = Vec2d(self.cart_velocity_target, 0.0) - self.cart.body.velocity
            self.cart.body.apply_impulse(e*500.0)
            # self.cart.body.velocity = Vec2d(self.cart_velocity_target, 0.0)
        else:
            self.cart.body.velocity = Vec2d(0.0, 0.0)
        self.space.step(delta)
        if self.show_graphics:
            self.draw(delta)
    def draw_pole(self, pos, angle):
        angle = angle - pi/2.0
        index = int(2.0*float(angle)*180.0/pi) % 720
        bb = self.pole_sprite[index].get_rect()
        offset = 2.5 * 180.0 / pi
        center_pos = (float(bb.width)/2.0, float(bb.height)/2.0)
        #pos = (pos[0] - center_pos[0]/2.0 + (579 / 2) * cos(angle), \
        #       pos[1] - center_pos[1]/2.0 + (579 / 2) * sin(angle))
        pos = (float(pos[0]) - center_pos[0] - (145.0) * cos(angle), \
               float(pos[1]) - center_pos[1] + (145.0) * sin(angle))
        self.screen.blit(self.pole_sprite[index], \
                Rect(pos[0], pos[1], bb.width, bb.height))
    def draw(self, delta):
        '''
        Draws stuff on the screen
        '''
        if self.spring:
            if self.spring in self.space.constraints:
                self.space.remove(self.spring)
                self.spring = None
        if self.thing:
            self.spring = pymunk.DampedSpring(self.thing.body, self.floor.body, \
                self.thing_clickpos_rel, \
                self.floor.body.world_to_local(self.thing_movepos), \
                0.0, 3000.0, 0.1)
            self.space.add(self.spring)
        self.screen.fill(THECOLORS['white'])
        # Background
        self.screen.blit(self.img_background, \
            pygame.Rect(0, 0, self.screen_width, self.screen_height))
        # Screw
        self.screen.blit(self.img_screw, \
            pygame.Rect(- 600 + self.cart.body.position[0] \
                , 409, 1200, 60))
        # Base
        self.screen.blit(self.img_base, \
            pygame.Rect(0, 0, self.screen_width, self.screen_height))
        # Cart
        self.screen.blit(self.img_cart, \
            pygame.Rect(- 50 + self.cart.body.position[0] \
                , 387, 78, 70))
        # Pole
        self.draw_pole((self.cart.body.position[0], 400), \
            self.pole.body.angle)
        #pymunk.pygame_util.draw_space(self.screen, \
        #        self.space)
        # Spring
        if self.thing:
            pygame.draw.line(self.screen, THECOLORS['black'], \
                self._invy(self.thing.body.local_to_world(self.thing_clickpos_rel)), \
                self._invy(self.thing_movepos))
        pygame.display.flip()
        self.clock.tick(1.0 / delta)
    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                self.thing_clickpos = Vec2d(self._invy(event.pos))
                self.thing_movepos = self.thing_clickpos
                self.thing = self.space.point_query_first(self.thing_clickpos)
                if self.thing:
                    self.thing_clickpos_rel = \
                        self.thing.body.world_to_local(self.thing_clickpos)
            elif event.type == MOUSEBUTTONUP:
                if self.thing:
                    self.thing = None
                    if self.spring:
                        self.space.remove(self.spring)
            elif event.type == MOUSEMOTION:
                if self.thing:
                    self.thing_movepos = Vec2d(self._invy(event.pos))
    def get_angle(self):
        angle = self.pole.body.angle % (2.0*pi)
        if angle > pi:
            angle = angle - 2.0*pi
        return angle
    def get_angular_velocity(self):
        return self.pole.body.angular_velocity
    def get_position(self):
        return (self.cart.body.position[0] - self.cart_min_position) * \
                1000.0 / self.max_length
    def set_velocity(self, velocity):
        self.cart_velocity_target = velocity * 1000.0 / self.max_length;
    def run(self):
        while self.running:
            self.step(1.0/60.0)
            self.events()

#cp = CartPole()
#cp.run()

