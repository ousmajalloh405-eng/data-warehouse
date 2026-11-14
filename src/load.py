"""Chargement dans un schéma en étoile (SQLite)."""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime


def initialiser(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS dim_produit (
            produit_id INTEGER PRIMARY KEY,
            nom TEXT,
            categorie TEXT
        );
        CREATE TABLE IF NOT EXISTS dim_client (
            client_id INTEGER PRIMARY KEY,
            nom TEXT,
            ville TEXT
        );
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY,
            date TEXT UNIQUE,
            annee INTEGER,
            mois INTEGER,
            jour INTEGER
        );
        CREATE TABLE IF NOT EXISTS fact_ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_id INTEGER,
            produit_id INTEGER,
            client_id INTEGER,
            quantite INTEGER,
            montant REAL,
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
            FOREIGN KEY (produit_id) REFERENCES dim_produit(produit_id),
            FOREIGN KEY (client_id) REFERENCES dim_client(client_id)
        );
    """)
    conn.commit()


def charger_dimensions(conn: sqlite3.Connection):
    produits = [(1, "Laptop", "Informatique"), (2, "Smartphone", "Informatique"),
                (3, "Casque", "Accessoires"), (4, "Livre", "Livres")]
    clients = [(1, "Diallo", "Dakar"), (2, "Ndiaye", "Thiès"),
               (3, "Fall", "Saint-Louis"), (4, "Sow", "Ziguinchor")]
    conn.executemany("INSERT OR IGNORE INTO dim_produit VALUES (?, ?, ?)", produits)
    conn.executemany("INSERT OR IGNORE INTO dim_client VALUES (?, ?, ?)", clients)
    conn.commit()


def charger_faits(conn: sqlite3.Connection, csv_path: Path) -> int:
    count = 0
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row["date"]
            d = datetime.strptime(date_str, "%Y-%m-%d")
            cur = conn.execute("SELECT date_id FROM dim_date WHERE date = ?", (date_str,))
            res = cur.fetchone()
            if res:
                date_id = res[0]
            else:
                conn.execute(
                    "INSERT INTO dim_date (date, annee, mois, jour) VALUES (?, ?, ?, ?)",
                    (date_str, d.year, d.month, d.day),
                )
                date_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            montant = float(row["quantite"]) * float(row["prix"])
            conn.execute(
                """INSERT INTO fact_ventes (date_id, produit_id, client_id, quantite, montant)
                   VALUES (?, ?, ?, ?, ?)""",
                (date_id, int(row["produit_id"]), int(row["client_id"]),
                 int(row["quantite"]), round(montant, 2)),
            )
            count += 1
    conn.commit()
    return count
