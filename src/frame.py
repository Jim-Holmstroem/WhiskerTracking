class frame:
    """
    Dual for image as numpy.array and PIL.Image with lazy loading / constructing

    @Note the dual could be generalized and perhaps used elsewhere
    """

    img=None
    img_hash=hash(img) #last hash in which we updated the image with
    arr=None
    arr_hash=hash(arr) #last hash in which we updated the array with

    def __init__(self,image):
        raise Exception("Not tested yet")
        self.img=image

    def update_image(self):
        self.img=Image.fromarray(numpy.uint(self.arr))
        self.arr_hash=hash(self.arr)

    def update_array(self):
        self.arr=numpy.asarray(self.img)
        self.img_hash=hash(self.img)

    def get_image(self):
        """

        """
        if(self.arr_hash!=hash(self.arr)):
            self.update_image()
        return self.img

    def get_array(self):
        """

        """
        if(self.img_hash!=hash(self.img)):
            self.update_array()
        return self.arr

