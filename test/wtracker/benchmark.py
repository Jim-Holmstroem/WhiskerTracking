from square_tracker_bounce import BounceTracker
from tracker.pendulum_tracker import PendulumTracker
from wdb import StateTransitionDatabase
from wgui.wlayermanager import wlayermanager
from wgui.wwindow import wwindow
from wmedia import wvideo
import gtk
import numpy
import os

class TrackerBenchmark:
    
    TEST_DATA_BASE_DIR = "video"
    
    def __init__(self, tracker_classes, video_name, database_name, num_particles=100):
        video_path = os.path.join(self.TEST_DATA_BASE_DIR, video_name + ".pngvin")
        
        self.correct_states = numpy.load(os.path.join(video_path, "state_sequence.npy"))
        self.video = wvideo(video_path)
        self.db = StateTransitionDatabase(database_name)
        self.num_particles = num_particles

        self.trackers = map(lambda tracker_class:tracker_class(self.db, self.video), tracker_classes)
    
    def run(self):
        print "Running tracking test"
        self.tracks = map(lambda tracker:tracker.run(self.correct_states[0], self.num_particles), self.trackers)
        
        differences_from_correct = map(lambda track:numpy.abs(self.correct_states - track), self.tracks)
        sum_diffs = map(lambda diff:diff.sum(axis=0), differences_from_correct)
        
        print sum_diffs
        print "Finished tracking test"
    
    def animate(self, i):
        print "Animating test results"
        layer_manager = wlayermanager()
        layer_manager.add_layer(self.video)
        layer_manager.add_layer(self.trackers[i].get_animator())
        
        win = wwindow(layer_manager)
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
        print "Done animating test results"

if __name__ == "__main__":
    tracker_classes = [BounceTracker]
    tester = TrackerBenchmark(tracker_classes, "square_accelerating_0", "square_accelerating", 10)
    tester.run()
    tester.animate(0)
