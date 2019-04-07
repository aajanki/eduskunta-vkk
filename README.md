# Lauseluokitteludatasetti: Ministerien vastaukset kirjallisiin kysymyksiin

English summary: This package contains a Finnish NLP sentence
classification dataset based on cabinet ministers' answers to written
questions by members of parliament.

Tämä paketti sisältää suomenkielisen lauseaineiston esimerkiksi
luonnollisen kielen käsittelymenetelmien opettamiseen tai
testaamiseen.

Ainesto perustuu eduskunnan avoimena datana julkaisemaan ministerien
vastauksiin kansanedustajien kirjallisiin kysymyksiin vuosilta
2015-2019. Vastaukset on jaettu lauseiksi ja ennustettavana
kohdemuuttujana on se ministeriö, jonka vastauksesta lause on
poimittu.

## Lausetiedostot

Aineisto on saatavilla bzip2-pakattuina CSV-tiedostoina:

* [vkk/train.csv.bz2](vkk/train.csv.bz2): Opetusjoukko
* [vkk/dev.csv.bz2](vkk/dev.csv): Kehitysjoukko
* [vkk/test.csv.bz2](vkk/test.csv.bz2): Testijoukko

Jokainen tiedosto on CSV-muotoinen (sarake-erottimena pilkku) ja sisältää kaksi saraketta: sentence ja ministry. Tiedoston ensimmäisellä rivillä on sarakeotsikot. Jokainen sentence-sarakeen rivi on yksi lause satunnaisesta vastauksesta ja vastaava ministry-sarakeeen rivi kertoo minkä ministeriön vastauksesta lause on poimittu. Välimerkit on eroteltu niitä edeltävistä ja seuraavista sanoista lisäämällä tarvittaessa välilyöntejä.

Jako opetus-, kehitys- ja testijoukkoihin on tehty jakamalla lauseet satunnaisesti kolmeen osaan.

## Aineiston muodostaminen

Lauseainesto on valmiiksi käytettävässä muodossa [vkk-alihakemistossa](vkk).

Jos kuitenkin haluat ladata tuoreen aineiston eduskunnan palvelimelta ja toistaa esikäsittelyn, suorita seuraava komento:
```
pipenv run scripts/prepare_dataset.sh
```

## Käyttöehdot

Dokumentit on alunperin julkaistu [eduskunnan avoimen datan arkistossa](http://avoindata.eduskunta.fi/). Alkuperäiset dokumentit ja tässä julkaistu edelleenkäsitelty aineisto on julkaistu CC Nimeä 4.0 –lisenssillä. Katso [LICENSE.data-tiedosto](LICENSE.data).

Datan esikäsittelyskriptit on julkaistu MIT-lisenssillä. Katso [LICENSE-tiedosto](LICENSE).
