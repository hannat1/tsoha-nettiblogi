# Nettiblogi

## Esittely
Sovellus on nettiblogi. Nettiblogissa voi pitää yhteyttä muihin käyttäjiin tekemällä julkaisuja omasta elämästä ja arjesta sekä keskustella muiden käyttäjien kanssa julkaisuista kommenteissa. 
Sovelluksessa voi siis 
- luoda ja poistaa käyttäjän
- kirjautua sisään ja ulos
- tehdä ja poistaa julkaisuja
- seurata muita käyttäjiä ja lopettaa seuraamisen
- selata tehtyjä julkaisuja
- tykätä julkaisuista ja poistaa tykkäyksen
- kommentoida julkaisuja ja poistaa omia kommentteja
- hakea käyttäjiä ja postauksia hakusanalla


## Käynnistysohjeet
Kloonaa tämä repositorio ja siirry repositorion juurihakemistoon omalla koneellasi. Luo kansioon .env tiedosto ja lisää tiedostoon seuraavat tiedot:

DATABASE_URL=<tietokannan-paikallinen-osoite>

SECRET_KEY=<salainen-avain>

Salaisen avaimen voit luoda terminaalissa esimerkiksi näin:

$ python3

>>> import secrets

>>> secrets.token_hex(16)

>>> 'b83e4fc8226809f52eaf6a95dbafe061'


Sitten aktivoidaan virtuaaliympäristö seuraavasti:
$ python3 -m venv venv
$ source venv/bin/activate

Ja asennetaan riippuvuudet komennolla:
$ pip install -r ./requirements.txt

Sitten määritetään tietokannan skeema:
$ psql < schema.sql

Voit käynnistää sitten ohjelman komennolla:
flask run
