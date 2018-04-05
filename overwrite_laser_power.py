import re
import sys
import pdb

if len(sys.argv)<2:
    print("Convert error: specify file")
    exit()
filename = sys.argv[1]

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
fout = open(filename + '_converted.gcode','w')

LASER_REDUCTION_RATE = 0.8

z_filter_list = [17. , 17.6, 17.9, 18. , 18.1, 18.3, 18.4, 18.6, 18.7, 18.8, 18.9,
       19. , 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, 19.9, 20. , 20.1,
       20.2, 20.3, 20.4, 20.5, 20.6, 20.7, 20.8, 20.9, 21. , 21.1, 21.2,
       21.3, 21.4, 21.5, 21.6, 21.7, 21.8, 21.9, 22. , 22.1, 22.2, 22.3,
       22.4, 22.5, 22.6, 22.7, 22.8, 22.9, 23. , 23.1, 23.2, 23.3, 23.4,
       23.5, 23.6, 23.7, 23.8, 23.9, 24. , 24.1, 24.2, 24.3, 24.4, 24.5,
       24.6, 24.7, 24.8, 24.9, 25. , 25.1, 25.2, 25.3, 25.4, 25.5, 25.6,
       25.7, 25.8, 25.9, 26. , 26.1, 26.2, 26.3, 26.4, 26.5, 26.6, 26.7,
       26.8, 26.9, 27. , 27.1, 27.2, 27.3, 27.4, 27.5, 27.6, 27.7, 27.8,
       27.9, 28. , 28.1, 28.2, 28.3, 28.4, 28.5, 28.6, 28.7, 28.8, 28.9,
       29. , 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 30. ,
       30.1, 30.2, 30.3, 30.4, 30.5, 30.6, 30.7, 30.8, 30.9, 31. , 31.1,
       31.2, 31.3, 31.4, 31.5, 31.6, 31.7, 31.8, 31.9, 32. , 32.1, 32.2,
       32.3, 32.4, 32.5, 32.6, 32.7, 32.8, 32.9, 33. , 33.1, 33.2, 33.3,
       33.4, 33.5, 33.6, 33.7, 33.8, 33.9, 34. , 34.1, 34.2, 34.3, 34.4,
       34.5, 34.6, 34.7, 34.8, 34.9, 35. , 35.1, 35.2, 35.3, 35.4, 35.5,
       35.6, 35.7, 35.8, 35.9, 36. , 36.1, 36.2, 36.3, 36.4, 36.5, 36.6,
       36.7, 36.8, 36.9, 37. , 37.1, 37.2, 37.3, 37.4, 37.5, 37.6, 37.7,
       37.8, 37.9, 38. , 38.1, 38.2, 38.3, 38.4, 38.5, 38.6, 38.7, 38.8,
       38.9, 39. , 39.1, 39.2, 39.3, 39.4, 39.5, 39.6, 39.7, 39.8, 39.9,
       40. , 40.1, 40.2, 40.3, 40.4, 40.5, 40.6, 40.7, 40.8, 40.9, 41. ,
       41.2, 41.4, 41.6, 41.8, 41.9, 42.4, 42.8]

with open(filename) as f:
    lines = f.readlines()
    for line in lines:
        if g0re.match(line):
            if Zre.match(line):
                should_update = True
                nextZ = re.findall(Zpattern,line)[0].split('Z')[1]
                if currentZ != nextZ:
                    currentZ = nextZ
        elif g1re.match(line):
            if Xre.match(line): 
                should_update = True
                nextX = float(re.findall(Xpattern,line)[0].split('X')[1])
                if currentX != nextX:
                    currentX = nextX
            if Yre.match(line): 
                should_update = True
                nextY = float(re.findall(Ypattern,line)[0].split('Y')[1])
                if currentY != nextY:
                    currentY = nextY
            if Zre.match(line):
                should_update = True
                nextZ = float(re.findall(Zpattern,line)[0].split('Z')[1])
                if currentZ != nextZ:
                    currentZ = nextZ
            if Sre.match(line):
                nextS = int(re.findall(Spattern,line)[0].split('S')[1])
                if currentS != nextS:
                    currentS = nextS
            if float(currentZ) in z_filter_list:
                if Sre.match(line):
                    updateS = int(currentS * LASER_REDUCTION_RATE)
                    if updateS < 1:
                        updateS = 1
                    line = re.sub(r"S\d+","S"+str(updateS),line)    
        fout.write(line)            
fout.close() 
