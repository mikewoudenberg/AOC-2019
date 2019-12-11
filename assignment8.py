import numpy as np
from functools import reduce
filepath = 'data8.txt'


def readlines(filename):
    lineList = [line.rstrip('\n') for line in open(filename)]
    return lineList


input = [int(x) for x in readlines(filepath)[0]]
imgDim = [25, 6]


def getLayers():
    layers = []
    layerLength = imgDim[0] * imgDim[1]
    for i in range(int(len(input) / layerLength)):
        layers.append(input[i * layerLength:(i+1)*layerLength])
    return layers


layers = getLayers()
checksumLayer = sorted(layers, key=lambda x: x.count(0))[0]
print('Assignment 1:', checksumLayer.count(1) * checksumLayer.count(2))

image = np.array(layers[0])
for layer in layers[1:]:
    for i, pixel in enumerate(image):
        if pixel == 2:
            image[i] = layer[i]
image.shape = (imgDim[1], imgDim[0])
for y in image:
    print("".join(['.' if x == 0 else '█' for x in y]))
