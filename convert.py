import re
g0pattern = r"^G0.*"
g1pattern = r"^G1.*"
g0re = re.compile(g0pattern)
g1re = re.compile(g1pattern)

Xpattern = r".*X[-\.\d]+"
Ypattern = r".*Y[-\.\d]+"
Zpattern = r".*Z[-\.\d]+"
Spattern = r".*S\d+"
Xre = re.compile(Xpattern)
Yre = re.compile(Ypattern)
Zre = re.compile(Zpattern)
Sre = re.compile(Spattern)

currentX = 0
currentY = 0
currentZ = 0
currentS = 0
fout = open('out.csv','w')
should_update = False
with open('telescope.gcode') as f:
    lines = f.readlines()
    for line in lines:
        if g0re.match(line):
            if Zre.match(line):
                should_update = True
                nextZ = re.findall(Zpattern,line)[0].split('Z')[1]
                if currentZ != nextZ:
                    currentZ = nextZ
        elif g1re.match(line):
            print(line)
            if Xre.match(line): 
                should_update = True
                nextX = re.findall(Xpattern,line)[0].split('X')[1]
                if currentX != nextX:
                    currentX = nextX
            if Yre.match(line): 
                should_update = True
                nextY = re.findall(Ypattern,line)[0].split('Y')[1]
                if currentY != nextY:
                    currentY = nextY
            if Zre.match(line):
                should_update = True
                nextZ = re.findall(Zpattern,line)[0].split('Z')[1]
                if currentZ != nextZ:
                    currentZ = nextZ
            # if Sre.match(line):
            #     nextS = re.findall(Spattern,line)[0].split('S')[1]
            #     if currentS != nextS:
            #         currentS = nextS
            # should_update = should_update and (float(currentS) > 0)
            if should_update:
                # fout.write("{0},{1},{2},{3}\n".format(currentX,currentY,currentZ,currentS))
                fout.write("{0},{1},{2}\n".format(currentX,currentY,currentZ))
                should_update = False
fout.close() 
