# Mini Data Warehouse — Schéma en étoile

> Petit entrepôt de données avec schéma en étoile (faits + dimensions) pour analyser des ventes.

**Statut** : 🟢 Réalisé  
**Catégorie** : 🗄️ Solutions d’entrepôt de données  
**Portfolio** : [Profil GitHub](https://github.com/ousmajalloh405-eng)

---

## 1. Problème métier

Analyser les ventes selon plusieurs axes (produit, client, date) de façon simple et performante.

## 2. Schéma en étoile

```
          dim_date
             │
             │
dim_produit ─┼─ fact_ventes ─ dim_client
```

## 3. Tables

- **fact_ventes** : quantite, montant
- **dim_produit** : nom, categorie
- **dim_client** : nom, ville
- **dim_date** : date, annee, mois, jour

## 4. Technologies

- Python 3
- SQLite

## 5. Installation et exécution

```bash
git clone https://github.com/ousmajalloh405-eng/data-warehouse.git
cd data-warehouse
python3 main.py
```

## 6. Analyses fournies

- CA par catégorie
- CA par ville
- CA par mois

## 7. Compétences pour le CV

Conception et alimentation d’un schéma en étoile (Data Warehouse) avec tables de faits et de dimensions, et requêtes analytiques.

---

*Projet réalisé dans le cadre de la formation Data — Sonatel Academy.*
