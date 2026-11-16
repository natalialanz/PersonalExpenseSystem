#Progetto: Sistema di gestione delle spese personali

#Connessione al database SQLite

import sqlite3
from pathlib import Path

cartella_progetto = Path(__file__).resolve().parent

#Percorso del database e dello script SQL

percorso_database = cartella_progetto / "spese.db"
percorso_sql = cartella_progetto / "database.sql"

#Connessione al database e lettura del file SQL

connessione = sqlite3.connect(percorso_database)

#Attivazione delle chiavi esterne

connessione.execute("PRAGMA foreign_keys = ON")

try:
    with open(percorso_sql, "r", encoding= "utf-8") as file:
        script_sql = file.read()
        
#Esecuzione dello script SQL

    connessione.executescript(script_sql)

    print("==========================================")
    print("DATABASE CREATO CORRETTAMENTE!")
    print("Sistema di gestione delle spese personali")
    print("==========================================")

except sqlite3.Error as errore:
    print("ERRORE DURANTE LA CREAZIONE DEL DATABASE"), errore
    connessione.close()
    raise SystemExit

except OSError as errore:
    print("ERRORE NELLA LETTURA DEL FILE SQL"), errore
    connessione.close()
    raise SystemExit

# Creazione del cursore per eseguire le query SQL

cursor = connessione.cursor()

# Modulo 1 - Gestione delle categorie
def gestisci_categorie() :
    print("\n---- GESTIONE CATEGORIE ----")
    
# Visualizzazione delle categorie già presenti
    cursor.execute("SELECT id_categoria, nome FROM categorie ORDER BY id_categoria ASC")
    categorie = cursor.fetchall()
    print("\nCategorie già presenti:")

    if not categorie:
        print("Non ci sono ancora categorie registrate.")
    else:
        for categoria in categorie:
            print(f"{categoria[0]}. {categoria[1]}")
# 1. Definire il nome della categoria di spesa
    nome = input("Inserisci il nome della nuova categoria (oppure 0 per tornare al menu principale):").strip()
    if nome == "0":
        return

# 2. Verificare che il nome non sia vuoto
    if not nome:
        print("Errore: Il nome della categoria non può essere vuoto.")
        return
    
# 3. Controllo dell’esistenza della categoria (SQL SELECT)

    cursor.execute("SELECT id_categoria FROM categorie WHERE nome = ?", (nome,))
    categoria_esistente = cursor.fetchone()

    if categoria_esistente:
        print("Errore: la categoria inserita esiste già.")
        return
    
# 4. Inserimento della categoria se valida (SQL INSERT)
    cursor.execute("INSERT INTO categorie (nome) VALUES (?)",(nome,))
    connessione.commit()
    print("Categoria inserita correttamente.")

# Modulo 2 - Inserimento di una spesa
def inserisci_spesa():
    print("\n----- INSERISCI NUOVA SPESA -----")

# 1. Acquisizione di tutti gli input
    data = input("Inserisci la data (formato AAA-MM-GG)oppure 0 per tornare al menu principale: ").strip()
    if data == "0":
        return

    try:
        importo = float(input("Inserisci l'importo: "))
    except ValueError:
        print("Errore: Inserisci un importo numerico valido.")
        return

    categoria_nome = input("Inserisci il nome della categoria: ").strip ()
    descrizione = input("Inserisci una descrizione facoltativa: ").strip()

# 2. Validazione dell'importo
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di 0.")
        return
# 3. Controllo del formato e della validità della data
    try:
        from datetime import datetime
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print("Errore: la data inserita non è valida. Usa AAAA-MM-GG.")
        return

# 4. Verifica dell'esistenza della categoria (SQL SELECT)
    cursor.execute("SELECT id_categoria FROM categorie WHERE nome = ?",(categoria_nome,))
    categoria_trovata = cursor.fetchone()

    if not categoria_trovata :
        print("Errore: la categoria non esiste.")
        return
    categoria_id = categoria_trovata[0]
  
# 5. Inserimento della spesa nel database (SQL INSERT con chiave esterna)
    cursor.execute("INSERT INTO spese ( data, importo, id_categoria, descrizione) VALUES( ?,?,?,?)""", (data, importo, categoria_id, descrizione))
    connessione.commit()
    print("Spesa inserita correttamente!")

# Modulo 3 - Definizione del Budget Mensile
def definisci_budget():
    print("\n----- DEFINISCI BUDGET MENSILE -----")
    
# 1. Acquisisco gli input
    mese = input("Inserisci il mese (formato AAAA-MM):").strip()
    categoria_nome = input("Inserisci il nome della categoria: ").strip()

    try:
        importo_budget = float(input("Inserisci l'importo del budget: "))
    except ValueError:
        print("Errore: Inserisci un importo numerico valido.")
        return
# 2. Verifica che il budget sia maggiore di zero
    if importo_budget <= 0 :
        print("Errore: Il budget deve essere maggiore di 0:")
        return
# 3. Verifica del formato del mese
    from datetime import datetime
    try:
        datetime.strptime(mese, "%Y-%m")
    except ValueError:
        print("Errore: formato del mese non valido. Usa AAAA-MM.")
        return
# 4. Controllo dell'esistenza della categoria (SQL SELECT)
    cursor.execute("SELECT id_categoria FROM categorie WHERE nome = ?", (categoria_nome,))
    categoria_trovata = cursor.fetchone()

    if not categoria_trovata:
        print("Errore: la categoria non esiste.")
        return
    categoria_id = categoria_trovata[0]

# 5. Inserimento o aggiornamento del record di budget
    cursor.execute("INSERT INTO budget (mese, id_categoria, importo_budget) VALUES (?,?,?) ON CONFLICT (mese, id_categoria) DO UPDATE SET importo_budget = excluded.importo_budget""",(mese, categoria_id, importo_budget))
    connessione.commit()
    print("Budget mensile salvato correttamente.")

# Modulo 4 - Visualizzazione dei report
def visualizza_report():
    while True:
        print("\n --- MENU DEI REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese")
        print("4. Ritorna al menu principale")
        print("--------------------")

        scelta_report = input("Inserisci la tua scelta per il report (1-4):").strip()

# Report 1 - Totale delle spese per categoria

        if scelta_report == "1" :
            print("\n--- TOTALE SPESE PER CATEGORIA ---")
            print(f"{'Categoria' : <20} {'Totale Speso':>15}")
            print("-" * 35)

            cursor.execute("""SELECT c.nome, SUM (s.importo) FROM spese s JOIN categorie c ON s.id_categoria = c.id_categoria GROUP BY c.nome ORDER BY c.nome""")
            risultati = cursor.fetchall()
            if not risultati:
                print("Non sono presenti spese registrate.")
            else:
                for row in risultati:
                    print(f"{row[0]:<20} {row[1]:>15.2f} euro")
    
          
# Report 2 - Spese mensili vs budget

        elif scelta_report == "2":
            print("\n---SPESE MENSILI VS BUDGET---")
            cursor.execute("""WITH spese_mensili AS (SELECT SUBSTR(data, 1, 7) AS mese, id_categoria, SUM(importo) AS totale_speso
                    FROM spese GROUP BY SUBSTR(data, 1, 7), id_categoria),combinazioni AS (SELECT mese, id_categoria FROM budget UNION
                    SELECT mese, id_categoria FROM spese_mensili)SELECT combinazioni.mese, categorie.nome, COALESCE(budget.importo_budget, 0),
                    COALESCE(spese_mensili.totale_speso, 0)FROM combinazioni JOIN categorie ON combinazioni.id_categoria = categorie.id_categoria
                    LEFT JOIN budget ON combinazioni.mese = budget.mese AND combinazioni.id_categoria = budget.id_categoria LEFT JOIN spese_mensili
                    ON combinazioni.mese = spese_mensili.mese AND combinazioni.id_categoria = spese_mensili.id_categoria ORDER BY combinazioni.mese, categorie.nome""")
            risultati = cursor.fetchall()
            if not risultati:
                print("Non sono presenti spese o budget registrati.")
            else:
                for row in risultati:
                    mese, categoria, budget, speso = row
                    print(f"\nMese:{mese}")
                    print(f"Categoria: {categoria}")
                    print(f"Budget: {budget:.2f} euro")
                    print(f"Speso: {speso:.2f}euro")

                    if budget == 0:
                        print("Stato: BUDGET NON DEFINITO.")

                    elif speso > budget:
                        print("Stato: SUPERAMENTO DEL BUDGET")
                    else:
                        print("Stato: NELLA NORMA")

# Report 3 - Elenco completo delle spese

        elif scelta_report == "3":
            print("\n---- ELENCO COMPLETO DELLE SPESE----")
            print(f"{'Data':<12} {'Categoria':<15} {'Importo':<12} {'Descrizione':<25}")
            print("-" * 65)

            cursor.execute("""SELECT s.data, c.nome, s.importo, s.descrizione FROM spese s JOIN categorie c ON s.id_categoria = c.id_categoria ORDER BY s.data ASC, s.id_spesa ASC""")
            risultati = cursor.fetchall()
            if not risultati:
                print("Non sono presenti spese registrate.")
            else:
                for row in risultati:
                    data, categoria, importo, descrizione = row
                    print(f"{data:12} {categoria:<15}" f"{importo:<12.2f} {descrizione or '-':<25}")

        elif scelta_report == "4":
            print("Ritorno al MENU PRINCIPALE")
            break

        else:
            print("Scelta non valida. Riprova.")


# Ciclo principale del programma

print("=================================================")
print("BENVENUTO NEL SISTEMA DI GESTIONE SPESE PERSONALI")
print("=================================================")


while True:
    print("\n------MENU PRINCIPALE------")
    print("1. Gestione Categorie")
    print("2. Inserisci Nuova Spesa")
    print("3. Gestione Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("---------------------------")

    scelta = input("Seleziona un'opzione: ").strip()
    
# 1. Gestione delle categorie
    if scelta == "1" :
        print("Hai selezionato Gestione Categorie")
        gestisci_categorie()
# 2. Inserimento spesa
    elif scelta == "2" :
        print("Hai selezionato Inserisci Nuova Spesa")
        inserisci_spesa()
# 3. Definizione del budget
    elif scelta == "3" :
        print("Hai selezionato Gestione Budget Mensile")
        definisci_budget()
# 4. Visualizzazione del report
    elif scelta == "4" :
        print("Hai selezionato Visualizza Report")
        visualizza_report()
# 5. Uscita dal programma
    elif scelta == "5" :
        print("\nGrazie per aver utilizzato il programma. Arrivederci!")
        connessione.close()
        break
    
    else:
        print("\nScelta selezionata non valida. Inserisci un numero da 1 a 5 e riprova.")





    
    
    
