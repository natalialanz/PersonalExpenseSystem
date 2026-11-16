
# SISTEMA DI GESTIONE DELLE SPESE PERSONALI E DEL BUDGET

Il seguente elaborato descrive la realizzazione di un programma interattivo da console, progettato per consentire ad un singolo utente di tracciare le proprie spese attraverso macro-categorie, stabilire un budget mensile, inserire nuove spese e generare report finali di riepilogo.
Il sistema utilizza Python per la gestione delle funzionalità e SQLite per la memorizzazione dei dati.


## REQUISITI PER L'ESECUZIONE
Per poter eseguire questo programma da computer, assicurarsi di avere installato quanto segue:

- **Interprete necessario**: Python (versione 3.x consigliata)

link al download (https://www.python.org/downloads)

*NOTA PER UTENTI WINDOWS*: durante l'installazione 
assicurarsi di spuntare l'opzione **Add to Path**

- Il programma utilizza esclusivamente librerie standard integrate in Python come **sqlite3**, quindi non è necessaria l'installazione di pacchetti esterni.

- Un terminale nativo del sistema operativo (es. PowerShell su Windows.)
## CONFIGURAZIONE INIZIALE

Per utilizzare il programma è necessario scaricare il progetto da **GitHub**.

Aprire il terminale e digitare il seguente comando:
```bash
git clone https://github.com/natalialanz/PersonalExpenseSystem.git
```
In alternativa è possibile scaricare il progetto come archivio ZIP ed estrarlo sul computer:

https://github.com/natalialanz/PersonalExpenseSystem/archive/refs/heads/main.zip


## Istruzioni per l'esecuzione del programma

Puoi avviare il programma in due modalità:

1. PRIMO METODO: dal terminale
Esegui lo script principale digitando il seguente comando:
```bash
python main.py
```
2. SECONDO METODO: Tramite IDLE (Ambiente Python)

Clicca con il tasto destro sul file e seleziona **OPEN WITH IDLE**.
Seleziona RUN o digita il tasto F5 sulla tastiera per avviare l'applicazione nella console interattiva.
## STRUTTURA DELLA REPOSITORY
```text
PersonalExpenseSystem/
│
├── src/
│   └── main.py             # Codice sorgente dell'applicazione e menu interattivo
│
├── sql/
│   └── database.sql         # Script SQL con CREATE TABLE, vincoli e dati di esempio
│
├── demo/
│   └── demo_video.mp4       # Video dimostrativo delle funzionalità del programma
│
└── README.md                # Documentazione del progetto e guida all'esecuzione

```