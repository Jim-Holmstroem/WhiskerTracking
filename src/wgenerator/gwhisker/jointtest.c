#include <stdio.h>
#include <iostream>
#include <sstream>
#include <string>

#include <chipmunk/chipmunk.h>

#include <cairo/cairo.h>



static cpBody *
addBar(cpSpace* space, cpVect pos, cpVect boxOffset)
{
    cpFloat mass = 2.0f;
    cpVect a = cpv(0,  30);
    cpVect b = cpv(0, -30);

    cpBody *body = cpSpaceAddBody(space, cpBodyNew(mass, cpMomentForSegment(mass, a, b)));
    cpBodySetPos(body, cpvadd(pos, boxOffset));

    cpShape *shape = cpSpaceAddShape(space, cpSegmentShapeNew(body, a, b, 5.0f));
    cpShapeSetElasticity(shape, 0.0f);
    cpShapeSetFriction(shape, 0.7f);

    return body;
}


static void 
drawConstraint(cpConstraint *constraint,void* unused)
{
    cpBody *body_a = constraint->a;
    cpBody *body_b = constraint->b;
    
    const cpConstraintClass klass = constraint->klass;
    if( klass==cpDampedRotarySpringGetClass())
    {
        printf("not dampedrotarystpring :(");
        return;
    }    

    cpDampedRotarySpring *joint=(cpDampedRotarySpring*)constraint;

    cpVect a = cpvadd(body_a->p,cpvrotate(joint->anchr1,body_a->rot));
    cpVect b = cpvadd(body_b->p,cpvrotate(joint->anchr2,body_b->rot));

    printf("[%5.2f,%5.2f,%5.2f,%5.2f]",a.x,a.y,b.x,b.y);


}


int
main(void){
    
//=======SETUP SPACE===========
    cpVect gravity = cpv(0, -100);
     
    cpSpace *space = cpSpaceNew();
    cpSpaceSetGravity(space, gravity);
    cpSpaceSetSleepTimeThreshold(space,0.5f);
  

//======BUILDING=================

    cpBody *staticBody = cpSpaceGetStaticBody(space);


    cpBody *body1,*body2; 

    cpVect offset=cpv( 10, 10);
    cpVect posA = cpv( 50, 60);
    cpVect posB = cpv(110, 60);
   

    body1=addBar(space,posA,offset);
    body2=addBar(space,posB,offset);

    cpSpaceAddConstraint(space,cpPivotJointNew(body1,staticBody,cpvadd(offset,posA)));
    cpSpaceAddConstraint(space,cpPivotJointNew(body2,staticBody,cpvadd(offset,posB)));
    cpSpaceAddConstraint(space,cpDampedRotarySpringNew(body1,body2,0.0f,3000.0f,60.0f));


//=======CONSTANTS=============

    cpFloat timeStep = 1.0/60.0;

    int WIDTH=512;
    int HEIGHT=512;

//========CAIRO INIT===================
    cairo_surface_t *surface;
    cairo_t *cr;
    surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32,WIDTH,HEIGHT);
    cr=cairo_create(surface);
    cr = cairo_create(surface);
    cairo_translate(cr,WIDTH/2,HEIGHT/2);

//=======RENDER LOOP===================
    int frame=0;


    for(cpFloat time = 0; time < 4; time += timeStep,++frame){
       cpSpaceEachConstraint(space,drawConstraint,NULL); // could one simple send the cairocontext instead of null and typeconvert "unused" accordingly  
/*
        cpVect pos = cpBodyGetPos(ballBody);
        cpVect vel = cpBodyGetVel(ballBody);

        cairo_set_source_rgba(cr,1,1,1,1);
        cairo_rectangle(cr,-256,-256,512,512); 
        cairo_fill(cr);

        cairo_set_source_rgba(cr,0,0,0,0.7);
        cairo_arc(cr,pos.x,pos.y,2,0,2*M_PI);
        cairo_fill(cr);

        cairo_set_source_rgba(cr,1,0,0,0.7);
        cairo_rectangle(cr,-20,-5,2*20,2*5);
        cairo_set_line_width(cr,1);
        cairo_stroke(cr);
*/


//=========OUTPUT======================================

        std::stringstream ss;
        ss.fill('0');
        ss.width(5);
        ss << frame; 
        cairo_surface_write_to_png(surface,("whiskeroutput.pngvin/frame-"+ss.str()+".png").c_str());

//=========DEBUG OUTPUT=====================

   /*     printf(
            "[%5.2f,(%5.2f,%5.2f),(%5.2f,%5.2f)]\n",
            time, pos.x, pos.y, vel.x, vel.y
        );
    */
//=======STEP FORWARD=======================

        cpSpaceStep(space, timeStep);
    }
//=======CLEANUP=========================== 
    cairo_destroy(cr);
    cairo_surface_destroy(surface);
    
    
    cpSpaceFree(space);
    

    return 0;
}
