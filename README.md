# MDIAC – Amazon Fine Food Reviews

## Objectif

Prédire le **sentiment** (positif / négatif) d'un avis client à partir de son texte,
en s'appuyant sur le jeu de données [Amazon Fine Food Reviews](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)
(~568 000 avis). Le score (1–5 étoiles) est converti en label binaire :
`Score >= 4` → positif, `Score <= 2` → négatif, `Score == 3` écarté.

## Données : `Reviews.csv`

Jeu de données public **Amazon Fine Food Reviews** (équipe SNAP de Stanford, hébergé sur Kaggle) :
~568 000 avis sur des produits alimentaires Amazon, d'octobre 1999 à octobre 2012,
~256 000 utilisateurs, ~74 000 produits, ~300 Mo.

| Colonne | Description |
|---|---|
| `Id` | Identifiant de la ligne |
| `ProductId` | Identifiant du produit (ASIN Amazon) |
| `UserId` | Identifiant de l'utilisateur |
| `ProfileName` | Nom affiché de l'utilisateur |
| `HelpfulnessNumerator` | Nombre de personnes ayant trouvé l'avis utile |
| `HelpfulnessDenominator` | Nombre de personnes ayant voté (utile ou non) |
| `Score` | Note de 1 à 5 étoiles |
| `Time` | Date de l'avis (timestamp Unix) |
| `Summary` | Titre court de l'avis |
| `Text` | Texte complet de l'avis |

Utilisation dans le projet :

- `Text` sert d'entrée au modèle ; `Score` donne la cible (4–5 = positif, 1–2 = négatif, 3 écarté).
- `UserId`, `ProfileName` et `Time` servent à supprimer les doublons (nombreux dans ce dataset).
- `Helpfulness*` sert à écarter les lignes incohérentes (plus de votes « utile » que de votes au total).

### Téléchargement (à faire par chaque membre de l'équipe)

Le fichier n'est **pas sur GitHub** (trop lourd, ignoré par `.gitignore`). Il doit être placé dans `data/raw/Reviews.csv`.

**Option 1 – à la main** : télécharger l'archive sur
<https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews>, la dézipper et copier `Reviews.csv` dans `data/raw/`.

**Option 2 – CLI Kaggle** (nécessite un token API Kaggle dans `~/.kaggle/kaggle.json`,
à générer depuis *Kaggle → Settings → API → Create New Token*) :

```bash
pip install kaggle
kaggle datasets download -d snap/amazon-fine-food-reviews -p data/raw --unzip
```

L'archive contient aussi `database.sqlite` (mêmes données au format SQLite) : il n'est pas utilisé et peut être supprimé.

## Matrice du projet

| Étape             | Fichier / dossier                  | Entrée                         | Sortie                              |
|-------------------|------------------------------------|--------------------------------|-------------------------------------|
| Explorer          | `notebooks/01_exploration.ipynb`   | `data/raw/Reviews.csv`         | Constats, graphiques                |
| Nettoyer          | `src/data/clean.py`                | `data/raw/Reviews.csv`         | `data/interim/reviews_clean.parquet`|
| Préparer          | `src/data/split.py`                | `data/interim/...`             | `data/processed/train.parquet`, `test.parquet` |
| Créer le modèle   | `src/models/train.py`              | `data/processed/train.parquet` | `models/model.joblib`               |
| Tester            | `src/models/evaluate.py`           | `test.parquet` + modèle        | Métriques (accuracy, F1…)           |
| Mettre en ligne   | `src/api/app.py` (FastAPI)         | `models/model.joblib`          | API `/predict`                      |
| Surveiller        | `monitoring/`                      | Logs de prédiction             | Rapports de drift                   |

## Structure

```
MDIAC-Amazon-Fine-Food-Reviews/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/              # Reviews.csv (gitignored)
│   ├── interim/          # données nettoyées
│   └── processed/        # train.parquet / test.parquet
├── notebooks/
│   └── 01_exploration.ipynb
├── src/
│   ├── data/clean.py
│   ├── data/split.py
│   ├── models/train.py
│   ├── models/evaluate.py
│   └── api/app.py
├── models/               # modèles entraînés (gitignored)
├── monitoring/
├── tests/
├── .github/workflows/ci.yml
└── .gitignore
```

## Comment lancer

```bash
# 1. Environnement
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt

# 2. Données : placer Reviews.csv dans data/raw/ (voir « Téléchargement » ci-dessus)

# 3. Pipeline
python -m src.data.clean
python -m src.data.split
python -m src.models.train
python -m src.models.evaluate

# 4. API
uvicorn src.api.app:app --reload
# → http://127.0.0.1:8000/docs

# 5. Tests
pytest
```

## Règles de contribution

**Une étape = une branche, et la pull request est obligatoire** (aucun push direct sur `main`).
Détails dans [CONTRIBUTING.md](CONTRIBUTING.md).

## Intégration continue

`.github/workflows/ci.yml` s'exécute à chaque push sur `main` et sur chaque pull request :
installation des dépendances, lint avec `ruff`, puis `pytest`.
