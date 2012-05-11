#!/usr/bin/python

def run_cli():
    """Usage: python generate.py GENERATOR_CLASS [generator options...]

    Generates a video and places it in VIDEO_DIRECTORY, as specified in
    common.settings. Also generates a training database and places it in
    DATA_DIRECTORY.
    """
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

    generator_class_name = sys.argv[1]
    helping = False

    if generator_class_name == "help":
        helping = True
        if len(sys.argv) < 3:
            print "What to you want help with?"
            sys.exit(1)
        generator_class_name = sys.argv[2]

    generator_class = None
    try:
        generator_class = getattr(wgenerator, generator_class_name)
    except AttributeError:
        print "Unknown tracker:", generator_class_name
        sys.exit(1)

    if helping:
        print generator_class.__doc__
        sys.exit(0)

    try:
        cli_def = "DATASET_NAME [-o number_of_objects] [-n number_of_transitions] [-f number_of_frames] [-m number_of_movies] [--dt dt] [--debug debug]"
        try:
            cli_def += " " + generator_class.CUSTOM_CLI_DEFINITION
        except AttributeError:
            pass

        args, kwargs = cliutils.extract_variables(sys.argv[2:], cli_def)
    
        generator = generator_class(*args, **kwargs)
        generator.generate()
        sys.exit(1)
    except TypeError:
        print "Syntax error, please consult the documentation for the tracker %s."%(generator_class_name)
        print
        print "Docstring for %s:"%(generator_class_name)
        print
        print generator_class.__doc__

if __name__ == "__main__":
    run_cli()
