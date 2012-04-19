from square_tracker_bounce import BounceTracker
from wdb import StateTransitionDatabase
from wgui.wlayermanager import wlayermanager
from wgui.wwindow import wwindow
from wmedia import wvideo
from wmedia.square_particles_animator import square_particles_animator
import gtk
import numpy
import os

class TrackerTester:
    
    TEST_DATA_BASE_DIR = "video"
    
    def __init__(self, tracker_class, video_name, database_name):
        video_path = os.path.join(self.TEST_DATA_BASE_DIR, video_name + ".pngvin")
        
        self.correct_states = numpy.load(os.path.join(video_path, "state_sequence.npy"))
        self.video = wvideo(video_path)
        self.db = StateTransitionDatabase(database_name)
        
        self.tracker = tracker_class(self.db)
    
    def run(self):
        print "Running tracking test"
        self.track = self.tracker.run(self.video, self.correct_states[0], 1000)
        
        difference_from_correct = self.correct_states - self.track
        cum_diff = difference_from_correct.cumsum(axis=0)
        
        print cum_diff[-1,:]
        print "Finished tracking test"
    
    def animate(self):
        print "Animating test results"
        spa = square_particles_animator(None, 50, self.track, main_particle_color=(255,0,0))
        layer_manager = wlayermanager()
        layer_manager.add_layer(self.video)
        layer_manager.add_layer(spa)
        
        win = wwindow(layer_manager)
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
        print "Done animating test results"

if __name__ == "__main__":
    tester = TrackerTester(BounceTracker, "square_accelerating_0", "square_accelerating")
    tester.run()
    tester.animate()
