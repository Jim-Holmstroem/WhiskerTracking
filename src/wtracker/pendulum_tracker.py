__all__ = ["PendulumTracker"]

from wdb import StateTransitionDatabase
from wmedia import wvideo
from wmedia.pendulum import PendulumAnimator
import cProfile
import numpy
import os
from tracker import Tracker

class PendulumTracker(Tracker):
    
    def __init__(self, db, video):
        Tracker.__init__(self, db, video)
#        self.renderer = PendulumRenderer(400, 10)
        
    def make_animator(self, main_particles, particles, intermediate_particles):
        l = 400.0/self.video.image_shape()[1]
        radius = 10.0/self.video.image_shape()[1]
        return PendulumAnimator(main_particles, particles, intermediate_particles, l, radius)
    
#    def render(self, context, particle):
#        self.renderer.render(context, particle[0])
#    
    def goodness(self, particle, image):
        return 1
#        return wimage()*image
    
    def sample(self, prev_particle):
        return self.db.sample_weighted_average(prev_particle)
    
def cProfile_test(movie_id):
    dataset = "square_accelerating"
    movie = dataset + "_" + str(movie_id)
    save_img_dir = os.path.join("run", "square_tracker_bounce-%i.pngvin"%(movie_id))
    if(not os.path.exists(save_img_dir)):
        os.makedirs(save_img_dir)
    video = wvideo(os.path.join("video", movie+".pngvin")) # Dimensions: x, y, rgba
    db = StateTransitionDatabase(dataset)
    
    correct_states = numpy.load(os.path.join("video", movie+".pngvin", "state_sequence.npy"))
    
    PendulumTracker(db, video).run(correct_states[0,:], 100)

if __name__ == "__main__":
#    cProfile.run("run(7)")
#    cProfile.run("run(8)")
#    cProfile.run("run(9)")
    cProfile.run("cProfile_test(0)")
