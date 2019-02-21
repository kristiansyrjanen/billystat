#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#TODO opencv:stä jotenkin keskipiste objekteille -> lista objektien koordinaateista
# Objekti on siis kokoelma pikseleitä 


def listaa_pallot():

    coordinates = None #TODO: tee opencv:llä

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