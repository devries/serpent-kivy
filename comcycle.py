import Queue
import threading
import socket
import struct

fps = 24.0
spf = 1.0/fps

pixel_terminator = '\x00'*6

comm_channel = 0

class CommunicationManager(object):
    def __init__(self,ip_address,port):
        self.outputQ = Queue.Queue()
        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
    for address,pixel_array in enumerate(strand_arrays):
        npix = len(pixel_array)*3+len(pixel_terminator)
        header = struct.pack('!BBH',address,comm_channel,npix)
        comm_manager.send(header)
        comm_manager.send(''.join(pixel_array))
        comm_manager.send(pixel_terminator)

if __name__ == '__main__':
    l = CommunicationManager('localhost',60666)
    l.send('Hello Everyone')
    l.close()
