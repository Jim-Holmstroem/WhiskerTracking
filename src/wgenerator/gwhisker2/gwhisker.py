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

num_links=80
density=1000

bodies=[]

width=1


#
# To get it stiff:
#
# AMotor between at each joint (also at the first)
# Calculate the difference in angle between this joint and the next (first joint has a fixed angle)
#
# addTorques(t0,t1,t2) prop. to dphi (each angle, perpendicular?)
# map(lambda i:amoto.getAngle(i),range(3)) # to get all them angles (is these according to worldcoordinate, can one simply diff them?)
# 
# setMode(mode), mode must be either AMotorUser or AMotorEuler (whats the difference?)
#
# how many axis this it control? i only count 2 when on the unit sphere, is this correct?
#
# AMotor inheritancs from joint (all good baby, can still keep them joints just making em motors thats all)
#
#
#

dw=5.0/num_links #dw is the distance between the joints
for i in range(num_links):
    x=i*dw
    
    body=ode.Body(world)
    mass=ode.Mass()
    mass.setCappedCylinder(density,1,width-width*i/num_links,dw)
    
    body.setMass(mass)
    body.setPosition( (x+dw/2,2,0) )
    body.setFiniteRotationMode(1) #note important for accuracy (see doc)
    
    bodies.append(body)

joints=[]

last_body=None
for body in bodies:
    joint=ode.BallJoint(world)
    
    if last_body:
        joint.attach(last_body,body)
        joint.setAnchor( vadd(last_body.getPosition(),(dw/2,0,0)) )
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

    for body in bodies:
        x,y,z=body.getPosition()
        #pygame.draw.circle(srf,(0,0,0),coord(x,y),2,0)
        
        rot=body.getRotation()
        dx=dw*rot[0]/2.0
        dy=dw*rot[3]/2.0
        print dx,dy
        pygame.draw.line(srf,(0,0,0),coord(x-dx,y-dy),coord(x+dx,y+dy))
        
        #a,b,c,d = body.getQuaternion()
        #pygame.draw.line(srf,(0,0,0),coord(x,y),coord(x+a,y+d))

    for joint in joints:
        x,y,z=joint.getAnchor()
        pygame.draw.circle(srf,(255,0,0),coord(x,y),2,0)


    pygame.display.flip()
    
    world.step(dt)

