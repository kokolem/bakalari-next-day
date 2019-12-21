<h1 align="center">bakalari-next-day</h1>
  
<div align="center">
  
  Co si na zítra přidat a co z tašky vyndat podle Bakalářů
  
  ![GitHub](https://img.shields.io/github/license/kokolem/bakalari-next-day)
  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kokolem/bakalari-next-day)
  ![GitHub last commit](https://img.shields.io/github/last-commit/kokolem/bakalari-next-day)
  
</div>

## O programu
*Co si na zítra přidat a co z tašky vyndat podle Bakalářů* je Python program zobrazující co si vzít a co na příští den z tašky vyndat podle rozvrhu z Bakalářů.
Po spuštění se vás zeptá na tři údaje:
- Přihlašovací jméno
- Heslo
- URL adresa Bakalářů školy (například `https://skola.bakalari.cz/bakaweb/login.aspx`)

Potom vám ukáže požadované informace. Mohou vypadat třeba takto:

```
Do tasky si pridej:

Dějepis
Francouzský jazyk
Fyzika
Anglický jazyk
Pracovní činnosti

A vyndej: 

Zeměpis
Tělesná výchova
```

## Závislosti
- Python 3.x
- Knihovna [requests](http://docs.python-requests.org/en/master/)
