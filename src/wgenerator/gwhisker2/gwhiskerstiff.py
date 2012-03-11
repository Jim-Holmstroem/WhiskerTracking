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

pygame.init()
srf = pygame.display.set_mode((WIDTH,HEIGHT))

world = ode.World()
world.setGravity((9,1,0))

num_links=16*2
density=128

bodies=[]

width=1

dw=5.0/num_links #dw is the distance between the joints
for i in range(num_links):
    x=i*dw
    
    body=ode.Body(world)
    mass=ode.Mass()
    mass.setCappedCylinder(density,1,1.1*width-width*float(i)/num_links,dw)
    
    body.setMass(mass)
    body.setPosition( (x+dw/2,2,0) )
    body.setFiniteRotationMode(1) #note important for accuracy (see doc)
        
    bodies.append(body)

joints=[]

last_body=None
for body in bodies:
    joint=ode.UniversalJoint(world)

    if last_body:
        joint.attach(last_body,body)
        joint.setAnchor( vadd(last_body.getPosition(),(dw/2,0,0)) )
        
    else:
        joint.attach(ode.environment,body)
        joint.setAnchor( (0,2,0) )

    joint.setAxis1((0,0,1))
    joint.setAxis2((0,1,0))
    joints.append(joint)    

    last_body=body

fps = 500
dt = 1.0/fps
loopFlag = True

w=0

#
# Methods used not listed in reference litterate:
# 
# Joint.getAngle1()
# Joint.getAngle1Rate()
#
# remember to divide impulse (that is all) torques and forces by dt to get force dt independent
#




damping = 0.01
stiffness=0.01


while loopFlag:
    events = pygame.event.get()
    for e in events:
        if e.type==QUIT or e.type==KEYDOWN:
            print "EXIT"

    srf.fill((255,255,255))

    for body in bodies:
        x,y,z=body.getPosition()
        rot=body.getRotation()
        dx=dw*rot[0]/2.0
        dy=dw*rot[3]/2.0
        width=int(math.sqrt(body.getMass().mass/dw)/8)
        pygame.draw.line(srf,(0,0,0),coord(x-dx,y-dy),coord(x+dx,y+dy),width)

    for joint in joints:
        x,y,z=joint.getAnchor()

        joint.addTorques(-stiffness*joint.getAngle1()/dt,-stiffness*joint.getAngle2()/dt)
        joint.addTorques(-damping*joint.getAngle1Rate()/dt,-damping*joint.getAngle2Rate()/dt)
        
        pygame.draw.circle(srf,(255,0,0),coord(x,y),2,0)

        #debug output how much i am adding as torque and if it has descired effect
        #can I some how make damping and stifness work together to get a fast shackdown as in mekaniken (whats it called?, the fastest possible stopping of distrubtion)

        pygame.draw.line(srf,(0,255,0),coord(x,y),coord(x+1,y+1),1) 

    pygame.display.flip()
    world.step(dt)

