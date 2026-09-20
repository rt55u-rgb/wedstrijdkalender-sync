# Wedstrijdkalender Sync

Met dit programma kun je een wedstrijdkalender uit een Excel-bestand automatisch toevoegen aan een Google Agenda.

## Hoe werkt het?

Het programma doet eigenlijk maar drie dingen:

1. Je vult de wedstrijden in in `data/wedstrijdkalender.xlsx`.
2. Het programma leest de Excel-file uit.
3. De wedstrijden worden toegevoegd aan de ingestelde Google Agenda.

De standaardinstellingen staan in `config.py`. Daarin staat onder andere welke Google Agenda gebruikt wordt en dat de tijdzone `Europe/Amsterdam` is.

---

## 1. Benodigdheden

Je hebt nodig:

- Python
- De repository op je computer
- Een Google-account
- Toegang tot de Google Calendar API
- De benodigde Python-packages

De benodigde packages staan al in `requirements.txt`.


Maak daarna eventueel een Python virtual environment:

```bash
python -m venv .venv
```

Activeren:

### Windows

```bash
.venv\Scripts\activate
```


---

## 3. Excel-bestand aanpassen

De wedstrijden staan in:

```text
data/wedstrijdkalender.xlsx
```

Het programma verwacht daarin een werkblad met de naam:

```text
Blad1
```

De kolommen worden als volgt gelezen:

| Kolom | Betekenis |
|---|---|
| A | Dag |
| B | Datum |
| C | Categorie |
| D | Systeem |
| E | Informatie |
| F | Locatie |
| G | Starttijd |
| H | Leeftijd |
| I | Opmerkingen |

Het programma begint vanaf rij 2, dus rij 1 bevat de kolomnamen.

### Voorbeeld

Een wedstrijd kan bijvoorbeeld zo in Excel staan:

| Dag | Datum | Categorie | Systeem | Informatie | Locatie | Starttijd | Leeftijd | Opmerkingen |
|---|---|---|---|---|---|---|---|---|
| Zaterdag | 20-09-2026 | Wedstrijd | 1e klasse | Team A - Team B | Sporthal Vught | 14:00 | Senioren | Aanwezig 13:30 |

**Belangrijk:** gebruik echte Excel-datums en -tijden voor de kolommen Datum en Starttijd.

---

## 4. Google Calendar instellen

De eerste keer dat je het programma uitvoert, moet het programma toegang krijgen tot je Google Agenda.

Hiervoor moeten deze bestanden aanwezig zijn:

```text
credentials/
├── credentials.json
└── token.json
```

`credentials.json` komt uit de Google Cloud/API-configuratie.

`token.json` wordt daarna automatisch aangemaakt wanneer je voor de eerste keer inlogt. Het programma gebruikt dit token bij volgende uitvoeringen zodat je niet iedere keer opnieuw hoeft in te loggen.

**Deel `credentials.json` en `token.json` nooit publiekelijk.**

---

## 5. De kalender instellen

In `config.py` staan de belangrijkste instellingen:

```python
CALENDAR_ID = "..."
TIMEZONE = "Europe/Amsterdam"
DEFAULT_DURATION_HOURS = 3
EXCEL_FILE = "data/wedstrijdkalender.xlsx"
```

Meestal hoef je alleen de `CALENDAR_ID` aan te passen als je een andere Google Agenda wilt gebruiken.

De wedstrijden worden standaard drie uur lang gemaakt.

---

## 6. Synchroniseren

Als alles is ingesteld, ga je in de terminal naar de map van het project:

```bash
cd wedstrijdkalender-sync
```

Start daarna:

```bash
python sync.py
```

Het programma:

1. leest `data/wedstrijdkalender.xlsx`;
2. maakt van iedere wedstrijd een wedstrijd-object;
3. maakt verbinding met Google Calendar;
4. voegt iedere wedstrijd toe aan de agenda.

Aan het einde krijg je bijvoorbeeld:

```text
Toegevoegd: Wedstrijd - Team A - Team B
Toegevoegd: Wedstrijd - Team C - Team D

2 wedstrijden gesynchroniseerd.
```

Dit is precies wat `sync.py` doet: het laadt alle wedstrijden en voegt ze één voor één toe aan Google Calendar.

---

## 7. Wedstrijd toevoegen of wijzigen

### Nieuwe wedstrijd

Voeg de wedstrijd toe aan:

```text
data/wedstrijdkalender.xlsx
```

en voer daarna opnieuw uit:

```bash
python sync.py
```

### Wedstrijd wijzigen

Pas de wedstrijd aan in Excel en voer het script opnieuw uit.

**Let op:** het huidige script controleert niet of een wedstrijd al in de Google Agenda staat. Bij opnieuw uitvoeren kunnen wedstrijden dus opnieuw worden toegevoegd.

---

## 8. Wat staat er uiteindelijk in Google Calendar?

De titel van een wedstrijd wordt opgebouwd uit:

```text
Categorie - Informatie
```

Bijvoorbeeld:

```text
Wedstrijd - Team A - Team B
```

De locatie uit Excel wordt de locatie van de agenda-afspraak.

De wedstrijd begint op de opgegeven datum en starttijd en duurt standaard 3 uur. De tijdzone is `Europe/Amsterdam`.

---

## 9. Problemen oplossen

### `FileNotFoundError`

Controleer of dit bestand bestaat:

```text
data/wedstrijdkalender.xlsx
```

Controleer ook of je het programma vanuit de hoofdmap van de repository start.

---

### Google vraagt opnieuw om toestemming

Controleer of:

```text
credentials/credentials.json
```

aanwezig is.

Het programma gebruikt daarnaast:

```text
credentials/token.json
```

voor de opgeslagen Google-autorisatie.

---

### Er worden geen wedstrijden gevonden

Controleer:

- of het Excel-bestand op de juiste plek staat;
- of het werkblad `Blad1` heet;
- of de gegevens vanaf rij 2 staan;
- of de datumkolom daadwerkelijk Excel-datums bevat.

---

## Kort overzicht

Als alles eenmaal is ingesteld, hoef je normaal gesproken alleen dit te doen:

### 1. Excel aanpassen

```text
data/wedstrijdkalender.xlsx
```

### 2. Synchroniseren

```bash
python sync.py
```

### 3. Google Calendar controleren

De wedstrijden staan nu in de ingestelde agenda.

---

## Bestandsstructuur

De belangrijkste bestanden zijn:

```text
wedstrijdkalender-sync/
│
├── data/
│   └── wedstrijdkalender.xlsx
│
├── credentials/
│   ├── credentials.json
│   └── token.json
│
├── calendar_sync.py
├── config.py
├── models.py
├── parser.py
├── requirements.txt
└── sync.py
```

Je hoeft voor normaal gebruik vooral te werken met:

- `data/wedstrijdkalender.xlsx` → wedstrijdgegevens
- `config.py` → instellingen
- `sync.py` → programma starten

De overige Python-bestanden regelen het uitlezen en verwerken van de gegevens.
