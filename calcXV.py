import re
import sys
import pdb
from math import sqrt
import time

g0pattern = r"^G0.*"
g1pattern = r"^G1.*"
g0re = re.compile(g0pattern)
g1re = re.compile(g1pattern)

Xpattern = r".*X[-\.\d]+"
Ypattern = r".*Y[-\.\d]+"
Zpattern = r".*Z[-\.\d]+"
Fpattern = r".*F\d+"
Xre = re.compile(Xpattern)
Yre = re.compile(Ypattern)
Zre = re.compile(Zpattern)
Fre = re.compile(Fpattern)

currentX = 0
currentY = 0
currentZ = 0
currentF = 3000
nextX = 0
nextY = 0
nextZ = 0
nextF = 3000 
BUFSIZE = 6

delay_array = []
MINIMUM_DELAY_TIME = 0.1

def parse(line):
    global BUFSIZE,cnt,currentX,currentY,currentZ,currentF,nextX,nextY,nextZ,nextF 

    if g0re.match(line) or g1re.match(line):
        if Xre.match(line): 
            nextX = float(re.findall(Xpattern,line)[0].split('X')[1])
            if currentX != nextX:
                currentX = nextX
        if Yre.match(line): 
            nextY = float(re.findall(Ypattern,line)[0].split('Y')[1])
            if currentY != nextY:
                currentY = nextY
        if Zre.match(line):
            nextZ = float(re.findall(Zpattern,line)[0].split('Z')[1])
            if currentZ != nextZ:
                currentZ = nextZ
        if Fre.match(line):
            nextF = float(re.findall(Fpattern,line)[0].split('F')[1])
            if currentF != nextF:
                currentF = nextF

        dr = sqrt((nextX-currentX)**2+(nextY-currentY)**2+(nextY-currentX)**2)
        v = currentF/60
        t = dr/v #[s]
        delay_array.append(max(t,MINIMUM_DELAY_TIME))

filepath = "/Users/shohei/Downloads/moge/20mm_cube.gcode"
with open(filepath) as f:
    lines = f.readlines()
    line_number = 0
    for idx,line in enumerate(lines):
        if(line[0]==';'):
            continue
        if(line_number<BUFSIZE):
            arduino.write(line)
            time.sleep(MINIMUM_DELAY_TIME)
        else:
            parse(line)
            arduino.write(line)
            time.sleep(delay_array[line_number-BUFSIZE])
        line_number += 1     

