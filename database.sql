-- ===================================================
-- PROGETTO: SISTEMA  DI GESTIONE DELLE SPESE PERSONALI
-- Creazione del database e delle tabelle
 -- ===================================================

PRAGMA foreign_keys = ON;

-- ===================================================
-- TABELLA 1: CATEGORIE 
-- ===================================================

CREATE TABLE IF NOT EXISTS categorie (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE );

-- ===================================================
--TABELLA 2: SPESE 
-- ===================================================

CREATE TABLE IF NOT EXISTS spese (
    id_spesa INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL CHECK ( length(data) = 10
            AND data GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
            AND date(data) IS NOT NULL
            AND date(data) = data ),
    importo REAL NOT NULL CHECK (importo > 0),
    id_categoria INTEGER NOT NULL,
    descrizione TEXT,

    FOREIGN KEY (id_categoria)
           REFERENCES categorie(id_categoria) );

-- ===================================================
-- TABELLA 3: BUDGET 
-- ===================================================

CREATE TABLE IF NOT EXISTS budget (
    id_budget INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL
        CHECK (
            length(mese) = 7
            AND mese GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]'
            AND substr(mese, 6, 2) BETWEEN '01' AND '12' ),
    id_categoria INTEGER NOT NULL,
    importo_budget REAL NOT NULL CHECK (importo_budget > 0),

    FOREIGN KEY (id_categoria)
        REFERENCES categorie(id_categoria),
    UNIQUE (mese, id_categoria) );

 -- ==================================================
--  INSERIMENTO DATI DI ESEMPIO
-- ==================================================

-- CATEGORIE 

INSERT OR IGNORE INTO categorie
(id_categoria, nome)
VALUES
(1, 'Alimentari'),
(2, 'Salute'),
(3, 'Tempo libero'),
(4, 'Shopping');

-- SPESE  DICEMBRE 2026 

INSERT OR IGNORE INTO spese
(id_spesa, data, importo, id_categoria, descrizione)
VALUES
(1, '2026-12-01', 35.00, 1, 'Spesa supermercato'),
(2, '2026-12-02', 6.00, 2, 'Farmacia'),
(3, '2026-12-03', 45.00, 3, 'Abbonamento palestra'),
(4, '2026-12-04', 10.00, 3, 'Biglietti cinema'),
(5, '2026-12-05', 50.00, 4, 'Acquisto scarpe');

--  BUDGET  DICEMBRE 2026

INSERT OR IGNORE INTO budget
(id_budget, mese, id_categoria, importo_budget)
VALUES
(1, '2026-12', 1, 300.00),
(2, '2026-12', 2, 50.00),
(3, '2026-12', 3, 100.00),
(4, '2026-12', 4, 100.00);

-- FINE SCRIPT SQL 