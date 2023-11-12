import sqlite3
from openai import OpenAI
client = OpenAI()
# Hae dataa tietokannasta

conn = sqlite3.connect('kurssit.db')
cursor = conn.cursor()
# Luo taulu
cursor.execute('''
    CREATE TABLE IF NOT EXISTS kurssit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kurssin nimi TEXT,
        tietoa kurssista TEXT,
        opintopiste määrä INTEGER
    )
''')

tietueet = [
    (1, "ICT-valmiudet", "Kun olet käynyt tämän opintojakson, osaat hyödyntää tieto- ja viestintätekniikkaa opiskelussasi. Sinulla on perustiedot tekijänoikeuksista, tietoturvasta, tietosuojasta sekä niiden vaikutuksesta opiskeluusi ja työelämään. Osaat käyttää monipuolisesti tekstinkäsittelyn, esitysgrafiikan ja taulukkolaskennan toimisto-ohjelmia. Osaat osallistua ja luoda verkkokokouksen sekä käyttää ryhmätyövälineitä.", 3),
    (2, "Kyberturvallisuus", "Sinä hallitset keskeisimmät kyberturvallisuuteen liittyvät osa-alueet: käsitteet (esim. luottamuksellisuus, eheys ja saatavuus), standardit ja lainsäädäntö (esim. tietosuoja, suojaustasot). Sinä käsität miten nämä soveltuvat henkilökohtaisessa, yhteiskunnallisessa ja organisaation kyberturvallisuudessa. Sinä tutustut teknisiin menetelmiin, joiden avulla voidaan esimerkiksi suojata järjestelmiä, havaita puutteita ja varmistaa tiedon eheys. Sinä tunnet tiedonsiirrossa käytetyt turvamekanismit luotettavuuteen ja saatavuuteen liittyen sekä haittaohjelmien ja haavoittuvuuksien toimintaperiaatteet ja vaikutukset.",4),
    (3, "Linuxin käyttö ja hallinta", "Suoritettuasi opintojakson ymmärrät Linux-käyttöjärjestelmän keskeisimmät käsitteet ja osaat työskennellä, sekä hallinnoida käyttöjärjestelmää tekstipohjaisen käyttöliittymän avulla.", 5)
]
#cursor.executemany("INSERT INTO kurssit VALUES(?,?,?,?)", tietueet)
#conn.commit()

tulokset = cursor.execute("SELECT * FROM kurssit")
tulos = str(tulokset.fetchall())
#print(tulos)

while True:
    syote = input("Sinä: ")

    vastaus = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are student advisor who helps students with their studies. you answer shortly and only the asked thing. ext information is database and you must use it: {}".format(tulos)},
            {"role": "user", "content": "{}".format(syote)}
        ],
        max_tokens=200
    )
    res = str(vastaus.choices[0].message)
    res2 = res.replace("ChatCompletionMessage(content=", "")
    res3 = res2.replace(", role='assistant', function_call=None, tool_calls=None)", "")
    print("Mauri:", res3)
    if syote.lower()=="exit":
        break
conn.close()
