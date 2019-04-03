# BillySTAT Info-sivu

### Tämän hetkinen tilanne:

*Tehtävää*:

*Värit kuntoon, niitten testaus, jos ei toimi niin toiset arvot mukaan.*

*Materiaalin trapetsointi (homographic perspective).*

*FOM (Fast-moving object) testiin.*


*Vähimmäismaali:*

*Osumatarkkuuden laskeminen. Kun joku muu kuin valkoinen pallo liikkuu = Osuma*

*Vain valkoinen pallo liikkuu = ohi kohde pallosta.*

## Haastikset

Haastattelimme muutamaa Snooker-harrastelijaa ja he antoivat muutaman hyvän idean.

* Virhelyöntien jälkeinen pallojen paikkojen merkkaus (Mahd. projektorilla pöydälle)
* Mahdollisesti pisteiden laskua kuvan tunnistuksella

## Ideat

* Digitaalinen pisteidenlaskutaulu, pisteet tallennetaan käyttäjälle palvelimelle tai lähetetään spostilla käyttäjälle
* Statistiikkaa 
* Mahdollisuus luoda lopputulos joko Yolo:lla tai pelkästään OpenCV:tä käyttäen




## Ongelmat

* Kannettavien näytönohjainten ajuriongelmat, ei suostu käyttämään sisäistä näytönohjainta kuvantunnistukseen
* Quadro K4000 hyyty kuvan tunnistuksessa (syy: 7 vuotta vanha)
* Videonlaatu liian hyvää, joutuu skaalaamaan alaspäin (1080p/4k-->360p)
* Kasassa olevat (punaiset) pallot näkyvät yhtenä isona alueena (OpenCV 25.02.19)
* 

## Miten tehdä?

* Viiden sekunnin välein diffi.
* Värilliset / Värin perusteella diffit



## Pohdiskelut

* Yolo vai OpenCV? (Alustavasti Miikka sekä Matias työskentelevät Yolo:lla, Kristian sekä Axel työskentelevät OpenCV:llä), kun on selkeästi todettavissa, että toinen menetelmä on parempi niin siirrymme siihen.
* Punaisten pallojen merkintä selkeästi pallojen ollessa lähellä toisiaan.


