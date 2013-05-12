import comcycle
import time

pixel_map,strand_map = comcycle.create_julunggul_map()

comm = comcycle.CommunicationManager('192.168.10.88',60666)

for j in range(12*9):
    for i in range(25):
        comcycle.set_pixel(strand_map,pixel_map,i,j,0,0,255)
        if j>0:
            comcycle.set_pixel(strand_map,pixel_map,i,j-1,0,0,0)
        
    comcycle.send_strands(comm,strand_map)
    time.sleep(0.05)

comm.close()
