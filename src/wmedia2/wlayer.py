
class wlayer:
    """
    Acts as base for all the different types of layers
    """
    alpha=1.0
    
    def render(self,context,i=None):
        pass

    def set_alpha(self,alpha=1.0):
        self.alpha=alpha

    def __len__(self):
        return 1
