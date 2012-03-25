
class squareanimation(wanimation):
    
    def render_square(context,data_point):
        context.rotate
        context.rectangle(data_point.x,data_point.y,...)

    def __init__(self,data,alpha=1.0)
        super(squareanimation,self).__init__(data,self.render_square,alpha)

    
