import json
from kafka import KafkaConsumer
import psycopg2

KAFKA_TOPIC = 'website_clicks'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'clickstream_db'
DB_USER = 'postgres'
DB_PASSWORD = 'password'

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def create_table_if_not_exists(conn):
    query = """
    CREATE TABLE IF NOT EXISTS user_clicks (
        id SERIAL PRIMARY KEY,
        event_id VARCHAR(50),
        timestamp BIGINT,
        user_id INT,
        page_url VARCHAR(100),
        user_region VARCHAR(10),
        device_type VARCHAR(20),
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()
        print("Table 'user_clicks' ready.")

def main():
    print(f"Démarrage du Consumer Kafka sur le topic '{KAFKA_TOPIC}'...")

    try:
        conn = get_db_connection()
        create_table_if_not_exists(conn)
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return
    
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest', # Lit depuis le début si on redémarre
        group_id='click_processor_group_1', # Identifiant du groupe de consommateurs
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Consumer prêt, en attente de messages...")

    try:
        cursor = conn.cursor()
        for message in consumer:
            data = message.value

            insert_query = """
            INSERT INTO user_clicks (event_id, timestamp, user_id, page_url, user_region, device_type)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['event_id'],
                data['timestamp'],
                data['user_id'],
                data['page_url'],
                data['user_region'],
                data['device_type']
            ))
            conn.commit()

            print(f"Sauvegarde : {data['user_id']} a cliqué sur {data['page_url']}")
    except KeyboardInterrupt:
        print("Stop consumer...")
    except Exception as e:
        print(f"Erreur lors du traitement des messages: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()