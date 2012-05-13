#!/usr/bin/python

import cairo
import numpy
import os
import wdb
from common import make_run_path
from wview import GWhiskerRenderer

def run_cli():
    """Usage: python draw_database.py DATASET_NAME OUTPUT_name

    Draws the named database.
    """

    import sys

    if len(sys.argv) < 2:
        print run_cli.__doc__
        sys.exit()

    from common import cliutils
    import wgenerator

    args, kwargs = cliutils.extract_variables(sys.argv[1:], "DATASET_NAME OUTPUT_NAME")
    
    if len(args) < 1:
        print "ERROR: Dataset name was not specified."
        sys.exit(1)

    db_name = args[0]
    out_name = args[1]

    db = wdb.StateTransitionDatabase(db_name)
    from_states, to_states = numpy.split(db.get_all_transitions(0), 2)
    """
    from_states[:,0] = 0
    from_states[:,1] = 0
    to_states[:,0] = 0
    to_states[:,1] = 0
    """

    renderer = GWhiskerRenderer(5, 150, 5, translate=(256-75, 256), particle_alpha=0.0001)

    imsurf=cairo.ImageSurface(cairo.FORMAT_ARGB32, 512,512)
    ctx = cairo.Context(imsurf)
    #for btm, top in zip(numpy.linspace(0, 1-1.0/8, 8), numpy.linspace(1.0/8, 1, 8)):
    for states, name in ((from_states, "_from"), (to_states, "_to")):
        ctx.identity_matrix()
        ctx.rectangle(0, 0, 512, 512)
        ctx.set_source_rgb(0, 0, 0)
        ctx.fill()
        for s in states:
            #if 0.00002*btm < abs(s[0]) and abs(s[0]) < 0.00002*top:
            renderer.render(ctx, s, alpha=0.05)
	    imsurf.write_to_png(make_run_path(os.path.join("debug","db","%s.png"%(out_name + name))))

if __name__ == "__main__":
    run_cli()
