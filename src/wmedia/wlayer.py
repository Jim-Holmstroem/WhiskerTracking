import cairo
from common import settings

class wlayer:
    """
    Acts as base for all the different types of layers
    """
    def __init__(self,alpha=1.0):
        self.alpha = alpha

    def render(self,context,i=None):
        raise NotImplementedError("Attempt to render raw wlayer (abstract class!)")

    def set_alpha(self,alpha=1.0):
        self.alpha=alpha

    def __len__(self):
        return 1

    def get_imagesurface(self, width=settings.IMAGE_WIDTH, height=settings.IMAGE_HEIGHT):
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(img)
        self.render(context)
        return img
