import gtk
import pygtk



class wwindow(gtk.Window):

    __version__="0.1"
    __program_name="WhiskerTracking"
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title(self.__program_name+" - v"+self.__version__)
        self.set_default_size(1024,768)
        self.connect("destroy",gtk.main_quit)
        
        

        
        
        self.show_all()



if __name__=="__main__":
    win=wwindow()
    
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
