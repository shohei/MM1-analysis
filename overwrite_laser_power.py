import re
import sys

if len(sys.argv)<2:
    print("Convert error: specify file")
    exit()
filename = sys.argv[1]

g0pattern = r"^G0.*"
g1pattern = r"^G1.*"
g0re = re.compile(g0pattern)
g1re = re.compile(g1pattern)

Spattern = r".*S\d+"
Sre = re.compile(Spattern)

currentS = 0
fout = open(filename.split('.')[0]+'_converted.gcode','w')

z_filter_list = [17.6, 17.9, 18. , 18.1]

REDUCTION_RATE = 0.8

with open(filename) as f:
    lines = f.readlines()
    for line in lines:
        Zpattern = r".*Z[-\.\d]+"
        Zre = re.compile(Zpattern)
        if g1re.match(line):
            if Sre.match(line):
                nextS = re.findall(Spattern,line)[0].split('S')[1]
                if currentS != nextS:
                    currentS = nextS
            if Zre.match(line):
                Z = re.findall(Zpattern,line)[0].split('Z')[1]
                if Z in z_filter_list:
                    updateS = int(currentS * REDUCTION_RATE)
                    if updateS < 1:
                        updateS = 1
                elif:
                    updateS = currentS
            line = re.sub(r"S\d",updateS,line)        
    fout.write(line)

fout.close() 
