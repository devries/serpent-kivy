from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import comcycle

class SerpentUI(FloatLayout):
    def do_touch(self,touch):
        touch.apply_transform_2d(self.to_local)
        xmin,ymin = self.serpent.pos
        width,height = self.serpent.size
        x,y = touch.pos

        xf = float(x-xmin)/width
        yf = float(y-ymin)/height
        if xf>=0.0 and yf>=0.0 and xf<1.0 and yf<1.0:
            self.pattern.touch_point(1.0-yf,xf)
            print "Area touched: %f,%f"%(xf,yf)

    def do_press(self):
        ipaddr = '192.168.10.88'
        port = 60666
        self.pattern.connect(ipaddr,port)

    def do_stop(self):
        self.pattern.stop()
        exit(0)

class SerpentApp(App):
    def build(self):
        s = SerpentUI()
        s.pattern = comcycle.BillowPattern()
        return s

if __name__=='__main__':
    SerpentApp().run()
