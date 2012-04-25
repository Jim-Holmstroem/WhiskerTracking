
__all__=['testscreen']

from wmedia.wanimation import wanimation

class testscreen(wanimation):
    def render_function(self,context,data_point):

        context.scale(512,512)

        context.set_line_width(0.01)
        context.rectangle(0.01,0.01,0.98,0.45-data_point/300)
        context.set_source_rgba(1.0,1.0,1.0,self.alpha)
        
        
        context.stroke()


    def __init__(self,b=5,alpha=1.0):
        """
        You should call parent-constructor
        """
        wanimation.__init__(self,lambda x:float(b*x),self.render_function,alpha)

    def __len__(self):
        """
        Must be defined
        Used to check how much should be rendered, if undefined one can return 1
        """
        return 30
