class frame:
    """
    Dual for image as numpy.array and PIL.Image with lazy loading/constructing

    @Example
        f=frame(Image.load('test.png'))
        frame.get_image().show() #no converting
        read_array(frame.get_array()) #convert img->arr internally since img updated (from None)
        frame.get_image().show() #no converting since arr hash haven't changed
        write_array(frame.get_array()) #no conversion
        frame.get_image().show() #convert arr->img since arr has updated

    @NOTE AVOID (Example)
        arr=f.get_arr()
        img=f.get_image()
        write2(arr)
        img.show() #will show the old image

    @Note the dual could be generalized and perhaps used elsewhere
    """

    __img=None
    __img_hash=hash(__img) #last hash in which we updated the image with
    __arr=None
    __arr_hash=hash(__arr) #last hash in which we updated the array with

    def __init__(self,image):
        raise Exception("Not tested yet")
        self.__img=image

    def __update_hash(self):
        """
        Called when __img and __arr is synced
        """
        self.__img_hash=hash(self.__img)
        self.__arr_hash=hash(self.__arr)

    def __update_image(self):
        self.__img=Image.fromarray(numpy.uint(self.__arr))
        self.__update_hash()

    def __update_array(self):
        self.__arr=numpy.asarray(self.__img)
        self.__update_hash()

    def get_image(self):
        """

        """
        if(self.__arr_hash!=hash(self.__arr)): #if __arr has changed
            self.__update_image()
        return self.__img

    def get_array(self):
        """

        """
        if(self.__img_hash!=hash(self.__img)): #if __img has changed
            self.__update_array()
        return self.__arr

