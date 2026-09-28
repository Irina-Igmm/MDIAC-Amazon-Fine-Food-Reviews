# Règles de contribution

Ces règles s'appliquent à **toute personne qui touche au projet**.

## 1. Une étape = une branche

Chaque étape du projet se fait sur **sa propre branche**, créée à partir de `main` à jour :

```bash
git checkout main
git pull
git checkout -b <type>/<etape>-<description-courte>
```

| Étape             | Exemple de nom de branche          |
|-------------------|------------------------------------|
| Explorer          | `feat/explorer-distribution-scores`|
| Nettoyer          | `feat/nettoyer-suppression-doublons`|
| Préparer          | `feat/preparer-split-stratifie`    |
| Créer le modèle   | `feat/modele-tfidf-logreg`         |
| Tester            | `feat/tester-metriques-f1`         |
| Mettre en ligne   | `feat/api-endpoint-predict`        |
| Surveiller        | `feat/surveiller-drift`            |

Types : `feat/` (nouvelle fonctionnalité), `fix/` (correction), `docs/` (documentation),
`chore/` (configuration, outillage), `test/` (tests uniquement).

## 2. Pull request obligatoire

- **Aucun push direct sur `main`.** Toute modification passe par une pull request.
- La PR décrit l'étape concernée, ce qui a été fait et comment le vérifier.
- La CI (lint `ruff` + `pytest`) doit être **verte** avant le merge.
- Au moins **une relecture** par un autre membre de l'équipe avant le merge.
- Une fois mergée, la branche est supprimée.

## 3. Avant d'ouvrir la PR

```bash
ruff check src tests monitoring
pytest
```

Ne jamais commiter de données (`data/`, `*.csv`, `*.parquet`) ni de modèles entraînés (`models/`).
