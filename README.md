# Lauseluokitteludatasetti: Ministerien vastaukset kirjallisiin kysymyksiin

English summary: This package prepares a Finnish NLP sentence
classification dataset based on cabinet ministers' answers to written
questions by members of parliament.

Tämä paketti sisältää suomenkielisen lauseaineiston esimerkiksi
luonnollisen kielen käsittelymenetelmien opettamiseen.

Ainesto perustuu eduskunnan avoimena datana julkaisemaan ministerien
vastauksiin kansanedustajien kirjallisiin kysymyksiin. Vastaukset on
jaettu lauseiksi ja ennustettavana kohdemuuttujana on se ministeriö,
jonka vastauksesta lause on poimittu.

## Lausetiedostot

Aineisto on tallennettu CSV-muodossa:

* [vkk/train.csv](vkk/train.csv): Opetusjoukko
* [vkk/dev.csv](vkk/dev.csv): Kehitysjoukko
* [vkk/test.csv](vkk/test.csv): Testijoukko

Jokainen tiedosto on CSV-muotoinen (sarake-erottimena pilkku) ja sisältää kaksi saraketta: sentence ja ministry. Jokainen sentence-sarakeen rivi on yksi lause satunnaisesta vastauksesta ja vastaava ministry-sarakeeen rivi kertoo minkä ministeriön vastauksesta lause on poimittu. Välimerkit on eroteltu niitä edeltävistä ja seuraavista sanoista lisäämällä tarvittaessa välilyöntejä.

Jako opetus-, kehitys- ja testijoukkoihin on tehty jakamalla lauseet satunnaisesti kolmeen osaan.

## Aineiston muodostaminen

Lauseainesto on esikäsitellyssä muodossa [vkk-alihakemistossa](vkk), eikä sen käyttämiseksi tarvitse tehdä mitään.

Jos kuitenkin haluat ladata tuoreen aineiston ja toistaa esikäsittelyn, suorita seuraava komento:
```
pipenv run scripts/prepare_dataset.sh
```

## Käyttöehdot

Dokumentit on alunperin julkaistu [eduskunnan avoimen datan
arkistossa](http://avoindata.eduskunta.fi/). Alkuperäiset dokumentit
ja tässä julkaistu edelleenkäsitelty aineisto on julkaistu CC Nimeä
4.0 –lisenssillä.

Datan esikäsittelyskriptit on julkaistu MIT-lisenssillä.

Tarkemmat tiedot [LICENSE-tiedostossa](LICENSE).
