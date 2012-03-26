from .. import wanimation

class skeleton(wanimation):
    def render_function(context,data_point):
        """
        Must be defined
        """
        pass

    def __init__(self,data,alpha=1.0):
        """
        You should call parent-contstructtor
        """
        super(skeleton,self).__init__(data,self.render_function,alpha)

    def __len__(self):
        """
        Must be defined
        Used to check how much should be rendered, if undefined one can return 1
        """
        pass
