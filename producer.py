import time
import json
import random
from kafka import KafkaProducer
from faker import Faker

TOPIC_NAME = 'website_clicks'
BOOTSTRAP_SERVERS = ['localhost:9092']

fake = Faker()

PRODUCTS = ['Laptop', 'Smartphone', 'Headphones', 'Monitor', 'Keyboard', 'Mouse', 'Smartwatch']

def json_normalizer(data):
    return json.dumps(data).encode('utf-8')

def get_random_click_data():
    return {
        "event_id": fake.uuid4(),
        "timestamp": int(time.time()),
        "user_id": random.randint(1, 1000),
        "page_url": f"/product/{random.choice(PRODUCTS)}",
        "user_region": fake.country_code(),
        "device_type": random.choice(['mobile', 'desktop', 'tablet'])
    }

def main():
    print(f"Démarrage du Producer Kafka sur le topic '{TOPIC_NAME}'...")

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=json_normalizer
    )

    try:
        while True:
            click_data = get_random_click_data()
            producer.send(TOPIC_NAME, value=click_data)
            print(f"Envoi : {click_data['user_id']} a cliqué sur {click_data['page_url']}")            
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        print("Stop producer...")
        producer.close()

if __name__ == "__main__":
    main()