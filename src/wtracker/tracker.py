import numpy
from pf import pf

class Tracker:
    ANIMATOR_CLASS = None
    
    def __init__(self, db, video):
        self.db = db
        self.video = video
        self.num_frames = len(self.video)
    
    def goodness(self, particle, image):
        raise NotImplementedError("This class is abstract!")
    
    def sample(self, prev_particle):
        raise NotImplementedError("This class is abstract!")
    
    def make_animator(self, main_particles, particles, intermediate_particles):
        raise NotImplementedError("This class is abstract!")
    
    def get_animator(self):
        return self.animator
    
    def run(self, start_state, num_particles):
        
        print "Tracking..."
        
        particles = numpy.array([start_state]*num_particles)
        
        track = numpy.zeros((self.num_frames, start_state.size))
        track[0,:] = start_state
        all_particles = [None]*self.num_frames
        all_intermediate_particles = [None]*self.num_frames
        all_particles[0] = particles
        all_intermediate_particles[0] = particles
        
        for i, frame in enumerate(self.video[1:], 1):
            particles, intermediate_particles = pf(particles, frame.get_array(), self.goodness, sampling_function=self.sample)
            track[i,:] = particles.mean(axis=0)
            all_particles[i] = particles
            all_intermediate_particles[i] = intermediate_particles
            print "Tracked frame %i of %i"%(i+1, self.num_frames)
        
        print "Tracking complete."
        
        self.make_animator(track, all_particles, all_intermediate_particles)
        
        return track
    
    def render_results(self, context, frame_i):
        self.get_animator().render(context, frame_i)
