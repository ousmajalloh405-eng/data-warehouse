"""Mini Data Warehouse — Schéma en étoile."""

import sys
from pathlib import Path
import sqlite3

sys.path.insert(0, str(Path(__file__).parent / "src"))

from generate import generer
from load import initialiser, charger_dimensions, charger_faits


CSV_PATH = Path(__file__).parent / "data" / "ventes_brutes.csv"
DB_PATH = Path(__file__).parent / "data" / "warehouse.db"


def requetes_analytiques(conn: sqlite3.Connection):
    print("\n=== Analyses ===")

    print("\nCA par catégorie :")
    for row in conn.execute("""
        SELECT p.categorie, ROUND(SUM(f.montant), 2) AS ca
        FROM fact_ventes f
        JOIN dim_produit p ON f.produit_id = p.produit_id
        GROUP BY p.categorie
        ORDER BY ca DESC
    """):
        print(f"  {row[0]:15} {row[1]} €")

    print("\nCA par ville :")
    for row in conn.execute("""
        SELECT c.ville, ROUND(SUM(f.montant), 2) AS ca
        FROM fact_ventes f
        JOIN dim_client c ON f.client_id = c.client_id
        GROUP BY c.ville
        ORDER BY ca DESC
    """):
        print(f"  {row[0]:15} {row[1]} €")

    print("\nCA par mois :")
    for row in conn.execute("""
        SELECT d.annee, d.mois, ROUND(SUM(f.montant), 2) AS ca
        FROM fact_ventes f
        JOIN dim_date d ON f.date_id = d.date_id
        GROUP BY d.annee, d.mois
        ORDER BY d.annee, d.mois
        LIMIT 6
    """):
        print(f"  {row[0]}-{row[1]:02d} : {row[2]} €")


def main():
    print("=== Mini Data Warehouse ===\n")

    generer(400, CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    initialiser(conn)
    charger_dimensions(conn)
    nb = charger_faits(conn, CSV_PATH)
    print(f"Faits chargés : {nb}")

    requetes_analytiques(conn)
    conn.close()
    print(f"\nBase créée : {DB_PATH}")
    print("Pipeline terminé.")


if __name__ == "__main__":
    main()
