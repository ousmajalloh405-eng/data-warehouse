"""Génération de données pour le schéma en étoile."""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

PRODUITS = [
    (1, "Laptop", "Informatique"),
    (2, "Smartphone", "Informatique"),
    (3, "Casque", "Accessoires"),
    (4, "Livre", "Livres"),
]

CLIENTS = [
    (1, "Diallo", "Dakar"),
    (2, "Ndiaye", "Thiès"),
    (3, "Fall", "Saint-Louis"),
    (4, "Sow", "Ziguinchor"),
]


def generer(n: int = 400, fichier: Path = Path("data/ventes_brutes.csv")) -> None:
    fichier.parent.mkdir(parents=True, exist_ok=True)
    debut = datetime(2026, 1, 1)
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "produit_id", "client_id", "quantite", "prix"])
        for _ in range(n):
            date = debut + timedelta(days=random.randint(0, 200))
            prod = random.choice(PRODUITS)
            client = random.choice(CLIENTS)
            qte = random.randint(1, 5)
            prix = round(random.uniform(20, 800), 2)
            writer.writerow([date.strftime("%Y-%m-%d"), prod[0], client[0], qte, prix])
    print(f"{n} lignes générées")
