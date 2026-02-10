import arcade as a

class Welcome(a.Window):
    '''Main welcome window
    '''

    def __init__(self, width,height,title):
        super().__init__(width,height,title)

        a.set_background_color(a.color.ORANGE_PEEL)

    def on_draw(self): #overriding the parent on_draw method
        
        a.draw_text("Welcome",self.width/2,self.height/2,a.color.BLACK)