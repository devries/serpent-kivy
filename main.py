from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import comcycle

class FingerTouch(Widget):
    def fade(self):
        self.opacity = self.opacity*0.8

class SerpentUI(FloatLayout):
    finger = ObjectProperty(None)

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
            self.finger.center = touch.pos
            self.finger.opacity=1.0

    def do_press(self):
        ipaddr = '192.168.10.88'
        port = 60666
        self.pattern.connect(ipaddr,port)

    def do_stop(self):
        self.pattern.stop()
        exit(0)

    def set_red(self,red):
        self.pattern.red=red

    def set_green(self,green):
        self.pattern.green=green

    def set_blue(self,blue):
        self.pattern.blue=blue

    def periodic(self,dt):
        self.finger.fade()


class SerpentApp(App):
    def build(self):
        s = SerpentUI()
        s.pattern = comcycle.BillowPattern()
        Clock.schedule_interval(s.periodic,0.1)
        return s

if __name__=='__main__':
    SerpentApp().run()
