import pygame
from pygame.locals import *
import ode
import math

import itertools

WIDTH=1024
HEIGHT=768

def vadd(vi,vj):
    return tuple(map(lambda (i,j):i+j,zip(tuple(vi),tuple(vj))))

def coord(x,y):
    return int(WIDTH/2+WIDTH/10*x), int(HEIGHT/2-HEIGHT/10*y)

# Initialize pygame
pygame.init()

# Open a display
srf = pygame.display.set_mode((WIDTH,HEIGHT))

# Create a world object
world = ode.World()
world.setGravity((0,-0.1,0))

num_links=100
density=1000

bodies=[]

width=1

dx=5.0/num_links
for i in range(num_links):
    x=i*dx
    
    body=ode.Body(world)
    mass=ode.Mass()
    mass.setCappedCylinder(density,1,width,dx)
    
    body.setMass(mass)
    body.setPosition( (x+dx/2,2,0) )

    bodies.append(body)


joints=[]

last_body=None
for body in bodies:
    joint=ode.BallJoint(world)
    
    if last_body:
        joint.attach(last_body,body)
        joint.setAnchor( vadd(last_body.getPosition(),(dx/2,0,0)) )
    else:
        joint.attach(ode.environment,body)
        joint.setAnchor( (0,2,0) )

    joints.append(joint)
    last_body=body


# Simulation loop...


fps = 100
dt = 1.0/fps
loopFlag = True
clk = pygame.time.Clock()

w=0

while loopFlag:
    events = pygame.event.get()
    for e in events:
        if e.type==QUIT:
            loopFlag=False
        if e.type==KEYDOWN:
            loopFlag=False

    # Clear the screen
    srf.fill((255,255,255))

    
    #====DRAW=======

    for joint in joints:
        x,y,z=joint.getAnchor()
        pygame.draw.circle(srf,(55,0,200),coord(x,y),5,0)


    pygame.display.flip()
    
    # Next simulation step
    world.step(dt)

    # Try to keep the specified framerate    
   # clk.tick(fps)
