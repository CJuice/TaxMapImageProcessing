import os, sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches

# path = raw_input("Path to files\n>")
path = r"E:\TaxMapsProject\Testing\TFWexplorations"
count = 0
lsXCoordinates = []
lsYCoordinates = []
dictStatsX = {}
dictStatsY = {}
def countUpOccurrences(dictA, value):
    if not dictA.get(value):
        dictA[value] = 1
    else:
        dictA[value] += 1

for(dirname, dirs, files) in os.walk(path):
    for file in files:
        strFileName = os.path.basename(file)
        lsfileparts = strFileName.lower().split(".")
        try:
            strextension = lsfileparts[1]
            if strextension == "tfw":
                strfilecontents = None
                with open(os.path.join(dirname,file)) as fopen:
                    lsLines = []
                    for line in fopen:
                        line = line.rstrip()
                        if len(line) != 0:
                            lsLines.append(line)
                    X = float(lsLines[4])
                    Y = float(lsLines[5])
                    # if X > 0:
                    lsXCoordinates.append(X)
                    lsYCoordinates.append(Y)
                    countUpOccurrences(dictStatsX, X)
                    countUpOccurrences(dictStatsY, Y)
                # Lines 5 and 6 of the tfw are x and y coords of the upper left pixel of the raster
                # Get the range of these values for the feet and meters versions
        except Exception as e:
            print e
print dictStatsX
print dictStatsY
print "max X: {}".format(max(lsXCoordinates))
print "min X: {}".format(min(lsXCoordinates))
print "max Y: {}".format(max(lsYCoordinates))
print "min Y: {}".format(min(lsYCoordinates))

# plotting occurrences of unique values
# xArray = np.array(dictStatsX.keys())
# yArray = np.array(dictStatsX.values())
# plt.scatter(xArray,yArray)
# plt.show()

# Extents
extentWKID26985_X = [185218.488100,185218.488100,570274.874800,570274.874800]
extentWKID26985_Y = [24686.339700,230946.080000,230946.080000,24686.339700]

extentWKID2248_X = [607670.989729,607670.989729,1870976.818427,1870976.818427]
extentWKID2248_Y = [80991.766092,757695.597392,757695.597392,80991.766092]

extentWKID3857_X = [-79.487303,-79.487303,-75.049201,-75.049201]
extentWKID3857_Y = [37.886530,39.722874,39.722874,37.886530]

# plotting x,y pairs
xArray = np.array(lsXCoordinates)
yArray = np.array(lsYCoordinates)
plt.scatter(xArray,yArray,s=12,c="purple",marker=".")

plt.scatter(x=extentWKID26985_X,y=extentWKID26985_Y,s=144,c="green",marker="*")
plt.scatter(x=extentWKID2248_X,y=extentWKID2248_Y,s=100,c="orange",marker="*")
# plt.scatter(x=extentWKID3857_X,y=extentWKID3857_Y,s=100,c="red",marker="*")
plt.show()

# plotting extents
# verts = [
#    (185218.488100, 24686.339700),  # left, bottom
#    (185218.488100, 230946.080000),  # left, top
#    (570274.874800, 230946.080000),  # right, top
#    (570274.874800, 24686.339700),  # right, bottom
#    (0., 0.),  # ignored
# ]
# codes = [
#     Path.MOVETO,
#     Path.LINETO,
#     Path.LINETO,
#     Path.LINETO,
#     Path.CLOSEPOLY,
# ]
#
# path = Path(verts, codes)
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# patch = patches.PathPatch(path, facecolor='orange', lw=2)
# ax.add_patch(patch)
# ax.set_xlim(185217, 1870977)
# ax.set_ylim(24686, 757695)
# plt.show()

