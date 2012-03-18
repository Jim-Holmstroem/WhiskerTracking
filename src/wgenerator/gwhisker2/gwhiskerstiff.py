import pygame
from pygame.locals import *
import ode
import math
from math import cos,sin
import itertools as itt

WIDTH=1024
HEIGHT=768

class color:
    gray=(128,128,128)
    red=(255,0,0)
    green=(0,255,0)
    blue=(0,0,255)


def vadd(vi,vj):
    return tuple(map(lambda (i,j):i+j,zip(tuple(vi),tuple(vj))))

def coord(x,y):
    return int(WIDTH/2+WIDTH/10*x), int(HEIGHT/2-HEIGHT/10*y)

def rotation_matrix(phi,theta,psi):
    """
        Returns a vector of 9 elements containing the rotation matrix (that is 3x3)
    """
    return [ cos(theta)*cos(psi) , -cos(phi)*sin(psi)+sin(phi)*sin(theta)*cos(psi) , sin(phi)*sin(psi)+cos(phi)*sin(theta)*cos(psi) , cos(theta)*sin(psi) , cos(phi)*cos(psi)+sin(phi)*sin(theta)*sin(psi) , -sin(phi)*cos(psi)+cos(phi)*sin(theta)*sin(psi) , -sin(theta) , sin(phi)*cos(theta) , cos(phi)*cos(theta) ]

print rotation_matrix(0,0,0)


def interpolate(p):
    """
    Returns the points between the list p
    """
    pass


class whisker:
    bodies=[]
    joints=[]


    def __init__(self,world,pos=(0,0,0),direction=(0,0,0),length=5.0,width=1,num_links=32,density=128): 
        """
            @param world - ode.World in which the whisker is created in
            @param pos - the start position of the whisker
            @param direction - the euler angle to define the direction of the whisker
            @param length - the length of the whisker
            @param width - almost the width att the root
            @param num_links - the number of joints the whisker should be simulated with
            @param density - the density of the  whisker, the mass will be calculated accordingly with the size of the whisker

        """
        
        dw=length/num_links
        for i in range(num_links):
            x=i*dw

            body=ode.Body(world)
            mass=ode.Mass()
            mass.setCappedCylinder(density,1.1*width-width*float(i)/num_links,dw)
            body.setMass(mass)
          

            #body.
            body.setFiniteRotationMode(1)

            bodies.append(body)

        



pygame.init()
srf = pygame.display.set_mode((WIDTH,HEIGHT))

world = ode.World()
world.setGravity((9,1,0))

num_links=32
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

fps = 2000.0
dt = 1.0/fps
loopFlag = True

w=0

#
# Methods used not listed in reference litterate:
# 
# Joint.getAngle1()
# Joint.getAngle1Rate() #BUGGY DONT USE
#
# remember to divide impulse (that is all) torques and forces by dt to get force dt independent
#


damping = 20.0

#stiffness=10.0 works nicely

stiffness=20.0



oldAngle1=joint.getAngle1() #HACK to go around the need of joint.getAngle1Rate()
oldAngle2=joint.getAngle2()

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
        width=1+int(math.sqrt(body.getMass().mass/dw)/8)
        pygame.draw.line(srf,(0,0,0),coord(x-dx,y-dy),coord(x+dx,y+dy),width)
        pygame.draw.circle(srf,(0,255,0),coord(x,y),2,0)


    first_joint=True
    for joint in joints:
        x,y,z=joint.getAnchor()

        if(first_joint):
            first_joint=False
        else:
            joint.addTorques(-stiffness*joint.getAngle1()/dt,-stiffness*joint.getAngle2()/dt)
            joint.addTorques(damping*(oldAngle1-joint.getAngle1())/dt,damping*(oldAngle2-joint.getAngle2())/dt)

        #update oldAngles
        oldAngle1=joint.getAngle1()
        oldAngle2=joint.getAngle2()

        pygame.draw.circle(srf,(255,0,0),coord(x,y),2,0)

        #draw grid
        M=5
        for q in range(-M,M+1):
            pygame.draw.line(srf,color.gray,coord(-M,q),coord(M,q),1) #x
            pygame.draw.line(srf,color.gray,coord(q,-M),coord(q,M),1) #y

        #draw the coordinate system
        pygame.draw.line(srf,(0,128,128),coord(0,0),coord(1,0),2)
        pygame.draw.line(srf,(0,128,128),coord(0,0),coord(0,1),2)

        g=world.getGravity()
        pygame.draw.line(srf,(128,128,0),coord(0,0),coord(g[0],g[1]),2)

    pygame.display.flip()
    world.step(dt)

