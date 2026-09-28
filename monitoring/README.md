# Surveiller

- `logs/predictions.jsonl` : chaque appel à `/predict` y est journalisé (gitignored).
- `drift.py` : compare les prédictions de production au jeu d'entraînement
  (longueur des textes, part de positifs) et écrit `reports/drift_summary.json`.
  Pour un suivi plus complet, voir [Evidently](https://github.com/evidentlyai/evidently).
