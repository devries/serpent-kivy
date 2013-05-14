import Queue
import threading
import socket
import struct
import collections
import math
import time
import sys

fps = 12.0
spf = 1.0/fps

pixel_terminator = '\x00'*6

comm_channel = 0

serpent_segments = 9
serpent_ring_length = 25 # This is also nx
serpent_rings_per_segment = 12 

image_nx = serpent_ring_length
image_ny = serpent_segments*serpent_rings_per_segment

class CommunicationManager(object):
    def __init__(self,ip_address,port):
        self.outputQ = Queue.Queue()
        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((ip_address,port))
        self.socket = s
        
        self.keepRunning = True
        self.outputThread = threading.Thread(target=self.runOutput)
        self.outputThread.start()

    def runOutput(self):
        while self.keepRunning:
            output_bytes = self.outputQ.get()
            totalsent = 0
            msglen = len(output_bytes)
            while totalsent<msglen:
                sent = self.socket.send(output_bytes[totalsent:])
                if sent == 0:
                    self.keepRunning=False # I should do something like shut off the queue queue
                totalsent = totalsent + sent

    def send(self,data):
        if self.keepRunning:
            self.outputQ.put(data)
        else:
            raise RuntimeError('The output thread is stopped')

    def hup(self):
        while not self.outputQ.empty():
            self.outputQ.get()

    def close(self):
        self.keepRunning = False
        self.outputQ.put('')
        self.outputThread.join()
        self.socket.close()

def setup_mapping(pixel_map,y_start,nx,ny,strand_address=0,pixel_start=0,start_descending=False):
    if start_descending:
        odd_even=1
    else:
        odd_even=0

    for j in range(ny):
        for i in range(nx):
            x = i
            y = j+y_start
            if j%2==odd_even:
                pixel = pixel_start + nx*j + i
            else:
                pixel = pixel_start + nx*j + nx-i-1

            pixel_map[(x,y)]=(strand_address,pixel)

def create_julunggul_map():
    pixel_map = {}
    for segment in range(serpent_segments):
        setup_mapping(pixel_map,segment*serpent_rings_per_segment,serpent_ring_length,serpent_rings_per_segment,segment+1)

    strand_arrays = setup_strands([300]+[serpent_ring_length*serpent_rings_per_segment+18]*(serpent_segments+1))

    return (pixel_map,strand_arrays)

def setup_strands(strand_lengths):
    strand_arrays = []
    for l in strand_lengths:
        subarray = ['\x00\x00\x00']*l
        strand_arrays.append(subarray)

    return strand_arrays

def set_pixel(strand_arrays,pixel_map,x,y,r,g,b):
    strand_tuple = pixel_map[(x,y)]
    strand_arrays[strand_tuple[0]][strand_tuple[1]] = struct.pack('!BBB',r,g,b)

def send_strands(comm_manager,strand_arrays):
    #comm_manager.hup()
    for address,pixel_array in enumerate(strand_arrays):
        npix = len(pixel_array)*3+len(pixel_terminator)
        header = struct.pack('!BBH',address+1,comm_channel,npix)
        comm_manager.send(header)
        comm_manager.send(''.join(pixel_array))
        comm_manager.send(pixel_terminator)

class BillowPattern(object):
    def __init__(self):
        self.pixel_map,self.strand_arrays = create_julunggul_map()
        self.points = collections.deque(maxlen=5)
        self.connection = None
        self.red = 108
        self.green = 80
        self.blue = 255
        self.speed = 1.0
        self.fade = 0.98

        self.keepRunning = True
        self.processThread = threading.Thread(target=self.go)
        self.processThread.start()

    def connect(self,ipaddress,port):
        try:
            self.connection = CommunicationManager(ipaddress,port)
        except:
            self.connection = None

    def stop(self):
        self.keepRunning = False
        self.processThread.join()
        if self.connection:
            self.connection.close()

    def step(self):
        current_rings = list(self.points)
        if len(current_rings)>5:
            print >>sys.stderr,"It's supposed to max at 5!"
        for j in range(image_ny):
            for i in range(image_nx):
                color = [0,0,0]
                for ring in current_rings:
                    if ring[2]<108.0:
                        d = math.sqrt((ring[0]-i)**2+(ring[1]-j)**2)
                        dev = math.fabs(d-ring[2])
                        if dev<ring[3]:
                            color = [(c+r)%255 for c,r in zip(color,ring[4])]

                set_pixel(self.strand_arrays,self.pixel_map,i,j,color[0],color[1],color[2])

        for ring in current_rings:
            ring[2]+=self.speed
            ring[4] = [c*self.fade for c in ring[4]]

    def go(self):
        while self.keepRunning:
            start = time.clock()
            self.step()
            if self.connection:
                send_strands(self.connection,self.strand_arrays)
            end = time.clock()
            delta = end-start

            if delta<spf:
                time.sleep(spf-delta)
            else:
                print "Behind"

    def touch_point(self,xf,yf):
        xp = int(math.floor(xf*image_nx))
        yp = int(math.floor(yf*image_ny))

        color = (self.red,self.green,self.blue)
        width = 4.0
        radius = 1.0

        self.points.appendleft([xp,yp,radius,width,color])

if __name__ == '__main__':
    l = CommunicationManager('localhost',60666)
    l.send('Hello Everyone')
    l.close()
