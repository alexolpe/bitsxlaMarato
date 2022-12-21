import cv2
import matplotlib.pyplot as plt
import numpy as np

from preprocessing import preprocessing
from MorphSnakes import example_nodule

from representation import representation
from shapely import geometry
import shapely



xStart = 0
yStart = 0
def click_event(event, x, y, flags, params):
     if event == cv2.EVENT_LBUTTONDOWN:
        global xStart, yStart
        print(x, ' ', y)
        xStart = x
        yStart = y
 
vidcap = cv2.VideoCapture('circDolent.avi')
success,image = vidcap.read()

cv2.imshow('starting image', image)
cv2.setMouseCallback('starting image', click_event)
cv2.waitKey(0)
f = open('distances.txt', 'w')

count = 0
while success:
    print("Frame: " , count)
    
    processed_image = preprocessing(image)

    result = example_nodule(processed_image, xStart, yStart)
    representation(image, result, count)
    coordinates=np.where(result == 1)
    listOfCoordinates= list(zip(coordinates[0], coordinates[1]))
    poly2 = geometry.Polygon([[p[1], p[0]] for p in listOfCoordinates])
    poly=poly2.convex_hull
    area=poly.area
    print("area: ",area)
    phi=0
    distances = []
    max=0
    min=0
    for i in range(36):
        try:
            pathX = 10000000*np.cos(phi)
            pathY = 10000000*np.sin(phi)
            path = geometry.LineString([(poly.centroid.x,poly.centroid.y), (poly.centroid.x + pathX, poly.centroid.y + pathY)])
            inter_result = shapely.intersection(path, poly)
            dist=np.linalg.norm(np.array([inter_result.coords[1:][0][0]-poly.centroid.x,inter_result.coords[1:][0][1]-poly.centroid.y]))
            if(dist>max or i==0):
                max=dist
            if(dist<min or i==0):
                min=dist
            distances.append(dist)
            print("max: ",max," min: ",min)
            phi = phi + 10*i
        except:
            phi = phi + 10*i
    
    
    if(max/min>=2 or max==0 or max>100):
        print("descarte")
        distances=aux_mem

    aux_area=area

    for n in range(36):
        f.write('_' + str(distances[n]))
    
    f.write('_' + str(area))
    aux_mem = distances
    f.write('\n')
    
    # Si la relacion de maximos diametros supera un lindar, descartamos y no actualizamos centroide
    if(max/min<2):
        xStart=poly.centroid.x
        yStart=poly.centroid.y

    print("Hola")
    success,image = vidcap.read()
    count += 1
f.close()

