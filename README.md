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

## Kuvia sovelluksesta 

Profiilinäkymä:

![Screenshot from 2024-09-11 16-33-46](https://github.com/user-attachments/assets/12cde710-46f7-4f8d-8d54-970122714fdb)

Bloginäkymä:

![Screenshot from 2024-09-11 16-36-48](https://github.com/user-attachments/assets/424cca6f-59b0-48a0-8fc8-329f376c82f9)

Uusi postaus:

![Screenshot from 2024-09-11 16-36-57](https://github.com/user-attachments/assets/efe82d17-a1a0-4bd1-aa37-0d0a1a47ea7f)

![Screenshot from 2024-09-11 16-37-05](https://github.com/user-attachments/assets/b17a1fb6-3b96-4037-aa60-37fed71f2688)

![Screenshot from 2024-09-11 16-37-37](https://github.com/user-attachments/assets/5677d946-d6c2-4b87-906b-3bd6e83fdb5e)

![Screenshot from 2024-09-11 16-44-10](https://github.com/user-attachments/assets/b0a3d6e7-44c3-4ca2-88dd-7adca8316327)
![Screenshot from 2024-09-11 16-47-04](https://github.com/user-attachments/assets/4a033ab2-50f2-4ffe-b979-ebc4a1224b4b)

![Screenshot from 2024-09-11 16-47-25](https://github.com/user-attachments/assets/0a4a0065-beb1-4325-a5df-137634c537ab)


## Käynnistysohjeet
Kloonaa tämä repositorio ja siirry repositorion juurihakemistoon omalla koneellasi. Luo kansioon .env tiedosto ja lisää tiedostoon seuraavat tiedot:
```
DATABASE_URL=<tietokannan-paikallinen-osoite>

SECRET_KEY=<salainen-avain>
```
Salaisen avaimen voit luoda terminaalissa esimerkiksi näin:
```
$ python3

>>> import secrets

>>> secrets.token_hex(16)

>>> 'b83e4fc8226809f52eaf6a95dbafe061'
```


Sitten aktivoidaan virtuaaliympäristö seuraavasti:
```
$ python3 -m venv venv

$ source venv/bin/activate
```

Ja asennetaan riippuvuudet komennolla:
```
$ pip install -r ./requirements.txt
```

Sitten määritetään tietokannan skeema:
```
$ psql < schema.sql
```

Voit käynnistää sitten ohjelman komennolla:
```
$ flask run
```

