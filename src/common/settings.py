"""Settings that do not change when moving the project"""

from settings_machine_specific import ROOT_DIRECTORY
from os.path import join

VIDEO_DIRECTORY = "video"
DATA_DIRECTORY = "data"

def make_path(*args):
    return join(ROOT_DIRECTORY, *args)

def make_video_path(*args):
    return make_path(VIDEO_DIRECTORY, *args)

def make_data_path(*args):
    return make_path(DATA_DIRECTORY, *args)
