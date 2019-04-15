#Tällä hetkellä saa kaikkien ympyröiden keskipisteet
#Kehän printattua listaan
#Mitä tehdä kun tulee päällekkäisyyksiä, miten kannattaisi vertailla palloja esim ympyröiden kehiä
#Jos päällekäisyyksiä, ehkä dilate ratkaisee asian

import numpy as np
from scipy.spatial.distance import euclidean

#Valittu hiirellä kuvasta, smanlainen koodi kuin maskin luonnissa.
hole_locations = [(0,1), (1,1), (1,2)]

def calculate_average_color(contour, image):
    """Halutaan keskimääräinen väri,
    että sitä voidaan verrata värimääritelmiin ja päätellä mikä palloista on kyseessä
    https://stackoverflow.com/a/54317652
    """
    pass

#Olettaen kattoperspektiivi, ei tarvita erotusta rykelmästä.
#+ että saadaan oikeasti vain ympyröitä 
# jos tarpeellista:
# filtteröinti mahdollista kehän avulla, cv2.minEnclosingCircle(contour)
# Jos mineclosingcirlen kehä/ala poikkeaa huomattavasti, contourin kehästä/alasta => ei pallo
#Tässä countour = cv2.findContours(?, ?, ?) tulos, sen jälkeen kun on tehty taustanpoisto kuvasta.

def liike(past_locations, current_locations):
    #Olettaen että locations = [(keskimäärinen_väri, koordinaatit), ...]
    # [('punainen', (0,1)), ('sininen', (1,1))]
    #Ja keskimääräinen_väri = kategoria (esim punainen)
    #Eli on jo katsottu alueelle calculate_average_color ja käyty läpi määritellyt värialueet
    # olettaen aina että len(past_locations) > len(current_locations)
    #Harkitaan etäisyyksien laskentaa etukäteen.

    #tiloja

    moving = np.logical(len(current_locations))
    vanished_near_hole = np.logical(len(current_locations))

    moving[:] = False
    vanished_near_hole[:] = False

    #Määrittele
    threshold = 5

    for index, color, coordinates in enumerate(current_locations):
        min_distance = np.inf
        any_balls = False
        for past_color, past_coordinates in past_locations:
            if color != past_color:
                continue
            distance = euclidean(coordinates, past_coordinates)
            any_matching_balls = True
            if distance < min_distance:
                distance = min_distance
        if (min_distance > threshold) & any_matching_balls:
            moving[index] = True

    for index, past_color, past_coordinates in enumerate(past_locations):
        for hole in hole_locations:
            #voi olla että pitää olla eri threshold
            distance = euclidean(hole, past_coordinates)
            if distance < threshold:
                same_colored_present = [item for item in current_locations if item[0] == past_color]
                same_colored_past = [item for item in past_coordinates if item[0] == past_color]
                #Jos monta palloa menee reikään samaan aikaan ei toimi, silloin pitää laskea etäisyydet ja katsoa mmikä hävisi.
                if len(same_colored_past) != len(same_colored_present):
                    vanished_near_hole[index] = True 
                    break

            
        
