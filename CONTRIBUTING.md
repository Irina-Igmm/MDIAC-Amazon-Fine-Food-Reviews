# Règles de contribution

Ces règles s'appliquent à **toute personne qui touche au projet**.

## 1. Une étape = une branche

Chaque étape du projet se fait sur **sa propre branche**, créée à partir de `main` à jour.
Nommage : **`<nom_git>/<etape>`**, où `<nom_git>` est ton nom d'utilisateur GitHub et
`<etape>` l'étape (ou le step) traitée, sans accents ni espaces :

```bash
git checkout main
git pull
git checkout -b <nom_git>/<etape>
```

| Étape             | Exemple de nom de branche |
|-------------------|---------------------------|
| Explorer          | `Irina-Igmm/explorer`     |
| Nettoyer          | `Irina-Igmm/nettoyer`     |
| Préparer          | `Irina-Igmm/preparer`     |
| Créer le modèle   | `Irina-Igmm/modele`       |
| Tester            | `Irina-Igmm/tester`       |
| Mettre en ligne   | `Irina-Igmm/api`          |
| Surveiller        | `Irina-Igmm/surveiller`   |

Pour un travail hors étapes (setup, CI, docs), utiliser un step explicite : `Irina-Igmm/ci`, `Irina-Igmm/docs`…

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
