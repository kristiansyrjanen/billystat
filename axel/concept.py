#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2

#TODO opencv:stä jotenkin keskipiste objekteille -> lista objektien koordinaateista
# Objekti on siis kokoelma pikseleitä 
#http://answers.opencv.org/question/80081/not-rect-roi-defined-by-4-points/
#https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
#https://stackoverflow.com/questions/12931621/opencv-sub-image-from-a-mat-image

def filter_image(image, corner_points):

    #opencv:stä pitäisi löytyä funktiot, pisteet joutuu määrittelemään käsin joka kuvakulmalle

    #Muodosta convexHull(points)

    #Tee alkuperäisen kokoinen musta kuva (roi)

    #Maalaa convexhull valkoiseksi mustassa kuvassa fillConvexPoly(roi, points)

    #Filtteröi kuva bitwise_and(image, roi, filtered_image)

    return filtered_image

def listaa_pallot(contours):
    
    coordinates = []

    for cnt in contours:
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        coordinates.append((cx,cy))

    return coordinates

def vertaa(entiset, nykyiset):
    if len(entiset) == len(nykyiset):
        #Ei tarvitse tehdä mitään kaikki tallella
        return

    puuttuvat = []

    for koordinaatit in entiset:
        any_close = False #TODO: Löydä onko mikään nykyisisitä tarpeeksi lähellä

        if not any_close:
            puuttuvat.append(koordinaatit)

    return puuttuvat