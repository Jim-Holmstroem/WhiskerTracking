class wlayermanager(gtk.DrawingArea):
    """
    Contains all the layers and controlls the rendering
    """

    layers=[]
    current_frame=0

    def __init__(self,layers=None):
        """

        Arguments: layers either one layer or multiple
        """
        super(wlayermanager,self).__init__()
        self.connect("expose-event",self.expose)
        self.connect("motion-notify-event",self.motion)
    
    def set_current_frame(self,i):
        self.current_frame=i
    def next_frame(self):
        self.current_frame+=1
    def prev_frame(self):
        self.current_frame-=1

    def render_layer(self,context,layer,i):
        """
        Used by render to render each layer
        """
        layer.render(context,i)
        context.paint_with_alpha(layer.alpha)
        return layer

        def render(self,context,i):
            """
            
            """
            map(lambda layer:self.render_layer(context,layer,i),self.layers))

    def add_layer(self,layer,i=None):
        if i is None:
            self.layers.append(layer)
        else:
            self.layers.insert(i,layer)


    def expose(self,widget,event):
        context=widget.window.cairo_create()
        self.render(context,self.current_frame)

    def motion(self,widget,event):
        """
        Gets the mousemovement inside the drawingarea
        """
        pass


    def exportPNGVIN(self,filename=None):
        """
        """
        pass
