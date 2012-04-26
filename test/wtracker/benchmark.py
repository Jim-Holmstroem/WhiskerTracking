from common import make_video_path
from common.settings import make_run_path
from wdb import StateTransitionDatabase
from wgui.wlayermanager import wlayermanager
from wgui.wwindow import wwindow
from wmedia import wvideo
import gtk
import numpy
import os
import wtracker

class TrackerBenchmark:
    
    TEST_DATA_BASE_DIR = "video"
    
    def __init__(self, tracker_classes, video_name, database_name, num_particles=100):
        video_path = make_video_path(video_name + ".pngvin")
        
        self.video_name = video_name
        self.database_name = database_name
        
        self.correct_states = numpy.load(os.path.join(video_path, "state_sequence.npy"))
        self.video = wvideo(video_path)
        self.db = StateTransitionDatabase(database_name)
        self.num_particles = num_particles

        self.trackers = map(lambda tracker_class:tracker_class(self.db, self.video), tracker_classes)

    def _run_test(self, tracker):
        print "Tracking with tracker class %s"%(tracker.__class__.__name__)
        return tracker.run(self.correct_states[0], self.num_particles)
    
    def run(self):
        print "Running tracking test"
        self.tracks = map(self._run_test, self.trackers)
        
        differences_from_correct = map(lambda track:numpy.abs(self.correct_states - track), self.tracks)
        sum_diffs = map(lambda diff:diff.sum(axis=0), differences_from_correct)
        
        print sum_diffs
        print "Finished tracking test"
        print

        self.evaluate_results(sum_diffs)

    def evaluate_results(self, sum_diffs):
        print "##################################################"
        print "#                  TEST RESULTS                  #"
        print "##################################################"
        print
        
        diff_matrix = numpy.array(sum_diffs)
        winner_indices = numpy.array(zip(*numpy.where((diff_matrix-diff_matrix.max(axis=0)) == 0)))[:,0]
        print "Winners by parameter index:"
        print
        for i, winner in enumerate(winner_indices):
            print "Parameter %i: %s with cumulative difference %f"%(i, self.trackers[winner].__class__.__name__, sum_diffs[winner][i])
        print
        
        print "##################################################"
        print "#               END OF TEST RESULTS              #"
        print "##################################################"
        print
    
    def animate(self, tracker_i):
        print "Animating test results"
        layer_manager = wlayermanager()
        layer_manager.add_layer(self.video)
        layer_manager.add_layer(self.trackers[tracker_i].get_animator())
        
        win = wwindow(layer_manager)
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
        print "Done animating test results"
        print
    
    def export_results(self):
        for tracker in self.trackers:
            pngvin_dir = make_run_path(self.video_name + "_" + tracker.__class__.__name__ + ".pngvin")
            print "Saving results of tracker %s to %s"%(tracker.__class__.__name__, pngvin_dir)
            tracker.export_results(pngvin_dir)
        print

def run_cli():
    """Usage: python benchmark.py VIDEO_NAME DB_NAME [-n NUM_PARTICLES] classes...
    
    Runs the benchmark for each of the named classes. All named classes must be
    present in the wtracker module. The benchmark is carried out with the
    specified video and database as arguments.
    """

    import sys

    if len(sys.argv) <= 1:
        print run_cli.__doc__
        sys.exit()

    video_name = None
    database_name = None
    num_particles = 100

    tracker_classes = []

    it = iter(sys.argv)
    it.next()

    video_name = it.next()
    database_name = it.next()

    for arg in it:
        if arg == "-n":
            num_particles = int(it.next())

        elif arg in dir(wtracker):
            tracker_classes.append(getattr(wtracker, arg))
        else:
            print "WARNING: Class not found in module tracker:", arg

    print "Using video: %s"%(video_name)
    print "Using database: %s"%(database_name)
    print "Using %i particles"%(num_particles)
    
    print
    print "Benchmarking tracker classes:"
    for c in tracker_classes:
        print "\t%s"%(c.__name__)
    print
            
    benchmark = TrackerBenchmark(tracker_classes, video_name, database_name, num_particles)
    benchmark.run()
    benchmark.export_results()
    benchmark.animate(0)

if __name__ == "__main__":
    import cProfile
    cProfile.run("run_cli()")
