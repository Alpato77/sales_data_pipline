# Rapport du projet — Pipeline de ventes e-commerce

## Objectif et fonctionnement

Ce projet automatise le traitement du fichier `data/raw/sales.csv` avec Apache Airflow, puis enregistre les ventes nettoyées dans PostgreSQL. Docker Compose lance les services nécessaires : Airflow, PostgreSQL et Redis. Le DAG Airflow orchestre les tâches dans l’ordre suivant :

1. **Vérifier et extraire** — le DAG vérifie la présence du CSV, puis `scripts/extract.py` le copie dans `data/processed/extracted_sales.csv`.
2. **Valider et transformer** — `scripts/validates.py` vérifie les colonnes nécessaires et signale les anomalies. `scripts/transform.py` retire les doublons et les lignes incomplètes ou invalides, convertit les dates et calcule `total_amount`. Le résultat est enregistré dans `data/processed/transformed_sales.csv`.
3. **Charger dans PostgreSQL** — `scripts/load.py` lit le fichier transformé et insère ou met à jour les commandes dans la table `sales`, en utilisant `order_id` pour éviter les doublons lors des relances.

## Mise en place

- Le service PostgreSQL existant sert à la base de métadonnées d’Airflow. Une base séparée, `ecommerce_sales`, est utilisée pour les données du projet.
- Les scripts dans `postgres/init/` créent la base et la table `sales` lors de l’initialisation d’un nouveau volume PostgreSQL. La table contient les identifiants de commande, client et produit, la quantité, le prix, la date, le statut et le montant total.
- Compose fournit à Airflow la connexion `sales_postgres`. Le fournisseur PostgreSQL étant déjà présent dans l’image Airflow, `load.py` utilise son `PostgresHook`.
- Les scripts et les données sont montés dans les conteneurs Airflow. `PYTHONPATH` permet au DAG d’importer les modules `scripts`. L’image personnalisée installe `pandas` pour les étapes de traitement.
- Le [README.md](README.md) décrit le démarrage, l’interface Airflow et les commandes de consultation PostgreSQL.

## Vérification et résultat

La configuration a été validée avec `docker compose config --quiet`. Le DAG `hello_myfirst_pipline` a ensuite été exécuté deux fois avec `airflow dags test`. Les deux exécutions ont réussi : 30 lignes ont été extraites, puis 27 lignes valides ont été transformées et chargées. Après la seconde exécution, PostgreSQL contenait toujours 27 commandes distinctes, ce qui confirme que le chargement peut être relancé sans créer de doublons. Airflow n’a signalé aucune erreur d’import du DAG.

Pour démarrer les services :

```bash
docker compose up --build -d
```

Airflow est accessible sur `http://localhost:8080`. PostgreSQL est accessible depuis l’hôte sur le port `5433`. Pour vérifier les données :

```bash
docker compose exec -T postgres psql -U airflow -d ecommerce_sales -c "SELECT COUNT(*) FROM sales;"
```

Les identifiants présents dans la configuration sont destinés à un usage local de développement.
