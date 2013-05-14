from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty
import comcycle

ipaddr = '10.0.0.101'
port = 60666

class FingerTouch(Widget):
    color = ListProperty([0,0,1])
    def fade(self):
        self.opacity = self.opacity*0.8

class CLabel(Label):
    bgcolor = ListProperty([0,0,0])

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
        #ipaddr = '192.168.10.88'
        ipaddr = '10.0.0.101'
        port = 60666
        self.pattern.connect(ipaddr,port)

    def check_connection(self,dt):
        if self.pattern.connection is None:
            self.connection_status.text = 'Disconnected'
            self.connection_status.bgcolor = [1.0,0.0,0.0,1.0]
            self.pattern.connect(ipaddr,port)
        else:
            self.connection_status.text = 'Connected'
            self.connection_status.bgcolor = [0.0,0.8,0.0,1.0]

    def do_stop(self):
        self.pattern.stop()
        exit(0)

    def set_red(self,red):
        self.pattern.red=red
        self.finger.color=[self.pattern.red/255.0,self.pattern.green/255.0,self.pattern.blue/255.0]

    def set_green(self,green):
        self.pattern.green=green
        self.finger.color=[self.pattern.red/255.0,self.pattern.green/255.0,self.pattern.blue/255.0]

    def set_blue(self,blue):
        self.pattern.blue=blue
        self.finger.color=[self.pattern.red/255.0,self.pattern.green/255.0,self.pattern.blue/255.0]

    def set_speed(self,speed):
        print "Speed: %f"%speed

    def set_fade(self,fade):
        print "Fade: %f"%fade

    def periodic(self,dt):
        self.finger.fade()


class SerpentApp(App):
    def build(self):
        self.s = SerpentUI()
        self.s.pattern = comcycle.BillowPattern()
        Clock.schedule_interval(self.s.periodic,0.1)
        Clock.schedule_interval(self.s.check_connection,5.0)
        return self.s

    def on_stop(self):
        self.s.do_stop()

if __name__=='__main__':
    SerpentApp().run()
