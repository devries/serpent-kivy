from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

class SerpentUI(FloatLayout):
    def do_touch(self,touch):
        touch.apply_transform_2d(self.to_local)
        xmin,ymin = self.serpent.pos
        width,height = self.serpent.size
        x,y = touch.pos

        xf = float(x-xmin)/width
        yf = float(y-ymin)/height
        print "Area touched: %f,%f"%(xf,yf)

    def do_press(self):
        print "Button Pressed"

class SerpentApp(App):
    def build(self):
        s = SerpentUI()
        print "Pos:"+repr(s.serpent.pos)
        print "Size:"+repr(s.serpent.size)
        return s

if __name__=='__main__':
    SerpentApp().run()
