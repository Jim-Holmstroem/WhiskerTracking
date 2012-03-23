import pygame
from pygame.locals import *
import ode
import math

WIDTH=1024
HEIGHT=768

def coord(x,y):
    return int(WIDTH/2+WIDTH/10*x), int(HEIGHT/2-HEIGHT/10*y)

# Initialize pygame
pygame.init()

# Open a display
srf = pygame.display.set_mode((WIDTH,HEIGHT))

# Create a world object
world = ode.World()
world.setGravity((0,-0.1,0))

num_balls = 50
total_weight=2000

bodies=[]

dx=5.0/num_balls
for i in range(1,num_balls):
    x=i*dx
    body = ode.Body(world)
    mass = ode.Mass()
    mass.setSphere(1.1*total_weight-i*total_weight/num_balls,0.05)
    body.setMass(mass)
    body.setPosition( (x,2,0) )
    bodies.append(body)


joints=[]

last_body=None
for body in bodies:
    
    if(last_body):
        joint = ode.BallJoint(world)
        joint.attach(last_body,body)
        joint.setAnchor( last_body.getPosition() )
    else:
        joint= ode.HingeJoint(world)
        joint.attach(ode.environment,body)
        joint.setAnchor( (0,2,0) )
        joint.setAxis( (0,0,1) )
        joint.setParam(ode.ParamVel,1)
        joint.setParam(ode.ParamFMax,1)
    
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


    



    for body in bodies:
        x,y,z=body.getPosition()
        pygame.draw.circle(srf, (55,0,200),coord(x,y),int(math.sqrt(100.0*body.getMass().mass)),0)

#    for joint in joints:
#        x,y,z=joint.getAnchor()
#        pygame.draw.circle(srf,(200,0,55),coord(x,y),5,0)
#        x,y,z=joint.getAnchor2()
#        pygame.draw.circle(srf,(100,0,100),coord(x,y),2,0)


    pygame.display.flip()
    
    # Next simulation step
    world.step(dt)

    # Try to keep the specified framerate    
   # clk.tick(fps)
