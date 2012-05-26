"""Settings that do not change when moving the project

This module depends on settings_machine_specific, which must define
ROOT_DIRECTORY.
"""

from settings_machine_specific import ROOT_DIRECTORY
from os.path import join

"""Directory for video files, relative to ROOT_DIRECTORY"""
VIDEO_DIRECTORY = "video"

"""Directory for data files, relative to ROOT_DIRECTORY"""
DATA_DIRECTORY = "data"

"""Directory for files generated when running the program, relative to ROOT_DIRECTORY"""
RUN_DIRECTORY = "run"

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 300

def make_path(*args):
    """Make the given path an absolute path by prepending ROOT_DIRECTORY
    @param args: A sequence of strings representing a hierarchy of directories.
                    These along with ROOT_DIRECTORY will be passed to
                    os.path.join.
    """
    return join(ROOT_DIRECTORY, *args)

def make_video_path(*args):
    """Make the given path an absolute path by prepending ROOT_DIRECTORY and
    VIDEO_PATH
    @see: make_path
    """
    return make_path(VIDEO_DIRECTORY, *args)

def make_data_path(*args):
    """Make the given path an absolute path by prepending ROOT_DIRECTORY and
    DATA_PATH
    @see: make_path
    """
    return make_path(DATA_DIRECTORY, *args)

def make_run_path(*args):
    """Make the given path an absolute path by prepending ROOT_DIRECTORY and
    RUN_PATH
    @see: make_path
    """
    return make_path(RUN_DIRECTORY, *args)
