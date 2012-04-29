from tracker import Tracker
from wdb import StateTransitionDatabase
from wimageprocessing.imageprocessing import abs_edge
from wmedia import wvideo, wimage
from wview.pendulum import PendulumLayer, PendulumAnimator
import cProfile
import math
import numpy
import os
#__all__ = ["PendulumTracker"]

class PendulumTracker(Tracker):
    
    def __init__(self, db, video):
        Tracker.__init__(self, db, video)
        self.l = 400.0/self.video.image_shape()[1]
        self.radius = 24.0/self.video.image_shape()[1]
        self.renderer = PendulumLayer(self.l, self.radius)
        
    def make_animator(self, main_particles, particles, intermediate_particles):
        return PendulumAnimator(main_particles, particles, intermediate_particles, self.l, self.radius)
    
#    def render(self, context, particle):
#        self.renderer.render(context, particle[0])
#    
    def goodness(self, particle, image):
#        return 1
        mask = wimage(PendulumLayer(particle))
        processed_image = wimage(image)
        
        mask_sum = mask.sum()
        if mask_sum == 0:
            return 0
#        mask = wimage(PendulumLayer(particle)).transform(abs_edge).blur(3)
#        processed_image = wimage(image).transform(abs_edge).blur(3)
        return (mask*processed_image).sum()/(255*mask_sum)
#        return wimage()*image
    
    def sample(self, prev_particle):
        return self.db.sample_weighted_average(prev_particle) + numpy.random.normal(0, math.radians(5), prev_particle.shape)

class PendulumTrackerGoodnessSquared(PendulumTracker):
    def goodness(self, particle, image):
        return PendulumTracker.goodness(self, particle, image)**2
    
class PendulumTrackerGoodnessCubed(PendulumTracker):
    def goodness(self, particle, image):
        return PendulumTracker.goodness(self, particle, image)**3
    
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
