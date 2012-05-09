#!/usr/bin/python

def run_cli():
    """Usage: python generate.py GENERATOR_CLASS DATASET_NAME [-o NUM_OBJECTS]
    [-n NUM_TRANSITIONS] [-f NUM_FRAMES] [-m NUM_MOVIES] [--dt TIMESTEP_SIZE]
    [--debug (True|False)]")

    Generates a video and places it in VIDEO_DIRECTORY, as specified in
    common.settings. Also generates a training database and places it in
    DATA_DIRECTORY.
    """

    import sys

    if len(sys.argv) < 2:
        print run_cli.__doc__
        sys.exit()

    from common import cliutils
    import wgenerator

    args, kwargs = cliutils.extract_variables(sys.argv[1:], "GENERATOR_CLASS DATASET_NAME [-o number_of_objects] [-n number_of_transitions] [-f number_of_frames] [-m number_of_movies] [--dt dt] [--debug debug]")

    generator = getattr(wgenerator, args[0])(*args[1:], **kwargs)
    generator.generate()

if __name__ == "__main__":
    run_cli()
