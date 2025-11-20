# Pipeline d'Analyse de Clics en Temps Réel (Streaming)

Ce projet implémente une architecture de données **Event-Driven** (pilotée par les événements) capable d'ingérer et de traiter des données utilisateur en temps réel.

Contrairement aux pipelines "Batch" classiques (qui tournent une fois par jour), ce système utilise **Apache Kafka** pour traiter la donnée à la milliseconde où elle est générée.

## Architecture Streaming

```mermaid
graph LR
    A[Producer Python (Simulateur)] -- JSON Events --> B((Kafka Broker))
    B -- Topic: website_clicks --> C[Consumer Python]
    C -- Insert --> D[(PostgreSQL)]
```

* Producer : Simule le trafic d'un site E-commerce (génération aléatoire de clics, utilisateurs, produits) et sérialise les données en JSON.

* Broker (Kafka) : Gère le flux de messages à haute performance. Déployé via Docker avec l'image Confluent.

* Consumer : Écoute le topic Kafka en continu, désérialise les messages et les persiste dans une base de données relationnelle.

## Stack Technique

* Langage : Python 3.9+ (kafka-python, Faker, psycopg2)

* Message Broker : Apache Kafka (Confluent Platform) & Zookeeper

* Base de Données : PostgreSQL 14

* Infrastructure : Docker

* Monitoring : Kafdrop (Interface Web pour visualiser les topics Kafka)

## Comment l'exécuter
1. Prérequis : Docker et Python installés.

2. Lancer l'infrastructure :

```bash
docker-compose up -d
```
Cela démarre Zookeeper, Kafka, Kafdrop et Postgres.

3. Installer les dépendances :

```Bash
pip install -r requirements.txt
```
4. Lancer le Pipeline : Il faut ouvrir deux terminaux différents :

* Terminal 1 (Génération de trafic) :

```Bash
python producer.py
```

* Terminal 2 (Traitement des données) :

```Bash
python consumer.py
```

5. Visualisation :

* Accéder à Kafdrop sur http://localhost:9000 pour voir les messages transiter.

* Vérifier les données dans Postgres :

```Bash
docker exec -it postgres_db psql -U gazi -d clickstream_db -c "SELECT * FROM user_clicks ORDER BY id DESC LIMIT 10;"
```