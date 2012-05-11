__all__ = ["Tracker"]

from pf import pf
import numpy

class Tracker:
    
    def __init__(self, db, video, start_states, num_particles, *other_args, **other_kwargs):
        self.db = db
        self.video = video
        self.num_frames = len(self.video)
        self.start_states = start_states
        self.num_objects = len(self.start_states)
        self.num_particles = num_particles

        self.tracks = [None]*self.num_objects
        self.animators = [None]*self.num_objects
        self.resampled_particles = [None]*self.num_objects
        self.preresampled_particles = [None]*self.num_objects
        self.highest_weight_particles = []
    
    def goodness(self, particle, image):
        raise NotImplementedError("This class is abstract!")
    
    def sample(self, prev_particle):
        raise NotImplementedError("This class is abstract!")
    
    def make_animators(self):
        raise NotImplementedError("This class is abstract!")

    def preprocess_image(self, image):
        return image

    def get_track(self, i):
        return self.tracks[i]

    def get_animator(self, i):
        return self.animators[i]

    def track_object(self, obj_i, start_state):
        print "Tracking object %i of %i"%(obj_i+1, len(self.start_states))
        print "Start state for object %i is %s."%(obj_i+1, start_state)
        
        self.preresampled_particles[obj_i] = numpy.zeros((self.num_frames, self.num_particles, start_state.size))
        self.resampled_particles[obj_i] = numpy.zeros((self.num_frames, self.num_particles, start_state.size))
        self.highest_weight_particles.append([start_state])
        
        particles = numpy.array([start_state]*self.num_particles)
        
        track = numpy.zeros((self.num_frames, start_state.size))
        track[0,:] = start_state
        self.preresampled_particles[obj_i][0] = particles
        self.resampled_particles[obj_i][0] = particles
        
        for i, frame in enumerate(self.video[1:], 1):
            particles, intermediate_particles = pf(particles, self.preprocess_image(frame), self.goodness, sampling_function=self.sample, resampling_function=self.save_highest_weight_particle_and_resample)
            track[i,:] = particles.mean(axis=0)
            self.resampled_particles[obj_i][i] = particles

            print "Tracked frame %i of %i"%(i+1, self.num_frames)

        self.highest_weight_particles[obj_i] = numpy.array(self.highest_weight_particles[obj_i])
        
        print "Tracking complete."
        print
        
        self.tracks[obj_i] = track

    def run(self):
        print "%s tracking with %i particles..."%(self.__class__.__name__, self.num_particles)
        print

        map(self.track_object, xrange(len(self.start_states)), self.start_states)

        self.animators = self.make_animators()
    
    def export_results(self, pngvin_dir):
        from wgui import wlayermanager
        
        print "Exporting results as PNGVIN video..."
        wl = wlayermanager()
        wl.add_layer(self.video)
        map(wl.add_layer, self.animators)
        wl.exportPNGVIN(pngvin_dir)
        print "Export complete."
        print
