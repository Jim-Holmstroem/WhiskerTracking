
class wanimation(wlayer):
    """
    Acts as a base for moving layers, has some helping hands; one can either inherit from it and override the __init__ or just send in data and data_renderer
    """
    def __init__(self,data,data_renderer,alpha=1.0):
        """
        
        Argument data needs to have __getitem__ defined
        Argument data_renderer(context,data_point) and renderers it
        """
        assert(isinstance(data,collections.Sqeuence))
        self.data=data
        self.data_renderer=data_renderer

    def set_alpha(self,alpha=1.0):
        self.alpha=alpha

    def render(context,i):
        self.data_renderer(context,data[i])
  

