
__all__=['testscreen']

from wmedia2.wanimation import wanimation

class testscreen(wanimation):
    def render_function(context,data_point):
        """
        Must be defined
        """
        context.save() #TODO move these suckers outside so one can guarantee the same transformations and stuff
        context.move_to(0,0)
        context.line_to(data_point,data_point)

        context.restore()

    def __init__(self,b=5,alpha=1.0):
        """
        You should call parent-constructor
        """
        wanimation.__init__(self,lambda x:b*x,self.render_function,alpha)

    def __len__(self):
        """
        Must be defined
        Used to check how much should be rendered, if undefined one can return 1
        """
        return 14
