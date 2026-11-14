# Architecture — Mini Data Warehouse

## Schéma en étoile

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ dim_produit │     │ fact_ventes  │     │ dim_client  │
│─────────────│     │──────────────│     │─────────────│
│ produit_id  │◄────│ produit_id   │────▶│ client_id   │
│ nom         │     │ client_id    │     │ nom         │
│ categorie   │     │ date_id      │     │ ville       │
└─────────────┘     │ quantite     │     └─────────────┘
                    │ montant      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  dim_date   │
                    │─────────────│
                    │ date_id     │
                    │ date        │
                    │ annee/mois  │
                    └─────────────┘
```

## Avantages

- Requêtes analytiques simples
- Séparation faits / dimensions
- Facile à étendre
