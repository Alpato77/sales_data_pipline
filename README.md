# Pipeline de ventes e-commerce

Petit projet ETL local avec Apache Airflow, pandas et PostgreSQL. Le DAG lit le CSV source, le valide, nettoie les lignes, calcule le montant de chaque commande, puis charge les résultats dans PostgreSQL.

## Structure

```text
.
├── dags/ecommerce_sales_pipeline.py   # Orchestration du pipeline
├── data/raw/sales.csv                 # Données source
├── data/processed/                    # CSV intermédiaires et résultat transformé
├── postgres/init/                     # Création de la base et de la table au premier démarrage
├── scripts/extract.py                 # Lecture du CSV source
├── scripts/validates.py               # Vérification des colonnes et des données
├── scripts/transform.py               # Nettoyage et calcul de total_amount
├── scripts/load.py                    # Chargement idempotent vers PostgreSQL
├── Dockerfile                         # Image Airflow avec pandas
└── docker-compose.yaml                # Airflow, PostgreSQL et Redis
```

## Démarrer le projet

Il faut avoir Docker Desktop en cours d’exécution. Depuis ce dossier, lancer :

```bash
docker compose up --build -d
```

Airflow est disponible sur [http://localhost:8080](http://localhost:8080). En configuration locale, l’utilisateur et le mot de passe initiaux sont `airflow` / `airflow`. Le DAG `hello_myfirst_pipline` est créé en pause : l’activer dans l’interface, puis le déclencher manuellement.

PostgreSQL est accessible depuis l’hôte sur le port `5433` (port `5432` dans le réseau Docker). Les valeurs de développement sont : utilisateur `airflow`, mot de passe `airflow`, base `ecommerce_sales`. Airflow utilise la connexion `sales_postgres`, fournie par la variable `AIRFLOW_CONN_SALES_POSTGRES` dans Compose.

## Étapes du DAG

1. `check_data_availability` vérifie que `data/raw/sales.csv` existe.
2. `extract_sales` copie le fichier dans `data/processed/extracted_sales.csv`.
3. `validate_sales` vérifie les colonnes attendues et signale quelques anomalies.
4. `transform_sales` supprime les commandes en double ou invalides et calcule `total_amount`.
5. `load_sales` insère les lignes dans la table `sales`. Une commande déjà chargée est mise à jour grâce à `order_id`, ce qui permet de relancer le DAG sans créer de doublons.

## Vérifier PostgreSQL

```bash
docker compose exec postgres psql -U airflow -d ecommerce_sales
```

Dans l’invite SQL :

```sql
SELECT COUNT(*) FROM sales;
SELECT * FROM sales ORDER BY order_id LIMIT 10;
```

On peut aussi exécuter une requête sans ouvrir l’invite :

```bash
docker compose exec -T postgres psql -U airflow -d ecommerce_sales -c "SELECT COUNT(*) FROM sales;"
```

## Initialisation PostgreSQL

Les fichiers de `postgres/init/` sont exécutés automatiquement par l’image PostgreSQL uniquement lorsque son volume de données est initialisé pour la première fois. La base du projet est `ecommerce_sales` et sa table est `sales`. Le volume `postgres-db-volume` conserve les données entre les redémarrages.

Pour les identifiants de production, remplacer les valeurs de développement dans la configuration par des secrets locaux et ne pas publier ces secrets dans GitHub.
