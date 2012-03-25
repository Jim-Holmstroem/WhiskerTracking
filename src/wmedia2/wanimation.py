class wanimation(wlayer):
    """
    Acts as a base for moving layers, has some helping hands; one can either inherit from it and override the __init__ or just send in data and data_renderer
    """
    def __init__(self,data,data_renderer,alpha=1.0):
        """
        
        Argument data needs to have __getitem__ defined OR being callable (function)
        Argument data_renderer(context,data_point) and renderers it
        """
        self.data=data
        self.data_renderer=data_renderer

    def render(context,i):
        if isinstance(data,collections.Sequence):
            self.data_renderer(context,data[i])
        elif callable(data):
            self.data_renderer(context,data(i))
        else:
            raise Exception("Data is not sequence nor callable")


