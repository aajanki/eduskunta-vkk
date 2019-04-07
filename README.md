# Lauseluokitteludatasetti: Ministerien vastaukset kirjallisiin kysymyksiin

English summary: This package contains a Finnish NLP sentence
classification dataset based on cabinet ministers' answers to written
questions by members of parliament.

Tämä paketti sisältää suomenkielisen lauseaineiston esimerkiksi
luonnollisen kielen käsittelymenetelmien opettamiseen tai
testaamiseen.

Ainesto perustuu eduskunnan avoimena datana julkaisemiin ministerien
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

Jako opetus-, kehitys- ja testiaineistoihin on tehty jakamalla lauseet satunnaisesti kolmeen osaan.

## Aineistoa kuvailevia tilastoja

Lauseiden lukumäärät:

* Opetusaineisto: 49693
* Kehitysaineisto: 2000
* Testiaineisto: 2000

Lauseiden mediaanipituus on 16 tokenia ja maksimipituus 176 tokenia.

Luokat ja lauseiden lukumäärät luokittain opetusaineistossa:

| Luokka                                    | Lauseiden lukumäärä |
| ------                                    | ---- |
| perhe- ja peruspalveluministeri           | 8038 |
| maatalous- ja ympäristöministeri          | 7377 |
| oikeus- ja työministeri                   | 6222 |
| opetus- ja kulttuuriministeri             | 5652 |
| sisäministeri                             | 5646 |
| liikenne- ja viestintäministeri           | 3695 |
| sosiaali- ja terveysministeri             | 3646 |
| valtiovarainministeri                     | 2765 |
| elinkeinoministeri                        | 1940 |
| ulkoministeri                             |  977 |
| kunta- ja uudistusministeri               |  954 |
| eurooppa-, kulttuuri- ja urheiluministeri |  758 |
| pääministeri                              |  705 |
| puolustusministeri                        |  667 |
| ulkomaankauppa- ja kehitysministeri       |  651 |

Testi- ja kehitysaineistojen luokkajakaumat vastaavat opetusaineiston jakaumaa.

## Esimerkkilauseita

| Lause | Luokka |
| ----- | ------ |
| Lääkkeelliset kaasut kuten lääkehappi ovat lääkkeitä ( lääkelaki 395/1987 , 3 § ) . | sosiaali- ja terveysministeri |
| Kilpailutuskriteereissä noudatetaan lakia julkisista hankinnoista ja muita asiaan vaikuttavia säädöksiä . | sisäministeri |
| Poissaolot tulee selvittää ensisijaisesti opiston ja opiskelijan kesken . | sisäministeri |
| Tavoitteeksi asetettiin Porkkalan luonnonsuojelualueen perustaminen . | maatalous- ja ympäristöministeri |
| Vihapuhetyöryhmä antaa suosituksensa huhtikuun 2019 lopussa . | oikeus- ja työministeri |
| Toissijaisuuden arviointi jää viime kädessä tuomioistuinten ratkaistavaksi . | liikenne- ja viestintäministeri |

## Aineiston muodostaminen

Ainesto on valmiiksi käytettävässä muodossa [vkk-alihakemistossa](vkk).

Jos kuitenkin haluat ladata tuoreen aineiston eduskunnan palvelimelta ja toistaa esikäsittelyn, suorita seuraava komento:
```
pipenv run scripts/prepare_dataset.sh
```

## Käyttöehdot

Dokumentit on alunperin julkaistu [eduskunnan avoimen datan arkistossa](http://avoindata.eduskunta.fi/). Alkuperäiset dokumentit ja tässä julkaistu edelleenkäsitelty aineisto on julkaistu CC Nimeä 4.0 –lisenssillä. Katso [LICENSE.data-tiedosto](LICENSE.data).

Datan esikäsittelyskriptit on julkaistu MIT-lisenssillä. Katso [LICENSE-tiedosto](LICENSE).
